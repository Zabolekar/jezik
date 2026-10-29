import re
from typing import Pattern
from . import characters as c
from .text_utils import insert, last_vowel_index

# Naming of things added for optimization purposes:
#   <name>_c − <name> but with compiled regexes
#   <name>_translator — a translation table used by `str.translate`
#   _<funcname>_<name> — a thing used by function `funcname`

# Not used yet; needed for e.g. passive participles and verbal nouns
# palatalization_modes: dict[str, dict[str, str]] = {
#    'и': {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
#          'ст': 'шт', 'зд': 'жд', 'сл': 'шљ', 'зл': 'жљ',
#          'шт': 'шт', 'жд': 'жд', 'ск': 'шт', 'зг': 'жд',
#          'к': 'к', 'ц': 'ч', 'х': 'х', 'г': 'г',
#          'ш': 'ш', 'ж': 'ж', 'ч': 'ч', 'џ': 'џ',
#          'т': 'ћ', 'д': 'ђ', 'с': 'ш', 'з': 'ж',
#          'л': 'љ', 'р': 'р', 'н': 'њ', 'ј': 'ј'},
#    '': {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
#         'ст': 'шћ', 'зд': 'жђ', 'сл': 'шљ', 'зл': 'жљ',
#         'шт': 'шћ', 'жд': 'жђ', 'ск': 'шт', 'зг': 'жд',
#         'к': 'ч', 'ц': 'ч', 'х': 'ш', 'г': 'ж',
#         'ш': 'ш', 'ж': 'ж', 'ч': 'ч', 'џ': 'џ',
#         'т': 'ћ', 'д': 'ђ', 'с': 'ш', 'з': 'ж',
#         'л': 'љ', 'р': 'р', 'н': 'њ', 'ј': 'ј'}
# }

# def palatalize(sequence:str, mode: str='') -> str:
#    idict = palatalization_modes[mode]
#    digraphs = ['ст', 'зд', 'сл', 'зл', 'шт', 'жд', 'ск', 'зг']
#    if sequence[-2:] in digraphs:
#       return sequence[:-2] + idict[sequence[-2:]]
#
#    return sequence[:-1] + idict[sequence[-1]]

