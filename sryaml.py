from typing import Dict, NamedTuple
import random
import re
import yaml

# workaround for Python 3.5 without new NamedTuple syntax
Accents = NamedTuple("Accents", [
   ("r", Dict[int, str]), # syllabic r
   ("v", Dict[int, str]) # any other vowel
])   
   
GramInfo = NamedTuple("Accents", [
   ("accents", Accents),
   ("AP", str), # accent paradigm
   ("MP", str) # morphological paradigm
])

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

def decipher(sequence: str) -> GramInfo:

   if sequence:
      begin_R = re.search('@', sequence).start(0) if '@' in sequence else None
      begin_AP = re.search('[A-Z]', sequence).start(0)
      begin_MP = re.search('[a-z]', sequence).start(0)
      line_accents = sequence[:begin_R] if '@' in sequence else sequence[:begin_AP]
      Rs = sequence[begin_R:begin_AP] if '@' in sequence else None
      accents = Accents(
          {int(i): '\u0325' for i in Rs[1:].split(',')} if Rs else {},
          {int(i[:-1]): i[-1] for i in line_accents.split(',')} if line_accents else {}
      )
      AP = sequence[begin_AP:begin_MP]
      MP = sequence[begin_MP:]
   else:
      accents, AP, MP = Accents({}, {}), "", ""

   return GramInfo(accents, AP, MP)

def insert(word: str, position_to_accent: Dict[int, str]) -> str:

   sorted_keys = sorted(position_to_accent.keys())
   first = [0] + sorted_keys
   second = sorted_keys + [None]
   pieces = [word[first[0]:second[0]]]

   for y in range(1, len(first)):
      pieces.append(position_to_accent[sorted_keys[y-1]])
      pieces.append(word[first[y]:second[y]])

   return ''.join(pieces)

def accentize(word: str, sequence: str) -> str:
   # we aim to remove all todos from our yaml file, but until then that's how we handle them
   if sequence == "todo":
      return "TODO"
   real_accent = {'`': '\u0300', '´': '\u0301', '¨': '\u030f', '^': '\u0311', '_': '\u0304'}
   accents = decipher(sequence).accents
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

def palatalize(sequence, mode = ''):
   if mode == 'и':
      idict = {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
            'ст': 'шћ', 'зд': 'жђ', 'сл': 'шљ', 'зл': 'жљ',
            'к': 'к', 'ц': 'ч', 'х': 'х', 'г': 'г',
            'ш': 'ш', 'ж': 'ж', 'ч': 'ч', 'џ': 'џ',
            'т': 'ћ', 'д': 'ђ', 'с': 'ш', 'з': 'ж',
            'л': 'љ', 'р': 'р', 'н': 'њ', 'ј': 'ј'}
   elif mode == 'ј':
      idict = {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
            'ст': 'шћ', 'зд': 'жђ', 'сл': 'шљ', 'зл': 'жљ',
            'к': 'чј', 'ц': 'чј', 'х': 'шј', 'г': 'жј',
            'ш': 'шј', 'ж': 'жј', 'ч': 'чј', 'џ': 'џј',
            'т': 'ћ', 'д': 'ђ', 'с': 'сј', 'з': 'зј',
            'л': 'љ', 'р': 'рј', 'н': 'њ', 'ј': 'ј'}
   else:
      idict = {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
            'ст': 'шћ', 'зд': 'жђ', 'сл': 'шљ', 'зл': 'жљ',
            'к': 'ч', 'ц': 'ч', 'х': 'ш', 'г': 'ж',
            'ш': 'ш', 'ж': 'ж', 'ч': 'ч', 'џ': 'џ',
            'т': 'ћ', 'д': 'ђ', 'с': 'ш', 'з': 'ж',
            'л': 'љ', 'р': 'р', 'н': 'њ', 'ј': 'ј'}
   
   if sequence.endswith('ст') or sequence.endswith('зд') or sequence.endswith('сл') or sequence.endswith('зл'):
      return sequence[:-2] + idict[sequence[-2:]]
   else:
      return sequence[:-1] + idict[sequence[-1]]

def prettify(text):
   text = re.sub('јй', '_ј', text)
   text = re.sub('й', 'и', text)
   return text
      
def conjugate(verb, AP, MP):
   prs_endings = {'и': ['и_м', 'и_ш', 'и_', 'и_мо', 'и_те', 'е_', 'й', 'ймо', 'йте'],
              'е': ['е_м', 'е_ш', 'е_', 'е_мо', 'е_те', 'у_', 'й', 'ймо', 'йте'],
              'а': ['а_м', 'а_ш', 'а_', 'а_мо', 'а_те', 'ају_', 'а_ј', 'а_јмо', 'а_јте']}
   inf_endings = ['ти', 'о', 'ла', 'ло', 'ли', 'ле', 'ла', 'х', '', '', 'смо', 'сте', 'ше']
   
   MP_dict = {'im': {'inf': verb[:-2], 'prs': (verb[:-3], 'и'), 'pp': (palatalize(verb[:-3], 'и'), 'е_н')},
              'am': {'inf': verb[:-2], 'prs': (verb[:-3], 'а'), 'pp': (verb[:-3], 'а_н')},
              'ujem': {'inf': verb[:-2], 'prs': (verb[:-5]+'уј', 'е'), 'pp': (verb[:-3], 'а_н')},
              'jem': {'inf': verb[:-2], 'prs': (palatalize(verb[:-3]), 'е'), 'pp': (verb[:-3], 'а_н')}
              }
   
   for ending in inf_endings:
      print(prettify(MP_dict[MP]['inf'] + ending))
   for ending in prs_endings[MP_dict[MP]['prs'][1]]:
      print (prettify(MP_dict[MP]['prs'][0] + ending))
      
   return None
      
if __name__ == '__main__':
   with open('a_sr_ru.yaml', encoding="utf-8") as f:
      data = yaml.load(f)
      letter_a = data['letter_a'][0]
      for raw_word in random.sample(letter_a.keys(), 10):
         if 'i' in letter_a[raw_word]:
            print('{:>25} : '.format(raw_word), end = "")
            accented_word = accentize(raw_word, letter_a[raw_word].get('i', ''))
            print(accented_word)
            conjugate(raw_word, None, decipher(letter_a[raw_word]['i']).MP)