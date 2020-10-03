
from typing import Dict, Iterator, Optional, Tuple, Type, Union
from .adjective import Adjective
from .adverb import Adverb
from .charutils import all_latin
from .data import data
from .noun import Noun
from .table import Table, Multitable
from .paradigm_helpers import has, make_caption
from .utils import strip_suffix
from .verb import Verb


PartOfSpeech = Union[
   Type[Verb],
   Type[Adjective],
   Type[Noun],
   Type[Adverb]
]

def part_of_speech(kind:str) -> Optional[PartOfSpeech]:
   POS = kind.split('\\')[0]
   # TODO: it gets calculated doubly here and inside concrete classes, rethink

   if POS == "V":
      return Verb
   if POS == "A":
      return Adjective
   if POS == "N":
      return Noun
   if POS == "B":
      return Adverb
   return None # TODO other parts of speech

def lazy_lookup(key:str, input_yat:str, output_yat:str) -> Iterator[Table]:

   if input_yat not in ["e", "ije"] or output_yat not in ["e", "je", "ije"]:
      return # TODO: nice error message, this would only lead to "word not found"

   latin = has(key, *tuple(all_latin))

   key, with_se = strip_suffix(key, (" se", " се"))

   for inner_key, values in data[key, input_yat]:
      caption, accented_keys, _, kind, info, replacements, amendments = values
      POS = part_of_speech(kind)
      # # TODO: we have a rather different POS variable in part_of_speech, make it a dict there
      if with_se and ((POS is not Verb) or (POS is Verb and not 'Refl' in kind)):
         continue # for skipping meaningless queries like "адвокат се"
      elif POS:
         word = POS(inner_key, accented_keys, kind, info, replacements, amendments)
         # # TODO: can we avoid passing kind and info again? POS already knows
         n_variants = len(word.accented_keys)
         for i in range(n_variants):
            full_caption = make_caption(caption, n_variants, i)
            yield Table(
               POS.__name__.lower(),
               full_caption,
               word.multiforms(variant=i, yat=output_yat, latin=latin)
            )
      else:
         yield Table(
            "",
            make_caption(("", ""), 1, 1),
            iter([("😞", ["Још не знамо како се акцентује ова реч"])])
         )
         # # TODO, and also sometimes ријеч and/or latin

def lookup(outer_key:str, input_yat:str="e", output_yat:Optional[str]=None) -> Multitable:
   if output_yat is None:
      output_yat = input_yat
   if input_yat == "je":
      input_yat = "ije"
   outer_key = outer_key.strip() # space-word-space will produce a search error otherwise
   return Multitable(outer_key, lazy_lookup(outer_key, input_yat, output_yat))

def random_key() -> Tuple[str, str]:
   return data.random_key()
