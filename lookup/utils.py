# TODO:
# ----- well-named function for recessive accent,
#       e.g. recessive(sequence) -> se̍quence
# ----- think of better name for prettify(), like alternate() or assimilate()

import re
from typing import (
   Union, Optional, Callable, TypeVar,
   Iterator, Iterable, Sequence,
   Pattern, Dict, List, Tuple
)
from itertools import chain
from .charutils import *


# Naming of things added for optimization purposes:
#   <name>_c − <name> but with compiled regexes
#   <name>_translator — a translation table used by `str.translate`
#   _<funcname>_<name> — a thing used by function `funcname`

palatalization_modes: Dict[str, Dict[str, str]] = {
   'и': {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
         'ст': 'шт', 'зд': 'жд', 'сл': 'шљ', 'зл': 'жљ',
         'шт': 'шт', 'жд': 'жд', 'ск': 'шт', 'зг': 'жд',
         'к': 'к', 'ц': 'ч', 'х': 'х', 'г': 'г',
         'ш': 'ш', 'ж': 'ж', 'ч': 'ч', 'џ': 'џ',
         'т': 'ћ', 'д': 'ђ', 'с': 'ш', 'з': 'ж',
         'л': 'љ', 'р': 'р', 'н': 'њ', 'ј': 'ј'},
   '': {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
        'ст': 'шћ', 'зд': 'жђ', 'сл': 'шљ', 'зл': 'жљ',
        'шт': 'шћ', 'жд': 'жђ', 'ск': 'шт', 'зг': 'жд',
        'к': 'ч', 'ц': 'ч', 'х': 'ш', 'г': 'ж',
        'ш': 'ш', 'ж': 'ж', 'ч': 'ч', 'џ': 'џ',
        'т': 'ћ', 'д': 'ђ', 'с': 'ш', 'з': 'ж',
        'л': 'љ', 'р': 'р', 'н': 'њ', 'ј': 'ј'}
}

