
from typing import Iterator, Optional, Type, Union
from .adjective import Adjective
from .adverb import Adverb
from .charutils import all_latin
from .data import data
from .noun import Noun
from .table import Table, Multitable
from .paradigm_helpers import has, make_caption
from .utils import strip_suffix
from .verb import Verb

ACCENTS_NOT_FOUND_MESSAGE = [("😞", ["Још не знамо како се акцентује ова реч"])]

PartOfSpeech = Union[
   Type[Verb],
   Type[Adjective],
   Type[Noun],
   Type[Adverb]
]

# keys are the first component of the `t` field in data.yml, see NOTATION.md
parts_of_speech: dict[str, PartOfSpeech] = {
   "V": Verb,
   "A": Adjective,
   "N": Noun,
   "B": Adverb
}

def part_of_speech(kind:str) -> Optional[PartOfSpeech]:
   # TODO other parts of speech: they return None here
   return parts_of_speech.get(kind.split('\\')[0])

def lazy_lookup(key:str, input_yat:str, output_yat:str) -> Iterator[Table]:

   if input_yat not in ["e", "ije"] or output_yat not in ["e", "je", "ije"]:
      return # TODO: nice error message, this would only lead to "word not found"

   latin = has(key, *tuple(all_latin))

   key, with_se = strip_suffix(key.lower(), (" se", " се"))

   for inner_key, entry in data[key, input_yat]:
      POS = part_of_speech(entry.type)
      if with_se and ((POS is not Verb) or (POS is Verb and not 'Refl' in entry.type)):
         continue # for skipping meaningless queries like "адвокат се"
      elif POS:
         word = POS(inner_key, entry)
         n_variants = len(word.accented_keys)
         for i in range(n_variants):
            full_caption = make_caption(entry.caption, n_variants, i)
            yield Table(
               POS.__name__.lower(),
               full_caption,
               word.multiforms(variant=i, yat=output_yat, latin=latin),
               entry.view
            )
      else:
         yield Table(
            "",
            make_caption(("", ""), 1, 1),
            iter(ACCENTS_NOT_FOUND_MESSAGE),
            entry.view
         )
         # # TODO, and also sometimes ријеч and/or latin

def lookup(outer_key:str, input_yat:str="e", output_yat:Optional[str]=None) -> Multitable:
   if output_yat is None:
      output_yat = input_yat
   if input_yat == "je":
      input_yat = "ije"
   outer_key = outer_key.strip() # space-word-space will produce a search error otherwise
   return Multitable(outer_key, lazy_lookup(outer_key, input_yat, output_yat))

def random_key() -> tuple[str, str]:
   return data.random_key()
