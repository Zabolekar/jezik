from typing import Dict, NamedTuple, List, Optional
from .utils import insert, all_vowels

# TODO: when 3.7 is out, make Accents and GramInfo dataclasses

class Accents:

   def __init__(self, r: Dict[int, str], v: Dict[int, str]) -> None:
      self.r = r # syllabic r
      self.v = v # any other vowel

   def accentize(self, word: str) -> str: # traditional accentuation
      real_accent = {'`': '\u0300', '´': '\u0301', '¨': '\u030f', '^': '\u0311', '_': '\u0304', '!': '!'}
      if self.v:
         if self.r: # now we put the magic ring
            word = insert(word, self.r)
         # after that we create a dict with letter numbers representing vowels
         syllabic = 0
         position_to_accent: Dict[int, str] = {}
         for i, letter in enumerate(word):
            if letter in all_vowels:
               syllabic += 1
               if syllabic in self.v:
                  position_to_accent[i+1] = real_accent[self.v[syllabic]]
         return insert(word, position_to_accent) # then we insert accents into word!
      else:
         return word

class GramInfo:
   """
   How to read the field `other`:
   - If the word is a verb, then `other` contains a list with two elements,
   one of "Tr", "Itr", "Refl" (which means transitive, intransitive,
   reflexive) and one of "Pf", "Ipf", "Dv" (perfective, imperfective,
   biaspectual; abbreviation "Dv" comes from "dvòvīdan")
   """
   def __init__(self, infos: List[str], types: str) -> None:
      Rs: Optional[str] # circles below syllabic r's
      Vs: str # accents above vowels AND above circles (see Rs)
      accents = []
      self.AP: List[str] = []
      for inf in infos:
         if inf:
            line_accents, AP, MP = inf.split('|')
            if '@' in inf:
               Rs, Vs = line_accents.split('@')
            else:
               Rs, Vs = None, line_accents
            accents.append(Accents(
                {int(i): '\u0325' for i in Rs[1:].split(',')} if Rs else {},
                {int(i[:-1]): i[-1] for i in Vs.split(',')} if line_accents else {}
            )              )
            self.AP.append(AP) # accent paradigm
         else:
            raise ValueError("Can't decipher empty i")

      if types:
         POS, *other = types.split('|')
      else:
         raise ValueError("Can't decipher empty t")

      self.accents: List[Accents] = accents
      
      self.MP: str = MP # morphological paradigm
      self.POS: str = POS # part of speech
      self.other: List[str] = other

class AccentedTuple(NamedTuple):
   morpheme: str
   accent: str

