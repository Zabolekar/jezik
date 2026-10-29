from ..generic_utils import Transform, compose1
from .text_utils import accentize, cyr2lat
from .phonology import (
   assimilate, deancientify, debracketify, decurlyerify, deyerify, je2ije
)
from .accents import garde, make_recessive, purify, ungarde

def apply_yat_and_latin(form: str, yat: str, latin: bool) -> str:
   if yat == "ije":
      form = je2ije(form)
   if latin:
      form = cyr2lat(form)
   return form

expose_transform: Transform[str] = compose1(
   (apply_yat_and_latin, ('yat', 'latin')),
   ungarde,
   (assimilate, ('yat',)),
   purify,
   make_recessive,
   debracketify,
   deyerify,
   decurlyerify,
   deancientify
)

def expose(form:str, yat:str="e", latin:bool=False) -> str:
   """
   all transformations from internal to external representation;
   ijekavian two-syllable yat appears only here, not in yat_replaces,
   otherwise ungarde() produces wrong results, i.e. **snìjeg
   """
   return expose_transform(form, yat=yat, latin=latin)

def expose_replacement(form:str, yat:str="e", latin:bool=False) -> str:
   return expose(garde(accentize(form)), yat, latin)
