from typing import Any, Dict, Iterator, Type, Union
from .table import Table, Multitable
from .adjective import Adjective
from .noun import Noun
from .verb import Verb
from .data import data

PartOfSpeech = Union[Type[Verb],
                     Type[Adjective],
                     Type[Noun],
                     Type[None]]

def part_of_speech(value: Dict[str, Any]) -> PartOfSpeech:
   if "t" in value:
      POS = value["t"].split('|')[0] # TODO: it gets calculated doubly here and inside concrete classes, rethink
      if POS == "V":
         return Verb
      if POS == "A":
         return Adjective
      if POS == "N":
         return Noun
   return type(None) # TODO other parts of speech

def lazy_lookup(key: str, yat:str="ekav") -> Iterator[Table]:
   with_se = key[-3:] == " се"
   if with_se:
      key = key[:-3]

   for caption, value in data[key]:
      POS = part_of_speech(value) # TODO: we have a rather different POS variable in part_of_speech, make it a dict there
      if POS is Verb:
         verb = Verb(key, value, yat)
         if with_se and not verb.is_reflexive:
            continue
         # TODO: simplify duplicate code here and a few lines below
         n_variants = len(verb.info.accents)
         for i in range(n_variants):
            full_caption = caption if n_variants == 1 else f"{caption} (вар. {i})"
            yield Table("verb", full_caption, verb.multiforms(variant=i, yat=yat))
      elif with_se: # for skipping meaningless queries like "адвокат се"
         continue
      elif POS is Adjective:
         adjective = Adjective(key, value, yat)
         n_variants = len(adjective.info.accents)
         for i in range(n_variants):
            full_caption = caption if n_variants == 1 else f"{caption} (вар. {i})"
            yield Table("adjective", full_caption, adjective.multiforms(variant=i, yat=yat))
      elif POS is Noun:
         noun = Noun(key, value, yat)
         n_variants = len(noun.info.accents)
         for i in range(n_variants):
            full_caption = caption if n_variants == 1 else f"{caption} (вар. {i})"
            yield Table("noun", full_caption, noun.multiforms(variant=i, yat=yat))
      else:
         yield Table("", "", iter([("😞", ["Још не знамо како се акцентује ова реч"])])) # TODO

def lookup(raw_word: str, yat:str="ekav") -> Multitable:
   return Multitable(raw_word, lazy_lookup(raw_word, yat))

def random_lookup() -> Multitable:
   return lookup(data.random_key())
