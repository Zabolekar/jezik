from typing import Iterator, Dict, Any
from verb import Verb
from data import data

def part_of_speech(value: Dict[str, Any]) -> type:
   if 'i' in value:
      return Verb
   return type(None) # TODO other parts of speech

def lookup(raw_word: str) -> Iterator[Iterator[str]]:
   with_se = raw_word[-3:] == " се"
   if with_se:
      raw_word = raw_word[:-3]

   for key, value in data.all_entries(raw_word):
      if part_of_speech(value) is Verb:
         verb = Verb(key, value)
         if with_se and not verb.is_reflexive:
            continue
         yield verb.conjugate()
      elif with_se: # for skipping meaningless queries like "адвокат се"
         continue
      else:
         yield iter(["Ово није глагол 😞"]) # TODO

def random_word() -> Iterator[Iterator[str]]:
   yield from lookup(data.random_key())
