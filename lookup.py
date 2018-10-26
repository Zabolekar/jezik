from typing import Any, Dict, Iterator, Optional, Type, Union
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
      POS = value["t"].split('\\')[0] # TODO: it gets calculated doubly here and inside concrete classes, rethink
      if POS == "V":
         return Verb
      if POS == "A":
         return Adjective
      if POS == "N":
         return Noun
   return type(None) # TODO other parts of speech

def lazy_lookup(key: str, input_yat: str, output_yat: str) -> Iterator[Table]:

   with_se = key[-3:] == " се" # TODO Latin
   if with_se:
      key = key[:-3]

   for inner_key, (caption, value) in data.__getitem__(key, input_yat): # TODO without __
      POS = part_of_speech(value) # TODO: we have a rather different POS variable in part_of_speech, make it a dict there
      if POS is Verb:
         verb = Verb(inner_key, value, output_yat)
         if with_se and not verb.is_reflexive:
            continue
         # TODO: simplify duplicate code here and a few lines below
         n_variants = len(verb.info.accents)
         for i in range(n_variants):
            full_caption = caption if n_variants == 1 else f"{caption} (вар. {i+1})" # TODO latin
            yield Table("verb", full_caption, verb.multiforms(variant=i, yat=output_yat))
      elif with_se: # for skipping meaningless queries like "адвокат се"
         continue
      elif POS is Adjective:
         adjective = Adjective(inner_key, value, output_yat)
         n_variants = len(adjective.info.accents)
         for i in range(n_variants):
            full_caption = caption if n_variants == 1 else f"{caption} (вар. {i+1})"
            yield Table("adjective", full_caption, adjective.multiforms(variant=i, yat=output_yat))
      elif POS is Noun:
         noun = Noun(inner_key, value, output_yat)
         n_variants = len(noun.info.accents)
         for i in range(n_variants):
            full_caption = caption if n_variants == 1 else f"{caption} (вар. {i+1})"
            yield Table("noun", full_caption, noun.multiforms(variant=i, yat=output_yat))
      else:
         yield Table("", "", iter([("😞", ["Још не знамо како се акцентује ова реч"])])) # TODO, and also sometimes ријеч and/or latin

def lookup(outer_key: str, input_yat:str="ekav", output_yat:Optional[str]=None) -> Multitable:
   if output_yat is None:
      output_yat = input_yat
   return Multitable(outer_key, lazy_lookup(outer_key, input_yat, output_yat))

def random_lookup() -> Multitable:
   return lookup(*data.random_key())
