from typing import Dict, List, Optional, Generic, Iterable, Tuple, TypeVar
from collections import OrderedDict
from dataclasses import dataclass
from itertools import repeat
from re import compile as rcompile
from .utils import insert, all_vowels, expose
from .charutils import cring, real_accent

oa = ['o.', 'o:', 'a.', 'a:', 'a!']
T = TypeVar('T')

_r = rcompile(r"([a-z]+|[A-Z]|\d)")
def nice_name(name: str) -> str:
   return " ".join(_r.findall(name))

def appendDef(
   targetList: List[str],
   inputList: List[str],
   appendable: List[str],
   defaultItem: str
) -> List[str]:
   for item in inputList:
      if item in appendable:
         targetList.append(item)
      else:
         targetList.append(defaultItem)
   return targetList

def accentize(word: str, r: Dict[int, str], v: Dict[int, str]) -> str: # traditional accentuation

   if v:
      if r: # now we put the magic ring
         word = insert(word, r)
      # after that we create a dict with letter numbers representing vowels
      syllabic = 0
      position_to_accent: Dict[int, str] = {}

      # a test
      tmp = tmp = word + 'ø' if not word[-1] in all_vowels else word
      exposed_word = expose(tmp)
      a = len([letter for letter in exposed_word if letter in all_vowels])
      for number in v:
         if number > a:
            raise ValueError(f"word {exposed_word} got less syllables than you assert")

      for i, letter in enumerate(word):
         if letter in all_vowels:
            syllabic += 1
            if syllabic in v:
               position_to_accent[i+1] = real_accent[v[syllabic]]
      return insert(word, position_to_accent) # then we insert accents into word!
   else:
      return word

@dataclass
class Accents:
   r: Dict[int, str] # syllabic r
   v: Dict[int, str] # any other vowel

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
      accents = []
      self.AP: List[str] = [] # accent paradigm
      self.MP: List[str] = [] # morphological paradigm
      self.comment: List[str] = []
      for info in infos:
         if info:
            splitted_info = info.split('\\')
            if len(splitted_info) == 4:
               comment, line_accents, AP, MP = splitted_info
            elif len(splitted_info) == 3:
               comment, line_accents, AP = splitted_info
               MP = ""
            else:
               raise ValueError("Can't decipher info of len ", len(splitted_info))
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

@dataclass
class AccentedTuple:
   morpheme: str
   accent: str

MorphemeChain = List[AccentedTuple]
# # the name sounds promising, but those "chains" are unlikely to be longer than two morphemes
LabeledEnding = Tuple[str, List[MorphemeChain]]

class OrderedSet(OrderedDict, Generic[T]):
   def __init__(self, i: Iterable[T]) -> None:
      super().__init__(zip(i, repeat(None)))

   def __repr__(self) -> str:
      return f"OrderedSet({list(self)})"
