from typing import Dict, Iterator
import random
import os
import re
import yaml
from paradigms import GramInfo, Accents, MP_to_stems
from auxiliary_data import palatalization_modes

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '\\a_sr_ru.yaml', encoding="utf-8") as f:
   data = yaml.load(f)
   letter_a = data['letter_a'][0]

# TODO: ungarde(word), e.g. асимилӣ̍ра̄м -> асимѝлӣра̄м
# ----- well-named function for recessive accent,
#       e.g. recessive(sequence) -> se̍quence
# ----- reflexive verbs like а́чити се
# ----- think of better name for prettify(), like alternate() or assimilate()

def last_vowel_index(trunk: str) -> int:
   *__, last_vowel = re.finditer('[АаЕеИиОоУуAaEeIiOoUu̥]', trunk)
   index, _ = last_vowel.span()
   return index

def first_vowel_index(trunk: str) -> int:
    return re.search('[АаЕеИиОоУуAaEeIiOoUu̥]', trunk).span()[0]

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

def decipher(infos, typ: str) -> GramInfo:

   if infos:
      line_accents, AP, MP = infos.split('|')
      Rs = line_accents.split('@')[0] if '@' in infos else None
      Vs = line_accents.split('@')[1] if '@' in infos else line_accents
      accents = Accents(
          {int(i): '\u0325' for i in Rs[1:].split(',')} if Rs else {},
          {int(i[:-1]): i[-1] for i in Vs.split(',')} if line_accents else {}
      )
   else:
      accents, AP, MP = Accents({}, {}), "", ""

   if typ:
      splitted_typ = typ.split('|')
      POS = splitted_typ[0]
      other = splitted_typ[1:]

   return GramInfo(accents, AP, MP, POS, other)

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
   word3 = re.sub('̍\u0304', '\u0304̍', word3) # swap length (\u0304) and accent (\u030d)

   return word3

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
   text = text.replace('јй', '̄ј')
   text = text.replace('й', 'и')
   return text

def conjugate(verb: str, info: GramInfo) -> Iterator[str]:
   accented_verb = garde(accentize(verb, info.accents))
   infinitive_dict = {'alpha': 'ити', 'beta': 'ати', 'gamma': 'нути',
                      'delta': 'ати', 'epsilon': 'овати', 'zeta': 'ивати',
                      'eta': 'ети', 'theta': 'ети', 'iota': 'ати',
                      'kappa': 'ти', 'lambda': 'ти', 'mu': 'ати'}
   if info.MP in infinitive_dict:
      verb_forms = []
      if info.AP == 'a': # There are 2 major types of paradigms: 'a' and the rest
         trunk = accented_verb[:-len(infinitive_dict[info.MP])]
         for stem in MP_to_stems[info.MP]:
            for ending in stem: # type: ignore
               verb_form = trunk
               for ending_part in ending:
                  if info.AP in ending_part.accent:
                     verb_form.replace('̍', '')
                     current_morph = ending_part.morpheme.replace('·', '̍')
                  else:
                     current_morph = ending_part.morpheme
                  verb_form += current_morph
               verb_forms.append(verb_form)

      else:
         if info.MP == 'kappa' or info.MP == 'lambda':
            trunk = accented_verb[:-len(infinitive_dict[info.MP])]
         else:
            trunk = accented_verb[:-len(infinitive_dict[info.MP])-1]
         to_insert = last_vowel_index(trunk) + 1
         trunk = insert(trunk, {to_insert: '·'})
         for stem in MP_to_stems[info.MP]:
            for ending in stem: # type: ignore
               verb_form = trunk
               #accentedness = False
               for ending_part in ending:
                  if info.AP in ending_part.accent:
                     current_morph = ending_part.morpheme.replace('·', '̍')
                     #print('accented: ', current_morph)
                     #accentedness = True
                  else:
                     current_morph = ending_part.morpheme
                  verb_form += current_morph
               if '̍' not in verb_form:
                  verb_form = verb_form.replace('·', '̍', 1)
               verb_forms.append(verb_form)

      for form in verb_forms:
         if '0̍' in form: # 0 means accent on the firstmost syllable
            form = form.replace('0', '')
            form = form.replace('̍', '')
            form = form.replace('~', '\u0304')
            to_insert = first_vowel_index(form) + 1
            form = insert(form, {to_insert: '̍'})
         form = form.replace('̍\u0304', '\u0304̍')
         form = form.replace('~', '')
         form = form.replace('0', '')
         form = form.replace('·', '')
         form = prettify(form)
         if 'Refl' in info.other:
            form = form + ' се'
         yield form

def lookup(raw_word: str) -> Iterator[Iterator[str]]:
   # TODO: lookup by partial keys in a dict? Really?
   # We ought to rethink the way we store data
   with_se = raw_word[-3:] == " се"
   if with_se:
      raw_word = raw_word[:-3]
   hits = []
   for key in letter_a.keys():
      key_without_disambiguator = key.split()[0]
      if raw_word == key_without_disambiguator:
         hits.append(key)

   for hit in hits:
      if 'i' in letter_a[hit]:
         verb, info = letter_a[hit]['i'], letter_a[hit]['t']
         if with_se and not 'Refl' in info:
            continue
         deciphered = decipher(verb, info)
         accented_word = accentize(hit, deciphered.accents)
         yield conjugate(hit, deciphered)
      elif with_se: # for skipping meaningless queries like "адвокат се"
         continue
      else:
         yield iter(["Ово није глагол 😞"]) # TODO

def random_word() -> Iterator[Iterator[str]]:
   while True:
      raw_word = random.choice(list(letter_a.keys()))
      if 'i' in letter_a[raw_word]:
         yield from lookup(raw_word)
         break

if __name__ == '__main__':
   for form in random_word():
      print(form)
