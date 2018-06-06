from typing import Iterator, Dict, Any
from .adjective import Adjective
from .verb import Verb
from .data import data

def part_of_speech(value: Dict[str, Any]) -> type: # TODO: make more precise
   if "t" in value:
      POS = value["t"].split('|')[0] # TODO: it gets calculated doubly here and inside concrete classes, rethink
      if POS == "V":
         return Verb
      if POS == "A":
         return Adjective
   return type(None) # TODO other parts of speech

def lookup(raw_word: str) -> Iterator[Iterator[str]]:
   with_se = raw_word[-3:] == " се"
   if with_se:
      raw_word = raw_word[:-3]

   for key, value in data[raw_word]:
      POS = part_of_speech(value) # TODO: we have a rather different POS variable in part_of_speech, make it a dict there
      if POS is Verb:
         verb = Verb(key, value)
         if with_se and not verb.is_reflexive:
            continue
         yield verb.conjugate()
      elif with_se: # for skipping meaningless queries like "адвокат се"
         continue
      elif POS is Adjective:
         adjective = Adjective(key, value)
         yield adjective.decline()
      else:
         yield iter(["Још не знамо како се акцентује ова реч 😞"]) # TODO

def random_lookup() -> Iterator[Iterator[str]]:
   yield from lookup(data.random_key())
