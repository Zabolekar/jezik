# TODO: ungarde(word), e.g. асимилӣ̍ра̄м -> асимѝлӣра̄м
# ----- well-named function for recessive accent,
#       e.g. recessive(sequence) -> se̍quence
# ----- think of better name for prettify(), like alternate() or assimilate()

from typing import Dict
import re
from paradigms import Accents
from auxiliary_data import palatalization_modes

def insert(word: str, position_to_accent: Dict[int, str]) -> str:

   sorted_keys = sorted(position_to_accent.keys())
   first = [0] + sorted_keys
   second = sorted_keys + [None]
   pieces = [word[first[0]:second[0]]]

   for y in range(1, len(first)):
      pieces.append(position_to_accent[sorted_keys[y-1]])
      pieces.append(word[first[y]:second[y]])

   return ''.join(pieces)

def accentize(word: str, accents: Accents) -> str: # traditional accentuation
   real_accent = {'`': '\u0300', '´': '\u0301', '¨': '\u030f', '^': '\u0311', '_': '\u0304'}
   #accents = decipher(sequence).accents, TODO: discuss with sveto
   if accents.v:
      if accents.r: # now we put the magic ring
         word = insert(word, accents.r)
      # after that we create a dict with letter numbers representing vowels
      syllabic = 0
      position_to_accent = {} # type: Dict[int, str]
      for i, letter in enumerate(word):
         if letter in 'aeiouAEIOUаеиоуАЕИОУ\u0325':
            syllabic += 1
            if syllabic in accents.v:
               position_to_accent[i+1] = real_accent[accents.v[syllabic]]
      return insert(word, position_to_accent) # then we insert accents into word!
   else:
      return word

def palatalize(sequence: str, mode='') -> str:
   idict = palatalization_modes[mode]
   digraphs = ['ст', 'зд', 'сл', 'зл', 'шт', 'жд']
   if sequence[-2:] in digraphs:
      return sequence[:-2] + idict[sequence[-2:]]

   return sequence[:-1] + idict[sequence[-1]]

def prettify(text: str) -> str:
   idict = palatalization_modes['ȷ']
   for key in idict:
      text = text.replace(key, idict[key])
   return text.replace('јй', '\u0304ј').replace('й', 'и')

def deaccentize(text: str) -> str:
   accents = '\u0301\u0300\u0304\u0306\u030f\u0311\u0302\u0325'
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
      if letter in 'aeiouAEIOUаеиоуАЕИОУ\u0325':
         if insert_bool:
            insert_dict[i+1] = '\u030d' # straight accent
            insert_bool = False
         else:
            if len(word) > i+1:
               if word[i+1] in '\u0300': # `
                  insert_bool = True
                  word2 = re.sub("^(.{" + str(i+1) + "}).", r"\g<1>" + '•', word2)
               elif word[i+1] in '\u0301': # ´
                  insert_bool = True
                  word2 = re.sub("^(.{" + str(i+1) + "}).", r"\g<1>" + '\u0304', word2)
               elif word[i+1] in '\u030f': # ¨
                  word2 = re.sub("^(.{" + str(i+1) + "}).",
                                 r"\g<1>" + '\u030d',
                                 word2)  # straight accent
               elif word[i+1] in '\u0311': # ^
                  word2 = re.sub("^(.{" + str(i+1) + "}).",
                                 r"\g<1>" + '\u030d',
                                 word2) # straight accent
                  insert_dict[i+1] = '\u0304' # _

   word3 = insert(word2, insert_dict)
   word3 = re.sub('•', '', word3) # delete
   word3 = re.sub('\u030d\u0304', '\u0304\u030d', word3) # swap length (\u0304) and accent (\u030d)

   return word3