cyr2lat_dict: Dict[str, str] = {
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

def indices(trunk:str) -> Tuple[Optional[int], Optional[int], Optional[int]]:
   lvi = last_vowel_index(trunk)
   fvi = first_vowel_index(trunk)
   pvi = last_vowel_index(trunk[:lvi])
   return lvi, fvi, pvi

def swap(word:str, c1:str, c2:str) -> str:
   return word.replace(c1+c2, c2+c1)


def insert(word:str, position_to_accent:Dict[int, str]) -> str:
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

def palatalize(sequence:str, mode: str='') -> str:
   idict = palatalization_modes[mode]
   digraphs = ['ст', 'зд', 'сл', 'зл', 'шт', 'жд', 'ск', 'зг']
   if sequence[-2:] in digraphs:
      return sequence[:-2] + idict[sequence[-2:]]

   return sequence[:-1] + idict[sequence[-1]]

_deyerify_repl_dict: Dict[str, str] = {
   "стън": "сн",
   "бък": "пк", "дък": "тк", "ђък": "ћк",
   "жък": "шк", "зък": "ск", "џък": "чк",
   "бът": "пт", "дът": "т", "ђт": "ћт",
   "жът": "шт", "зът": "ст", "џът": "чт",
   "бъц": "пц", "ђъц": "ћц", "дъц": "дц", "тъц": "ц",
   "жъц": "шц", "зъц": "сц", "џъц": "чц",
   "бъч": "пч", "ђъч": "ћч", "дъч": "ч", "тъч": "ч",
   "жъч": "шч", "зъч": "шч", "съч": "шч", "џъч": "ч"
}

# TODO: Name these two semantically:
_deyerify_pat1_c: Pattern = re.compile(f'([аеиоу{c.ring}][{c.straight}·]?)([лљмнњрјв]ʲ?)ъ')
_deyerify_pat2_c: Pattern = re.compile(f'[бвгдђжзјклʌљмнњпрṕсćтћфхцчџш]ʲ?{c.straight}')

_deyerify_translator = str.maketrans({
   'ø': None,
   'ъ': 'а',
   'ꚜ': 'а',
   'ꙏ': 'а'
})

_decurlyerify_repl_dict: Dict[str, str] = {
   k.replace('ъ', 'ꙏ') : v for k,v  in _deyerify_repl_dict.items()
}

def decurlyerify(form:str) -> str:
   for k, v in _decurlyerify_repl_dict.items():
      form = form.replace(k, v)
   return re.sub('([лљмнњрјв]ꙏ)', f'{c.macron}\\1', form).replace('ꙏ', '')

def deyerify(form:str) -> str:
   repl_dict = _deyerify_repl_dict
   re1 = _deyerify_pat1_c
   re2 = _deyerify_pat2_c

   two_yers = form.count('ъ') == 2 # зајутрак, зајутарка; probably not the best place to do it

   if form.endswith(c.straight+'ø'):
      form = form.replace('ø', '')
   if 'ø' in form:
      if two_yers and not '>' in form:
         form = form.replace('ъ', '', 1)
      form = form.translate(_deyerify_translator)
   else:
      if two_yers:
         form = form.replace('ъ', f'а{c.macron}', 1).replace('ъ', '')
      form = re1.sub(f'\\1{c.macron}\\2ъ', form)
      for k, v in repl_dict.items():
         form = form.replace(k, v)
      form = form.replace('ъ', '').replace('ꚜ', '').replace('ꙏ', '')

   match = re2.search(form)
   if match:
      wrong_acc_index = match.span()[0]
      form = form.replace(c.straight, '')
      lvi = last_vowel_index(form[:wrong_acc_index+2])
      if lvi is None:
         raise ValueError(f"_{form[:wrong_acc_index+2]}_ does not contain any vowels")
      else:
         form = insert(form, {lvi+1: c.straight})
   return form

_prettify_replaces: List[Tuple[str, str]] = [
   ('([чшжј])ѣ', '\\1а'), ('(шт|жд)ѣ', '\\1а'),
   (f'јӥ{c.straight}', f'{c.straight}јӥ'), ('јӥ', f'{c.macron}ј'),
   ('ӥ', 'и'), (f'{c.straight}{c.macron}', f'{c.macron}{c.straight}'),
   (f'ʌ([аеиоурœĵ]|{c.ring})', 'л\\1'),
   (f'{c.macron}{c.straight}ʌ', f'{c.straight}ʌ'),
   (f'{c.macron}ʌ', 'ʌ'),
   ('о·ʌ', f'о{c.macron}·'), ('оʌ', f'о{c.macron}'),
   (f'о{c.straight}ʌ', f'о{c.macron}{c.straight}'),
   (f'о·{c.macron}ʌ', f'о·{c.macron}'), ('ʌ', 'о'),
   ('цœ', 'че'),
   ('([ҵчџњљћђшжјʲ])œ', '\\1е'), ('œ', 'о'),
   ('ʲ', '')]

_prettify_replaces_c: List[Tuple[Pattern, str]]
_prettify_replaces_c = [(re.compile(p), r) for p, r in _prettify_replaces]

_prettify_yat_replaces: Dict[str, List[Tuple[str, str]]] = {
   "e": [('ꙓ', 'е'), ('ѣ', 'е')],
   "je": [
      (f'ѣ({c.straight}?о)', 'и\\1'),
      ('лѣ', 'ље'), ('нѣ', 'ње'),
      (f'ѣ({c.straight}?[љјњ])', 'и\\1'),
      (f'ꙓ({c.straight}?[ој])', "и\\1"),
      (f'ꙓ{c.macron}', f'йје{c.macron}'),
      ('лꙓ', 'ље'), ('нꙓ', 'ње'),
      ('([бгджзкпстфхцчш]р)ꙓ', '\\1е'),
      ('[ꙓѣ]', 'је')] }
_prettify_yat_replaces["ije"] = _prettify_yat_replaces["je"]

_prettify_yat_replaces_c: Dict[str, List[Tuple[Pattern, str]]] = {
   k: [(re.compile(p), r) for p, r in v]
   for k, v in _prettify_yat_replaces.items()
}

_prettify_big_palatalization: List[Tuple[str, str]] = [
   ("(ст|шт|ск)ȷ", "шт"), ("(зд|жд|зг)ȷ", "жд"),
   #('слȷ', 'шљ'), ('злȷ', 'жљ'),
   # back into regular string replaces, see `_prettify_simple_palatalization`
   ('т?кʹ', 'ц'), #('гʹ', 'з'), ('хʹ', 'с'),
   ('с[кц]¦?ʺе', 'шче'),
   ('[кц]¦?ʺе', 'че') #, ('гʺ', 'ж'), ('хʺ', 'ш')
]

_prettify_big_palatalization_c: List[Tuple[Pattern, str]] = [
   (re.compile(p), r) for p, r in _prettify_big_palatalization
]

_prettify_simple_palatalization: List[Tuple[str, str]] = [
   ('слȷ', 'шљ'), ('злȷ', 'жљ'),
   ('гʹ', 'з'), ('хʹ', 'с'),
   ('гʺ', 'ж'), ('хʺ', 'ш'),
   ('тȷ', 'ћ'), ('дȷ', 'ђ'),
   ('лȷ', 'љ'), ('нȷ', 'њ')
]

_prettify_small_palatalization: List[Tuple[str, str]] = [
   ("([бмвфп])ȷ", "\\1љ"),
   ("[кц]ȷ", "ч"),
   ("[хс]ȷ", "ш"),
   ("[гз]ȷ", "ж"),
   # back into regular string replaces, see `_prettify_simple_palatalization`
   #('тȷ', 'ћ'), ('дȷ', 'ђ'),
   #('лȷ', 'љ'), ('нȷ', 'њ'),
   ('ц¦œ', 'це'),
   ('[ʹʺ¦ȷ]', '')
]

_prettify_small_palatalization_c: List[Tuple[Pattern, str]] = [
   (re.compile(p), r) for p, r in _prettify_small_palatalization
]

_prettify_yer_yot = (
   ('бĵ', 'бљ'), ('мĵ', 'мљ'), ('вĵ', 'вљ'), ('фĵ', 'фљ'), ('пĵ', 'пљ'),
   ('стĵ', 'шћ'), ('здĵ', 'жђ'), ('слĵ', 'шљ'), ('злĵ', 'жљ'),
   ('штĵ', 'шћ'), ('ждĵ', 'жђ'), ('скĵ', 'шт'), ('згĵ', 'жд'),
   ('кĵ', 'чј'), ('цĵ', 'чј'), ('хĵ', 'шј'), ('гĵ', 'жј'),
   ('тĵ', 'ћ'), ('дĵ', 'ђ'), ('ћĵ', 'ћ'), ('ђĵ', 'ђ'),
   ('лĵ', 'љ'),('нĵ', 'њ'), ('јĵ', 'ј'), ('ĵ', 'ј')
)

def prettify(text:str, yat:str="e") -> str:
   other_repl_modes = (
      _prettify_small_palatalization_c,
      _prettify_replaces_c,
      _prettify_yat_replaces_c[yat]
   )

   for entity in _prettify_big_palatalization_c:
      text = entity[0].sub(entity[1], text)

   for old, new in _prettify_simple_palatalization:
      text = text.replace(old, new)

   for repl_mode in other_repl_modes:
      for entity in repl_mode:
         text = entity[0].sub(entity[1], text)

   for old, new in _prettify_yer_yot:
      text = text.replace(old, new)

   return text

_deaccentize_accented: Dict[str, str] = {
   'ȁȃâáàā': 'a', 'ȅȇêéèē': 'e', 'ȉȋîíìīĭ': 'i',
   'ȕȗûúùū': 'u', 'ȑȓŕ': 'r', 'ȀȂÂÁÀĀ': 'A',
   'ȄȆÊÉÈĒ': 'E', 'ȈȊÎÍÌĪĬ': 'I', 'ȔȖÛÚÙŪ': 'U',
   'ȐȒŔ': 'R', 'ȍȏôóòō': 'o', 'ȌȎÔÓÒŌ': 'O',
   'ӣѝй': 'и', 'ѐ': 'е', 'ӢЍЙ': 'И', 'Ѐ': 'Е'}

_deaccentize_translator = str.maketrans(dict(chain(
   ((acc, deacc) for accs, deacc in _deaccentize_accented.items()
                 for acc in accs),
   ((mark, None) for mark in c.items()),
   ((mark, None) for mark in '`´_°¨^!') #TODO move this string somewhere
)))

def deaccentize(text:str) -> str:
   return text.translate(_deaccentize_translator)

_garde_four_accents_c: Pattern = re.compile(any_of_four_accents)
_garde_translator = str.maketrans({
   c.doublegrave: c.straight,
   c.circumflex: f'{c.macron}{c.straight}'
})

def garde(word: str) -> str: # Garde's accentuation
   result = word
   accents_re = _garde_four_accents_c
   while accents_re.findall(result): # while word is ungarded-like:

      short_desc_index = result.rfind(c.doublegrave)
      long_desc_index = result.rfind(c.circumflex)
      real_fvi = first_vowel_index(result)
      fvi = real_fvi if real_fvi is not None else -100

      # if not 'there is a falling accent and it is not of the first syllable'
      # then the word is garded the usual way
      if (
         short_desc_index in (fvi + 1, -1) and
         long_desc_index in (fvi + 1, -1)
      ):
         word2 = result
         insert_bool = False
         insert_dict = {}
         # which means: for each letter, if the letter is a vowel, we take the next symbol,
         # change it to '•' and insert a straight accent afther the next vowel;
         # not sure how it works on 2 consecutive accents,
         # so if you know such a word please tell us
         for i, letter in enumerate(word2):

            if letter in all_vowels:
               if insert_bool:
                  insert_dict[i+1] = c.straight
                  insert_bool = False
               else:
                  if len(result) > i+1:
                     # TODO: May benefit from precompiling regexes
                     # (or from remaking the transformation in other terms?)
                     if result[i+1] == c.grave:
                        insert_bool = True
                        word2 = re.sub("^(.{" + str(i+1) + "}).", r"\g<1>" + '•', word2)
                     elif result[i+1] == c.acute:
                        insert_bool = True
                        word2 = re.sub("^(.{" + str(i+1) + "}).", r"\g<1>" + c.macron, word2)
                     elif result[i+1] == c.doublegrave:
                        word2 = re.sub("^(.{" + str(i+1) + "}).",
                                       r"\g<1>" + c.straight,
                                       word2)
                     elif result[i+1] == c.circumflex:
                        word2 = re.sub("^(.{" + str(i+1) + "}).",
                                       r"\g<1>" + c.straight,
                                       word2)
                        insert_dict[i+1] = c.macron

         word3 = insert(word2, insert_dict)
         word3 = swap(word3.replace('•', ''), c.straight, c.macron)
         result = word3

      else:
         excl_index = max(short_desc_index, long_desc_index)
         result = insert(result, {excl_index-1: '!'})
         result = result.translate(_garde_translator)
   return result

_zeroify_translator = str.maketrans({
   '0': None,
   c.straight: None,
   '~': c.macron
})

def zeroify(form:str) -> str:
   if '0̍' in form: # 0 means accent on the firstmost syllable
      form = form.translate(_zeroify_translator)
      fvi = first_vowel_index(form)
      if fvi is None:
         raise ValueError(f"{form} does not contain any vowels")
      else:
         to_insert = fvi + 1
         form = insert(form, {to_insert: c.straight})
   return form

_purify_translator = str.maketrans('', '', '~0·')

def purify(form:str) -> str:
   return swap(form.translate(_purify_translator), c.straight, c.macron)

def ungarde(form:str) -> str:
   chars = list(form) # splitting string into characters
   while c.straight in chars:
      old_accent_index = chars.index(c.straight)
      chars.pop(old_accent_index)

      new_accent_index = old_accent_index - 1
      vowel_count = 0
      shifted = False
      while new_accent_index >= 0:
         if chars[new_accent_index] == "!":
            chars.pop(new_accent_index)
            old_accent_index -= 1
            break
         if chars[new_accent_index] in all_vowels:
            vowel_count += 1
            if vowel_count == 2:
               shifted = True
               new_accent_index += 1
               break
         new_accent_index -= 1

      if shifted:
         chars.insert(new_accent_index, c.grave) #rising
      elif old_accent_index == 0:
         chars.insert(1, c.doublegrave) #falling
      else:
         chars.insert(old_accent_index, c.doublegrave) #falling

   return ("".join(chars)
             .replace(f'{c.grave}{c.macron}', c.acute) #long rising
             .replace(f'{c.macron}{c.doublegrave}', c.circumflex)
             .replace(f'{c.doublegrave}{c.macron}', c.circumflex) #long falling
             .replace('!', '') # for cases where ! is not
   )                           # right before the accented syllable

def debracketify(form:str) -> str:
      if '>' in form:
         barrier = form.find('>')
         first_piece = form[:barrier]
         first_piece = first_piece.replace(c.macron, '')
         second_piece = form[barrier:].replace('>', '')
         form = first_piece + second_piece
      return form

def je2ije(form:str) -> str:
   return (form.replace(f'йје{c.acute}', f'ије{c.grave}')
               .replace(f'йје{c.circumflex}', f'и{c.doublegrave}је')
               .replace(f'йје{c.macron}', 'ије')
   )

deancientify_dict = {
   'тˌт': 'ст', 'дˌт': 'ст', 'зˌт': 'ст', 'кˌт': 'ћ', 'гˌт': 'ћ', 'бˌт': 'пст',
   'тˌꚜʌ': 'ʌ', 'дˌꚜʌ': 'ʌ', 'тˌʌ': 'ʌ', 'дˌʌ': 'ʌ', 'ˌ': ''
}

def deancientify(form:str) -> str:
   for key, value in deancientify_dict.items():
      form = form.replace(key, value)
   return form


_T = TypeVar('_T')

_Transform = Callable[..., _T] # this is too liberal but at least works nice

_ComposeArg = Union[
   Callable[[_T], _T],
   Tuple[_Transform[_T], Sequence[str]]
]

# TODO: A function of such generality (and maybe others like it) may need a module of its own,
# like `fun_utils` or `gen_utils` outside `lookup`
def compose1(*functions: _ComposeArg[_T]) -> _Transform[_T]:
   """Composes a sequence of functions T -> T.

      `compose1(f, g, h)(x) == f(g(h(x)))`

      If kwargs are given, they can be supplied to these functions by
      specifying which ones to give:

      `compose1(f, (g, ('a')), h)(x, a=1, b=2) = f(g(h(x), a=1))`"""
   def composition(arg, **kwargs):
      for f in reversed(functions):
         if isinstance(f, tuple):
            f, kws = f
            arg = f(arg, **{kw: kwargs[kw] for kw in kws})
         else:
            arg = f(arg)
      return arg
   return composition


def apply_yat_and_latin(form: str, yat: str, latin: bool) -> str:
   if yat == "ije":
      form = je2ije(form)
   if latin:
      form = cyr2lat(form)
   return form

expose_transform: _Transform[str] = compose1(
   (apply_yat_and_latin, ('yat', 'latin')), # fails somehow
   ungarde,
   (prettify, ('yat',)),
   purify,
   zeroify,
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
   for k, v in _prettify_yat_replaces_c[yat]:
      form = k.sub(v, form)
   for q, w in real_accent.items():
      form = form.replace(q, w)
   return apply_yat_and_latin(form, yat, latin)


def strip_suffix(value:str, suffixes:Iterable[str]) -> Tuple[str, bool]:
   """
   Tries to strip one of the given suffixes, iterating over them.
   If succesful, returns (stripped_value, True).
   Otherwise, returns (value, False).
   """
   for suffix in suffixes:
      if value.endswith(suffix):
         return value[:len(value) - len(suffix)], True
   return value, False
