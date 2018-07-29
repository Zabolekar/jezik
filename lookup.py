from typing import Any, Dict, Iterator, Type, Union
from .table import Table, Multitable
from .adjective import Adjective
from .verb import Verb
from .data import data

PartOfSpeech = Union[Type[Verb],
                     Type[Adjective],
                     Type[None]]

def part_of_speech(value: Dict[str, Any]) -> PartOfSpeech:
   if "t" in value:
      POS = value["t"].split('|')[0] # TODO: it gets calculated doubly here and inside concrete classes, rethink
      if POS == "V":
         return Verb
      if POS == "A":
         return Adjective
   return type(None) # TODO other parts of speech

def lazy_lookup(key: str) -> Iterator[Table]:
   with_se = key[-3:] == " се"
   if with_se:
      key = key[:-3]

   for caption, value in data[key]:
      POS = part_of_speech(value) # TODO: we have a rather different POS variable in part_of_speech, make it a dict there
      if POS is Verb:
         verb = Verb(key, value)
         if with_se and not verb.is_reflexive:
            continue
         yield Table("verb", caption, verb.conjugate())
      elif with_se: # for skipping meaningless queries like "адвокат се"
         continue
      elif POS is Adjective:
         adjective = Adjective(key, value)
         yield Table("adjective", caption, adjective.decline())
      else:
         yield Table("", "", iter([("😞", ["Још не знамо како се акцентује ова реч"])])) # TODO

def lookup(raw_word: str) -> Multitable:
   return Multitable(raw_word, lazy_lookup(raw_word))

def random_lookup() -> Multitable:
   return lookup(data.random_key())