_deyerify_repl_dict: dict[str, str] = {
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

# vowel + sonorant + yer: the vowel is lengthened when the yer is lost,
# e.g. ва¨рък -> ва̄рк
_lengthen_before_sonorant_yer_c: Pattern = re.compile(f'([аеиоу{c.ring}][{c.straight}·]?)([лљмнњрјв]ʲ?)ъ')
# accent mark right after a consonant, e.g. авио̄н̍ (it comes from an accented
# zero ending); deyerify() moves it back to the preceding vowel
_stranded_accent_c: Pattern = re.compile(f'[бвгдђжзјклʌљмнњпрṕсćтћфхцчџш]ʲ?{c.straight}')

_deyerify_translator = str.maketrans({
   'ø': None,
   'ъ': 'а',
   'ꚜ': 'а',
   'ꙏ': 'а'
})

_decurlyerify_repl_dict: dict[str, str] = {
   k.replace('ъ', 'ꙏ') : v for k,v  in _deyerify_repl_dict.items()
}

def decurlyerify(form:str) -> str:
   for k, v in _decurlyerify_repl_dict.items():
      form = form.replace(k, v)
   return re.sub('([лљмнњрјв]ꙏ)', f'{c.macron}\\1', form).replace('ꙏ', '')

def deyerify(form:str) -> str:
   repl_dict = _deyerify_repl_dict

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
      form = _lengthen_before_sonorant_yer_c.sub(f'\\1{c.macron}\\2ъ', form)
      for k, v in repl_dict.items():
         form = form.replace(k, v)
      form = form.replace('ъ', '').replace('ꚜ', '').replace('ꙏ', '')

   match = _stranded_accent_c.search(form)
   if match:
      wrong_acc_index = match.span()[0]
      form = form.replace(c.straight, '')
      lvi = last_vowel_index(form[:wrong_acc_index+2])
      if lvi is None:
         raise ValueError(f"_{form[:wrong_acc_index+2]}_ does not contain any vowels")
      else:
         form = insert(form, {lvi+1: c.straight})
   return form

_assimilate_replaces: list[tuple[str, str]] = [
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

_assimilate_replaces_c: list[tuple[Pattern, str]]
_assimilate_replaces_c = [(re.compile(p), r) for p, r in _assimilate_replaces]

_assimilate_yat_replaces: dict[str, list[tuple[str, str]]] = {
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
_assimilate_yat_replaces["ije"] = _assimilate_yat_replaces["je"]

_assimilate_yat_replaces_c: dict[str, list[tuple[Pattern, str]]] = {
   k: [(re.compile(p), r) for p, r in v]
   for k, v in _assimilate_yat_replaces.items()
}

_assimilate_big_palatalization: list[tuple[str, str]] = [
   ("(ст|шт|ск)ȷ", "шт"), ("(зд|жд|зг)ȷ", "жд"),
   #('слȷ', 'шљ'), ('злȷ', 'жљ'),
   # back into regular string replaces, see `_assimilate_simple_palatalization`
   ('т?кʹ', 'ц'), #('гʹ', 'з'), ('хʹ', 'с'),
   ('с[кц]¦?ʺе', 'шче'),
   ('[кц]¦?ʺе', 'че') #, ('гʺ', 'ж'), ('хʺ', 'ш')
]

_assimilate_big_palatalization_c: list[tuple[Pattern, str]] = [
   (re.compile(p), r) for p, r in _assimilate_big_palatalization
]

_assimilate_simple_palatalization: list[tuple[str, str]] = [
   ('слȷ', 'шљ'), ('злȷ', 'жљ'),
   ('гʹ', 'з'), ('хʹ', 'с'),
   ('гʺ', 'ж'), ('хʺ', 'ш'),
   ('тȷ', 'ћ'), ('дȷ', 'ђ'),
   ('лȷ', 'љ'), ('нȷ', 'њ')
]

_assimilate_small_palatalization: list[tuple[str, str]] = [
   ("([бмвфп])ȷ", "\\1љ"),
   ("[кц]ȷ", "ч"),
   ("[хс]ȷ", "ш"),
   ("[гз]ȷ", "ж"),
   # back into regular string replaces, see `_assimilate_simple_palatalization`
   #('тȷ', 'ћ'), ('дȷ', 'ђ'),
   #('лȷ', 'љ'), ('нȷ', 'њ'),
   ('ц¦œ', 'це'),
   ('[ʹʺ¦ȷ]', '')
]

_assimilate_small_palatalization_c: list[tuple[Pattern, str]] = [
   (re.compile(p), r) for p, r in _assimilate_small_palatalization
]

_assimilate_yer_yot = (
   ('бĵ', 'бљ'), ('мĵ', 'мљ'), ('вĵ', 'вљ'), ('фĵ', 'фљ'), ('пĵ', 'пљ'),
   ('стĵ', 'шћ'), ('здĵ', 'жђ'), ('слĵ', 'шљ'), ('злĵ', 'жљ'),
   ('штĵ', 'шћ'), ('ждĵ', 'жђ'), ('скĵ', 'шт'), ('згĵ', 'жд'),
   ('кĵ', 'чј'), ('цĵ', 'чј'), ('хĵ', 'шј'), ('гĵ', 'жј'),
   ('тĵ', 'ћ'), ('дĵ', 'ђ'), ('ћĵ', 'ћ'), ('ђĵ', 'ђ'),
   ('лĵ', 'љ'),('нĵ', 'њ'), ('јĵ', 'ј'), ('ĵ', 'ј')
)

def assimilate(text:str, yat:str="e") -> str:
   other_repl_modes = (
      _assimilate_small_palatalization_c,
      _assimilate_replaces_c,
      _assimilate_yat_replaces_c[yat]
   )

   for entity in _assimilate_big_palatalization_c:
      text = entity[0].sub(entity[1], text)

   for old, new in _assimilate_simple_palatalization:
      text = text.replace(old, new)

   for repl_mode in other_repl_modes:
      for entity in repl_mode:
         text = entity[0].sub(entity[1], text)

   for old, new in _assimilate_yer_yot:
      text = text.replace(old, new)

   return text

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
