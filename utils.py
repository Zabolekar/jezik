# TODO:
# ----- well-named function for recessive accent,
#       e.g. recessive(sequence) -> se̍quence
# ----- think of better name for prettify(), like alternate() or assimilate()

import re
from typing import Dict, Optional, Iterator
from .auxiliary_data import palatalization_modes

all_vowels = "АаЕеИиОоУуЙйŒœꙒꙓѢѣAaEeIiOoUu\u0325"
any_vowel = f"[{all_vowels}]"

def last_vowel_index(trunk: str) -> Optional[int]:
   if re.search(any_vowel, trunk):
      *__, last_vowel = re.finditer(any_vowel, trunk)
      index, _ = last_vowel.span()
      return index
   else:
      return None

def first_vowel_index(trunk: str) -> Optional[int]:
   match = re.search(any_vowel, trunk)
   if match:
      return match.span()[0]
   else:
      return None

def insert(word: str, position_to_accent: Dict[int, str]) -> str:
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

def palatalize(sequence: str, mode: str='') -> str:
   idict = palatalization_modes[mode]
   digraphs = ['ст', 'зд', 'сл', 'зл', 'шт', 'жд']
   if sequence[-2:] in digraphs:
      return sequence[:-2] + idict[sequence[-2:]]

   return sequence[:-1] + idict[sequence[-1]]

def deyerify(form: str) -> str:
   if 'ø' in form:
      form = form.replace('ø', '').replace('ъ', 'а')
   else:
      form = form.replace('ъ', '')
   match = re.search('[бвгдђжзјклʌљмнљпрстфхцчџш]̍', form)
   if match:
      wrong_acc_index = match.span()[0]
      form = form.replace('̍', '')
      lvi = last_vowel_index(form[:wrong_acc_index])
      if lvi is None:
         raise ValueError(f"{form} does not contain any vowels")
      else:
         form = insert(form, {lvi+1: '̍'})
   return form
   
def prettify(text: str, yat:str='ekav') -> str:
   idict = palatalization_modes['ȷ']
   replaces = [ ('јй', '\u0304ј'), ('й', 'и'),
                ('̄̍ʌ', '̍ʌ'), ('̄ʌ', 'ʌ'), ('ʌ(а|е|и|о|у|р|œ|\u0325)', 'л\\1'), ('ʌ', 'о'),
                ('([чџњљћђшжј])œ', '\\1е'), ('œ', 'о')]
   yat_replaces = { 'ekav': [('ꙓ', 'е'), ('ѣ', 'е')],
                    'jekav': [('лѣ', 'ље'), ('нѣ', 'ње'),
                              ('[ѣꙓ]([ољјњ])', 'и\\1'), ('ꙓ̄', 'ӥје̄'),
                              ('([бгджзкпстфхцчш]р)ꙓ', '\\1е'), ('[ꙓѣ]', 'је')] }
   yat_replaces['ijekav'] = yat_replaces['jekav']
            
   for key in idict:
      text = text.replace(key, idict[key])
   for entity in replaces:
      text = re.sub(entity[0], entity[1], text)
   for entity in yat_replaces[yat]:
      text = re.sub(entity[0], entity[1], text)
   return text


   
def deaccentize(text: str) -> str:
   accents = '\u0301\u0300\u0304\u0306\u030f\u0311\u0302\u0325!'
   accented = {'ȁȃâáàā': 'a', 'ȅȇêéèē': 'e', 'ȉȋîíìī': 'i',
               'ȕȗûúùū': 'u', 'ȑȓŕ': 'r', 'ȀȂÂÁÀĀ': 'A',
               'ȄȆÊÉÈĒ': 'E', 'ȈȊÎÍÌĪ': 'I', 'ȔȖÛÚÙŪ': 'U',
               'ȐȒŔ': 'R', 'ȍȏôóòō': 'o', 'ȌȎÔÓÒŌ': 'O',
               'ӣѝ': 'и', 'ѐ': 'е', 'ӢЍ': 'И', 'Ѐ': 'Е'}
   for accent in accents:
      text = text.replace(accent, '')
   for letters in accented:
      for letter in letters:
         text = text.replace(letter, accented[letters])

   return text

def garde(word: str) -> str: # Garde's accentuation
   # TODO: check if there are non-initial ``s and ^s (пољопри̏вреда);
   # for now let us suppose there are none
   word2 = word
   insert_bool = False
   insert_dict = {}
   for i, letter in enumerate(word):
      # print('i, letter: ', i, ', ', letter)
      if letter in all_vowels:
         if insert_bool:
            insert_dict[i+1] = '\u030d' # straight accent
            insert_bool = False
         else:
            if len(word) > i+1:
               if word[i+1] == '\u0300': # `
                  insert_bool = True
                  word2 = re.sub("^(.{" + str(i+1) + "}).", r"\g<1>" + '•', word2)
               elif word[i+1] == '\u0301': # ´
                  insert_bool = True
                  word2 = re.sub("^(.{" + str(i+1) + "}).", r"\g<1>" + '\u0304', word2)
               elif word[i+1] == '\u030f': # ¨
                  word2 = re.sub("^(.{" + str(i+1) + "}).",
                                 r"\g<1>" + '\u030d',
                                 word2)  # straight accent
               elif word[i+1] == '\u0311': # ^
                  word2 = re.sub("^(.{" + str(i+1) + "}).",
                                 r"\g<1>" + '\u030d',
                                 word2) # straight accent
                  insert_dict[i+1] = '\u0304' # _

   word3 = insert(word2, insert_dict)
   word3 = re.sub('•', '', word3) # delete
   word3 = re.sub('\u030d\u0304', '\u0304\u030d', word3) # swap length (\u0304) and accent (\u030d)

   return word3

def zeroify(form: str) -> str:
   if '0̍' in form: # 0 means accent on the firstmost syllable
      form = (form
              .replace('0', '')
              .replace('\u030d', '') # straight accent
              .replace('~', '\u0304'))
      fvi = first_vowel_index(form)
      if fvi is None:
         raise ValueError(f"{form} does not contain any vowels")
      else:
         to_insert = fvi + 1
         form = insert(form, {to_insert: '\u030d'}) # straight accent
   return form
  
def purify(form: str) -> str:
   return (form.replace('~', '')
               .replace('0', '')
               .replace('·', '')
               .replace('\u030d\u0304', '\u0304\u030d')
           )
  
def expose(form: str) -> str:
   "all transformations from internal to external representation"
   return prettify(purify(zeroify(deyerify(form))))
   