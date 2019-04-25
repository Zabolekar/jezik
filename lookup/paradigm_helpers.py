from typing import Dict, NamedTuple, List, Optional, Generic, Iterable, Tuple, TypeVar
from collections import OrderedDict
from itertools import repeat
from re import compile as rcompile
from .utils import insert, all_vowels
from .charutils import cacute, cgrave, cdoublegrave, ccircumflex, cmacron, cring, real_accent

# TODO: when 3.7 is out, make Accents and GramInfo dataclasses

oa = ['o.', 'o:', 'a.', 'a:', 'a!']
T = TypeVar('T')

_r = rcompile("([a-z]+|[A-Z]|\d)")
def nice_name(name: str) -> str:
   return " ".join(_r.findall(name))


def accentize(word: str, r: Dict[int, str], v: Dict[int, str]) -> str: # traditional accentuation
   
   if v:
      if r: # now we put the magic ring
         word = insert(word, r)
      # after that we create a dict with letter numbers representing vowels
      syllabic = 0
      position_to_accent: Dict[int, str] = {}
      for i, letter in enumerate(word):
         if letter in all_vowels:
            syllabic += 1
            if syllabic in v:
               position_to_accent[i+1] = real_accent[v[syllabic]]
      return insert(word, position_to_accent) # then we insert accents into word!
   else:
      return word

class Accents:
   def __init__(self, r: Dict[int, str], v: Dict[int, str]) -> None:
      self.r = r # syllabic r
      self.v = v # any other vowel

def i_to_accents(line_accents: str) -> Accents:
   if '@' in line_accents:
      Rs: Optional[str]
      Vs: str
      Rs, Vs = line_accents.split('@')
   else:
      Rs, Vs = None, line_accents
   Rs_dict = {int(i): cring for i in Rs[0:].split(',')} if Rs else {}
   Vs_dict = {int(i[:-1]): i[-1] for i in Vs.split(',')} if line_accents else {}
   return Accents(Rs_dict, Vs_dict)

class GramInfo:
   """
   How to read the field `other`:
   - If the word is a verb, then `other` contains a list with two elements,
   one of "Tr", "Itr", "Refl" (which means transitive, intransitive,
   reflexive) and one of "Pf", "Ipf", "Dv" (perfective, imperfective,
   biaspectual; abbreviation "Dv" comes from "dvòvīdan")
   """
   def __init__(self, kind: str, infos: List[str]) -> None:
      Rs: Optional[str] # circles below syllabic r's
      Vs: str # accents above vowels AND above circles (see Rs)
      accents = []
      self.AP: List[str] = [] # accent paradigm
      self.MP: List[str] = [] # morphological paradigm
      self.comment: List[str] = []
      for info in infos:
         if info:
            comment, line_accents, AP, MP = info.split('\\')
            accents.append(i_to_accents(line_accents))
            self.AP.append(AP)
            self.MP.append(MP)
            self.comment.append(comment)
         else:
            raise ValueError("Can't decipher empty i")

      if kind:
         POS, *other = kind.split('\\')
      else:
         raise ValueError("Can't decipher empty t")

      self.accents: List[Accents] = accents
      
      self.POS: str = POS # part of speech
      self.other: List[str] = other

class AccentedTuple(NamedTuple):
   morpheme: str
   accent: str

MorphemeChain = List[AccentedTuple] # the name sounds promising, but those "chains" are unlikely to be longer than two morphemes
LabeledEnding = Tuple[str, List[MorphemeChain]]

class OrderedSet(OrderedDict, Generic[T]): 
   def __init__(self, i: Iterable[T]) -> None: 
      super().__init__(zip(i, repeat(None))) 

   def __repr__(self) -> str: 
      return f"OrderedSet({list(self)})"