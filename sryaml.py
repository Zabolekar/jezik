from typing import Dict, NamedTuple
import random
import re
import yaml

class Accents(NamedTuple):
   r: Dict[int, str]
   v: Dict[int, str]
   
class GramInfo(NamedTuple):
   accents: Accents
   AP: str # accent paradigm
   MP: str # morphological paradigm

def deaccentize(text: str) -> str:
   accents = '̥́̀̄̆̏̑'
   accented = {'ȁȃáàā': 'a', 'ȅȇéèē': 'e', 'ȉȋíìī': 'i',
               'ȕȗúùū': 'u', 'ȑȓŕ': 'r', 'ȀȂÁÀĀ': 'A',
               'ȄȆÉÈĒ': 'E', 'ȈȊÍÌĪ': 'I', 'ȔȖÚÙŪ': 'U',
               'ȐȒŔ': 'R', 'ӣѝ': 'и', 'ѐ': 'е',
               'ӢЍ': 'И', 'Ѐ': 'Е'}
   for accent in accents:
      text = text.replace(accent, '')
   for letters in accented:
      for letter in letters:
         text = text.replace(letter, accented[letters])

   return text

def decipher(sequence: str) -> GramInfo:

   if sequence:
      begin_R = re.search('@', sequence).start(0) if '@' in sequence else None
      begin_AP = re.search('[A-Z]', sequence).start(0)
      begin_MP = re.search('[a-z]', sequence).start(0)
      line_accents = sequence[:begin_R] if '@' in sequence else sequence[:begin_AP]
      Rs = sequence[begin_R:begin_AP] if '@' in sequence else None
      accents = Accents(
          {int(i): '̥' for i in Rs[1:].split(',')} if Rs else {},
          {int(i[:-1]): i[-1] for i in line_accents.split(',')} if line_accents else {}
      )
      AP = sequence[begin_AP:begin_MP]
      MP = sequence[begin_MP:]
   else:
      accents, AP, MP = (Accents({}, {}), "", "")

   return GramInfo(accents, AP, MP)

def insert(word: str, dict_: Dict[int, str]) -> str:

   list_ = sorted(dict_.keys())
   first = [0] + list_
   second = list_ + [None]
   pieces = [word[first[0]:second[0]]]

   for y in range(1, len(first)):
      pieces.append(dict_[list_[y-1]])
      pieces.append(word[first[y]:second[y]])

   return ''.join(pieces)

def accentize(word: str, sequence: str) -> str:
   real_accent = {'`': '̀', '´': '́', '¨': '̏', '^': '̑', '_': '̄'}
   acc_dict = decipher(sequence).accents
   if acc_dict.v:
      if acc_dict.r: # now we put the magic ring
         word = insert(word, acc_dict.r)
      # after that we create a dict with letter numbers representing vowels
      syllabic = 0
      vow_dict: Dict[int, str] = {}
      for i, letter in enumerate(word):
         if letter in 'aeiouAEIOUаеиоуАЕИОУ̥':
            syllabic += 1
            if syllabic in acc_dict.v:
               vow_dict[i+1] = real_accent[acc_dict.v[syllabic]]
      return insert(word, vow_dict) # then we insert accents into word!
   else:
      return word

if __name__ == '__main__':
   with open('a_sr_ru.yaml', encoding="utf-8") as f:
      data = yaml.load(f)
      letter_a = data['letter_a'][0]
      for raw_word in random.sample(letter_a.keys(), 10):
         accented_word = accentize(raw_word, letter_a[raw_word].get('i', ''))
         print('{:>25} : {}'.format(raw_word, accented_word))
