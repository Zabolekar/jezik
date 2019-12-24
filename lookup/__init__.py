from typing import Dict, Iterator, Optional, Tuple, Type, Union
from .table import Table, Multitable
from .adjective import Adjective
from .adverb import Adverb
from .noun import Noun
from .verb import Verb
from .data import data
from .charutils import all_latin
from .utils import strip_suffix

PartOfSpeech = Union[
   Type[Verb],
   Type[Adjective],
   Type[Noun],
   Type[Adverb],
   Type[None]
]

def part_of_speech(kind: str) -> PartOfSpeech:
   POS = kind.split('\\')[0] # TODO: it gets calculated doubly here and inside concrete classes, rethink
   if POS == "V":
      return Verb
   if POS == "A":
      return Adjective
   if POS == "N":
      return Noun
   if POS == "B":
      return Adverb
   return type(None) # TODO other parts of speech

def lazy_lookup(key: str, input_yat: str, output_yat: str) -> Iterator[Table]:

   if input_yat not in ["e", "ije"] or output_yat not in ["e", "je", "ije"]:
      return # TODO: nice error message, this would only lead to "word not found"

   latin = any(x in key for x in all_latin)

   key, with_se = strip_suffix(key, (" se", " се"))

   for inner_key, (caption, accented_keys, extra_key, kind, info, replacements, amendments) in data[key, input_yat]:
      POS = part_of_speech(kind)
      # # TODO: we have a rather different POS variable in part_of_speech, make it a dict there
      if POS is Verb:
         verb = Verb(inner_key, accented_keys, kind, info, replacements, amendments)
         # # TODO: can we avoid passing kind and info again? POS already knows
         if with_se and not verb.is_reflexive:
            continue
         # TODO: simplify duplicate code here and a few lines below
         n_variants = len(verb.accented_keys)
         for i in range(n_variants):
            full_caption = caption if n_variants == 1 else f"{caption} (вар. {i+1})" # TODO latin
            yield Table(
               "verb",
               full_caption,
               verb.multiforms(variant=i, yat=output_yat, latin=latin)
            )
      elif with_se: # for skipping meaningless queries like "адвокат се"
         continue
      elif POS is Adjective:
         adjective = Adjective(inner_key, accented_keys, kind, info, replacements, amendments)
         n_variants = len(adjective.accented_keys)
         for i in range(n_variants):
            full_caption = caption if n_variants == 1 else f"{caption} (вар. {i+1})"
            yield Table(
               "adjective",
               full_caption,
               adjective.multiforms(variant=i, yat=output_yat, latin=latin)
            )
      elif POS is Noun:
         noun = Noun(inner_key, accented_keys, kind, info, replacements, amendments)
         n_variants = len(noun.accented_keys)
         for i in range(n_variants):
            full_caption = caption if n_variants == 1 else f"{caption} (вар. {i+1})"
            yield Table(
               "noun",
               full_caption,
               noun.multiforms(variant=i, yat=output_yat, latin=latin)
            )
      elif POS is Adverb:
         adverb = Adverb(inner_key, accented_keys, kind, info)
         n_variants = len(adverb.accented_keys)
         for i in range(n_variants):
            full_caption = caption if n_variants == 1 else f"{caption} (вар. {i+1})"
            yield Table(
               "adverb",
               full_caption,
               adverb.multiforms(variant=i, yat=output_yat, latin=latin)
            )
      else:
         yield Table("", "", iter([("😞", ["Још не знамо како се акцентује ова реч"])]))
         # # TODO, and also sometimes ријеч and/or latin

def lookup(outer_key: str, input_yat:str="e", output_yat:Optional[str]=None) -> Multitable:
   if output_yat is None:
      output_yat = input_yat
   if input_yat == "je":
      input_yat = "ije"
   outer_key = outer_key.strip() # space-word-space will produce a search error otherwise
   return Multitable(outer_key, lazy_lookup(outer_key, input_yat, output_yat))

def random_key() -> Tuple[str, str]:
   return data.random_key()
