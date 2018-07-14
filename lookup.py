from typing import Any, Dict, Iterator, List
from .table import Table
from .adjective import Adjective
from .verb import Verb
from .data import data

class Multitable(list):
   """
   # TODO:
   Currently, it has to be a list because we need its length to display the
   table caption. Later, when the disambiguators are ready, we can greatly 
   simplify this file and get rid of the whole lookup/lazy_lookup distinction.
   """
   def __init__(self, word: str, iterable: Iterator[Table]) -> None:
      super().__init__(iterable)
      self.word = word

def part_of_speech(value: Dict[str, Any]) -> type: # TODO: make more precise
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
         yield Table(caption, verb.conjugate())
      elif with_se: # for skipping meaningless queries like "адвокат се"
         continue
      elif POS is Adjective:
         adjective = Adjective(key, value)
         yield Table(caption, adjective.decline())
      else:
         yield Table("", iter([("😞", ["Још не знамо како се акцентује ова реч"])])) # TODO

def lookup(raw_word: str) -> Multitable:
   return Multitable(raw_word, lazy_lookup(raw_word))

def random_lookup() -> Multitable:
   return lookup(data.random_key())
