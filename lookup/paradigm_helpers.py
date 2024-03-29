from typing import Dict, List, Optional, Generic, Iterable, Tuple, TypeVar, Union
from collections import OrderedDict
from dataclasses import dataclass
from itertools import repeat
from re import compile as rcompile
from .charutils import real_accent

oa = ['o.', 'o:', 'a.', 'a:', 'a!', 'a¡', 'a?', 'a¿']
T = TypeVar('T')

_r = rcompile(r"([a-z]+|[A-Z]|\d)")
def nice_name(name:str) -> str:
   return " ".join(_r.findall(name))

def str_find(word:str, substr:str) -> int:
   found = word.find(substr)
   if found == -1:
      return len(word)
   return found

def has(word:Union[str, List[str]], *args:str) -> bool:
   """
   Actually could've been called smth like "contains_any"
   but we need some brevity here.
   """
   for arg in args:
      if arg in word:
         return True
   return False

def append_def(
   target_list:List[str],
   input_list:List[str],
   appendable:List[str],
   default_item:str
) -> List[str]:
   appended = False
   for item in input_list:
      if item in appendable:
         target_list.append(item)
         appended = True
   if not appended:
      target_list.append(default_item)
   return target_list

def accentize(word:str) -> str: # traditional accentuation
   for k, v in real_accent.items():
      word = word.replace(k, v)
   return word

@dataclass
class Accents:
   r: Dict[int, str] # syllabic r
   v: Dict[int, str] # any other vowel

def cut_AP (x:str) -> str:
   start = x.find('\\') + 1
   finish : Optional[int] = x.find('/')
   if finish == -1:
      finish = None
   return x[start:finish].replace('$', ':')

class GramInfo:
   """
   How to read the field `other`:
   - If the word is a verb, then `other` contains a list with two elements,
   one of "Tr", "Itr", "Refl" (which means transitive, intransitive,
   reflexive) and one of "Pf", "Ipf", "Dv" (perfective, imperfective,
   biaspectual; abbreviation "Dv" comes from "dvòvīdan")
   """
   def __init__(self, kind:str, infos:List[str]) -> None:
      # accents = []
      self.AP: List[str] = [] # accent paradigm
      self.MP: List[str] = [] # morphological paradigm
      self.comment: List[str] = []
      for info in infos:
         info = info.replace('$', ':') # a line cannot end with :, so we use $, too
         if info:
            try:
               if '\\' in info:
                  comment, restinfo = info.split('\\')
               else:
                  comment = ''
                  restinfo = info
            except ValueError:
               raise ValueError(f"too much backslashes in {info}")
            try:
               if '/' in restinfo:
                  AP, MP = restinfo.split('/')
               else:
                  AP = restinfo
                  MP = ''
            except ValueError:
               raise ValueError(f"too much slashes in {info}")

            self.AP.append(AP)
            self.MP.append(MP)
            self.comment.append(comment)
         else:
            raise ValueError("Can't decipher empty i")

      if kind:
         POS, *other = kind.split('\\')
      else:
         raise ValueError("Can't decipher empty t")

      #self.accents: List[Accents] = accents

      self.POS: str = POS # part of speech
      self.other: List[str] = other

@dataclass
class AccentedTuple:
   morpheme: str
   accent: str

MorphemeChain = List[AccentedTuple]
# the name sounds promising, but those "chains" are unlikely to be longer than two morphemes
LabeledEnding = Tuple[str, List[MorphemeChain]]

class OrderedSet(OrderedDict, Generic[T]):
   def __init__(self, i:Iterable[T]) -> None:
      super().__init__(zip(i, repeat(None)))

   def __repr__(self) -> str:
      return f"OrderedSet({list(self)})"

def uniq(i:Iterable[T]) -> List[T]:
   return list(OrderedSet(i))


@dataclass
class TableCaption:
   caption: str
   par: str
   subpar: str
   full_caption: str


def make_caption(
   caption:Tuple[str, str],
   n:int,
   i:int
) -> TableCaption:
   capt = caption[0]
   dis = caption[1].replace(":", "")
   if n == 1:
      return TableCaption(capt, dis, "1", capt)
   else:
      return TableCaption(capt, dis, str(i+1), f"{capt} (вар. {i+1})") # TODO latin
