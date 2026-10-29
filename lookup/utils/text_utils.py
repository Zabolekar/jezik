import re
from itertools import chain
from typing import Optional, Iterator, Pattern
from . import characters as c
from .charutils import any_vowel, notation_marks, real_accent

# Naming of things added for optimization purposes:
#   <name>_c − <name> but with compiled regexes
#   <name>_translator — a translation table used by `str.translate`
#   _<funcname>_<name> — a thing used by function `funcname`

cyr2lat_dict: dict[str, str] = {
   'й':'ĭ', 'Й':'Ĭ',
   'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'ђ':'đ', 'е':'e', 'ж':'ž', 'з':'z', 'и':'i',
   'ј':'j', 'к':'k', 'л':'l', 'љ':'lj', 'м':'m', 'н':'n', 'њ':'nj', 'о':'o', 'п':'p', 'р':'r',
   'с':'s', 'т':'t', 'ћ':'ć', 'у':'u', 'ф':'f', 'х':'h', 'ц':'c', 'ч':'č', 'џ':'dž', 'ш':'š',
   'А':'A', 'Б':'B', 'В':'V', 'Г':'G', 'Д':'D', 'Ђ':'Đ', 'Е':'E', 'Ж':'Ž', 'З':'Z', 'И':'I',
   'Ј':'J', 'К':'K', 'Л':'L', 'Љ':'Lj', 'М':'M', 'Н':'N', 'Њ':'Nj', 'О':'O', 'П':'P', 'Р':'R',
   'С':'S', 'Т':'T', 'Ћ':'Ć', 'У':'U', 'Ф':'F', 'Х':'H', 'Ц':'C', 'Ч':'Č', 'Џ':'Dž', 'Ш':'Š'
   }

cyr2lat_translator = str.maketrans(cyr2lat_dict)

def cyr2lat(lowertext:str) -> str:
   return lowertext.translate(cyr2lat_translator)

_any_vowel_c: Pattern = re.compile(any_vowel)

def last_vowel_index(trunk:str) -> Optional[int]:
   if _any_vowel_c.search(trunk):
      *__, last_vowel = _any_vowel_c.finditer(trunk)
      index, _ = last_vowel.span()
      return index
   return None

def first_vowel_index(trunk:str) -> Optional[int]:
   match = _any_vowel_c.search(trunk)
   if match:
      return match.span()[0]
   return None

def indices(trunk:str) -> tuple[Optional[int], Optional[int], Optional[int]]:
   lvi = last_vowel_index(trunk)
   fvi = first_vowel_index(trunk)
   pvi = last_vowel_index(trunk[:lvi])
   return lvi, fvi, pvi

def swap(word:str, c1:str, c2:str) -> str:
   return word.replace(c1+c2, c2+c1)


def insert(word:str, position_to_accent:dict[int, str]) -> str:
   if not position_to_accent:
      return word

   keys = sorted(position_to_accent.keys())

   def pieces() -> Iterator[str]:
      yield word[:keys[0]]

      for i in range(1, len(keys)):
         yield position_to_accent[keys[i-1]]
         yield word[keys[i-1]:keys[i]]

      yield position_to_accent[keys[-1]]
      yield word[keys[-1]:]

   return ''.join(pieces())

_deaccentize_accented: dict[str, str] = {
   'ȁȃâáàā': 'a', 'ȅȇêéèē': 'e', 'ȉȋîíìīĭ': 'i',
   'ȕȗûúùū': 'u', 'ȑȓŕ': 'r', 'ȀȂÂÁÀĀ': 'A',
   'ȄȆÊÉÈĒ': 'E', 'ȈȊÎÍÌĪĬ': 'I', 'ȔȖÛÚÙŪ': 'U',
   'ȐȒŔ': 'R', 'ȍȏôóòō': 'o', 'ȌȎÔÓÒŌ': 'O',
   'ӣѝй': 'и', 'ѐ': 'е', 'ӢЍЙ': 'И', 'Ѐ': 'Е'}

_deaccentize_translator = str.maketrans(dict(chain(
   ((acc, deacc) for accs, deacc in _deaccentize_accented.items()
                 for acc in accs),
   ((mark, None) for mark in c.items()),
   ((mark, None) for mark in notation_marks)
)))

def accentize(word:str) -> str: # traditional accentuation
   for k, v in real_accent.items():
      word = word.replace(k, v)
   return word

def deaccentize(text:str) -> str:
   return text.translate(_deaccentize_translator)
