from typing import Optional
from dataclasses import dataclass
from re import compile as rcompile

roman = ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII') # declension classes

oa = ['o.', 'o:', 'a.', 'a:', 'a!', 'a¡', 'a?', 'a¿']

adj_AP_pairs = (
   ('a.,a.', 'A.'),
   ('0,a.', 'a.'),
   ('a:,a:', 'A:'),
   ('b:,b:', 'B:'),
   ('0,a:', 'a:'),
   ('0,c.', 'c.'),
   ('b.,b.', 'B.'),
   ('b.,c.', 'K.'),
   ('0,c:', 'c:'),
   ('b:,c.', 'K:.'),
   ('a.,c.', 'L.'),
   ('b?,b.', 'B?.'),
   ('a.,a:', 'A.:'),
   ('d:,b:', 'M:'),
   ('d.,b.', 'M.'),
   ('b:,c:', 'K:'),
   ('a:,c.', 'L:.'),
   ('b.,b:', 'B.:'),
   ('d.,c.', 'N.')
)  # rules: 0,x is x; x,x is X; bc ac db dc become KLMN;
   # leave one length mark if they are the same,
   # two length marks if they are different

adj_AP_to_inner_AP = {b:a for a,b in adj_AP_pairs}

infinitive_dict: dict[str, str] = {
   'alpha': 'ити', 'beta': 'ати', 'gamma': 'нути',
   'delta': 'ати', 'epsilon': 'овати', 'zeta': 'ивати',
   'eta': 'ѣти', 'theta': 'ети', 'iota': 'ати',
   'kappa': 'ти', 'kappa2': 'ти', 'kappa3': 'ти', 'lambda': 'ти', 'mu': 'ати'
}

_r = rcompile(r"([a-z]+|[A-Z]|\d)")
def nice_name(name:str) -> str:
   return " ".join(_r.findall(name))

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
   def __init__(self, kind:str, infos:list[str]) -> None:
      self.AP: list[str] = [] # accent paradigm
      self.MP: list[str] = [] # morphological paradigm
      self.comment: list[str] = []
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

      self.POS: str = POS # part of speech
      self.other: list[str] = other

@dataclass
class AccentedTuple:
   morpheme: str
   accent: str

MorphemeChain = list[AccentedTuple]
# the name sounds promising, but those "chains" are unlikely to be longer than two morphemes
LabeledEnding = tuple[str, list[MorphemeChain]]
