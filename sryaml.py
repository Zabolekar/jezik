from typing import Dict, NamedTuple
import os
import random
import re
import yaml

# TODO: ungarde(word), e.g. асимилӣ̍ра̄м -> асимѝлӣра̄м
# ----- well-named function for recessive accent,
#       e.g. recessive(sequence) -> se̍quence
# ----- reflexive verbs like а́чити се
# ----- think of better name for prettify(), like alternate() or assimilate()

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

AccentedTuple = NamedTuple("AccentedTuple", [
   ("morpheme", str),
   ("accent", str)
])

Ending = NamedTuple("Ending", [
   ("theme", AccentedTuple),
   ("ending", AccentedTuple)
])

Present = NamedTuple("Present", [
   ("prs1sg", Ending),
   ("prs2sg", Ending),
   ("prs3sg", Ending),
   ("prs1pl", Ending),
   ("prs2pl", Ending),
   ("prs3pl", Ending),
   ("imv2sg", Ending),
   ("imv1pl", Ending),
   ("imv2pl", Ending)
])

Past = NamedTuple("Past", [
   ("pfMsg", Ending),
   ("pfFsg", Ending),
   ("pfNsg", Ending),
   ("pfMpl", Ending),
   ("pfFpl", Ending),
   ("pfnNpl", Ending),
   ("aor1sg", Ending),
   ("aor2sg", Ending),
   ("aor3sg", Ending),
   ("aor1pl", Ending),
   ("aor2pl", Ending),
   ("aor3pl", Ending),
   ("infinitive", Ending),
   ("ipf1sg", Ending),
   ("ipf2sg", Ending),
   ("ipf3sg", Ending),
   ("ipf1pl", Ending),
   ("ipf2pl", Ending),
   ("ipf3pl", Ending)
])

"""Presents = NamedTuple("Presents", [
   ("i", Present),
   ("e", Present),
   ("a", Present),
   ("je", Present),
   ("ie", Present),
   ("uje", Present)
])

Pasts = NamedTuple("Pasts",[
   ("i", Past),
   ("a", Past),
   ("ie", Past),
   ("ova", Past),
   ("u", Past) # add "zero" after finishing the book!
])"""


Stems = NamedTuple("Stems", [
   ("present", Present),
   ("past", Past)
])

i_theme_past = AccentedTuple('и·', 'b.b:c.c:c#')
a_theme_past = AccentedTuple('а·~', 'b.b:c.c:c#cjx.y.y:y#z.')
ie_theme_past = AccentedTuple('е·', 'b.c.c:')
#zero_theme_past = AccentedTuple('', '')
#nu_theme_past = AccentedTuple('ну', '') # finish the book first!
ova_theme_past = AccentedTuple('ова·', 'cp')
iva_theme_past = AccentedTuple('и\u0304ва·', 'ct')

i_theme_ipf = AccentedTuple('ȷа\u0304·', 'c.c:c#')
ie_theme_ipf = AccentedTuple('ȷа\u0304·', 'c.c:')
a_theme_ipf = AccentedTuple('а\u0304·', 'c.cpc#y#')
ova_theme_ipf = AccentedTuple('о·ва\u0304', 'cp')
iva_theme_ipf = AccentedTuple('и\u0304·ва\u0304', 'ct')

ending_null = AccentedTuple('', '')
ending_x = AccentedTuple('х', '')
ending_she = AccentedTuple('ше', '')
ending_smo = AccentedTuple('смо', '')
ending_ste = AccentedTuple('сте', '')
ending_xu = AccentedTuple('ху', '')
ending_ti = AccentedTuple('ти', '')

i_past = Past(
   Ending(i_theme_past, AccentedTuple('о', '')),
   Ending(i_theme_past, AccentedTuple('ла', '')),
   Ending(i_theme_past, AccentedTuple('ло', '')),
   Ending(i_theme_past, AccentedTuple('ли', '')),
   Ending(i_theme_past, AccentedTuple('ле', '')),
   Ending(i_theme_past, AccentedTuple('ла', '')),
   Ending(i_theme_past, ending_x),
   Ending(AccentedTuple('и·', 'c#'), AccentedTuple('0·~', 'ab.b:c.c:')),
   Ending(AccentedTuple('и·', 'c#'), AccentedTuple('0·~', 'ab.b:c.c:')),
   Ending(i_theme_past, ending_smo),
   Ending(i_theme_past, ending_ste),
   Ending(i_theme_past, ending_she),
   Ending(i_theme_past, ending_ti),
   Ending(i_theme_ipf, ending_x),
   Ending(i_theme_ipf, ending_she),
   Ending(i_theme_ipf, ending_she),
   Ending(i_theme_ipf, ending_smo),
   Ending(i_theme_ipf, ending_ste),
   Ending(i_theme_ipf, ending_xu)
)

a_past = Past(
   Ending(a_theme_past, AccentedTuple('о0·', 'x.ct')),
   Ending(a_theme_past, AccentedTuple('ла0·', 'x.ct')),
   Ending(a_theme_past, AccentedTuple('ло0·', 'x.ct')),
   Ending(a_theme_past, AccentedTuple('ли0·', 'x.ct')),
   Ending(a_theme_past, AccentedTuple('ле0·', 'x.ct')),
   Ending(a_theme_past, AccentedTuple('ла0·', 'x.ct')),
   Ending(a_theme_past, ending_x),
   Ending(AccentedTuple('а', 'c#y:d.'), AccentedTuple('0·~', 'ax.z.b:c.ct')),
   Ending(AccentedTuple('а', 'c#y:d.'), AccentedTuple('0·~', 'ax.z.b:c.ct')),
   Ending(a_theme_past, ending_smo),
   Ending(a_theme_past, ending_ste),
   Ending(a_theme_past, ending_she),
   Ending(a_theme_past, ending_ti),
   Ending(a_theme_ipf, ending_x),
   Ending(a_theme_ipf, ending_she),
   Ending(a_theme_ipf, ending_she),
   Ending(a_theme_ipf, ending_smo),
   Ending(a_theme_ipf, ending_smo),
   Ending(a_theme_ipf, ending_xu)
)

ie_past = Past(
   Ending(ie_theme_past, AccentedTuple('о', '')),
   Ending(ie_theme_past, AccentedTuple('ла', '')),
   Ending(ie_theme_past, AccentedTuple('ло', '')),
   Ending(ie_theme_past, AccentedTuple('ли', '')),
   Ending(ie_theme_past, AccentedTuple('ле', '')),
   Ending(ie_theme_past, AccentedTuple('ла', '')),
   Ending(ie_theme_past, ending_x),
   Ending(ie_theme_past, ending_null),
   Ending(ie_theme_past, ending_null),
   Ending(ie_theme_past, ending_smo),
   Ending(ie_theme_past, ending_ste),
   Ending(ie_theme_past, ending_she),
   Ending(ie_theme_past, ending_ti),
   Ending(ie_theme_ipf, ending_x),
   Ending(ie_theme_ipf, ending_she),
   Ending(ie_theme_ipf, ending_she),
   Ending(ie_theme_ipf, ending_smo),
   Ending(ie_theme_ipf, ending_ste),
   Ending(ie_theme_ipf, ending_xu)
)

ova_past = Past(
   Ending(AccentedTuple('ова~', ''), AccentedTuple('о0·', 'cp')),
   Ending(AccentedTuple('ова~', ''), AccentedTuple('ла0·', 'cp')),
   Ending(AccentedTuple('ова~', ''), AccentedTuple('ло0·', 'cp')),
   Ending(AccentedTuple('ова~', ''), AccentedTuple('ли0·', 'cp')),
   Ending(AccentedTuple('ова~', ''), AccentedTuple('ле0·', 'cp')),
   Ending(AccentedTuple('ова~', ''), AccentedTuple('ла0·', 'cp')),
   Ending(ova_theme_past, ending_x),
   Ending(AccentedTuple('ова', ''), AccentedTuple('0·~', 'acp')),
   Ending(AccentedTuple('ова', ''), AccentedTuple('0·~', 'acp')),
   Ending(ova_theme_past, ending_smo),
   Ending(ova_theme_past, ending_ste),
   Ending(ova_theme_past, ending_she),
   Ending(ova_theme_past, ending_ti),
   Ending(ova_theme_ipf, ending_x),
   Ending(ova_theme_ipf, ending_she),
   Ending(ova_theme_ipf, ending_she),
   Ending(ova_theme_ipf, ending_smo),
   Ending(ova_theme_ipf, ending_ste),
   Ending(ova_theme_ipf, ending_xu)
)

iva_past = Past(
   Ending(iva_theme_past, AccentedTuple('о', '')),
   Ending(iva_theme_past, AccentedTuple('ла', '')),
   Ending(iva_theme_past, AccentedTuple('ло', '')),
   Ending(iva_theme_past, AccentedTuple('ли', '')),
   Ending(iva_theme_past, AccentedTuple('ле', '')),
   Ending(iva_theme_past, AccentedTuple('ла', '')),
   Ending(iva_theme_past, ending_x),
   Ending(iva_theme_past, AccentedTuple('·', 'ct')),
   Ending(iva_theme_past, AccentedTuple('·', 'ct')),
   Ending(iva_theme_past, ending_smo),
   Ending(iva_theme_past, ending_ste),
   Ending(iva_theme_past, ending_she),
   Ending(iva_theme_past, ending_ti),
   Ending(iva_theme_ipf, ending_x),
   Ending(iva_theme_ipf, ending_she),
   Ending(iva_theme_ipf, ending_she),
   Ending(iva_theme_ipf, ending_smo),
   Ending(iva_theme_ipf, ending_ste),
   Ending(iva_theme_ipf, ending_xu)
)

#("e", Present),   — todo later
#("ie", Present), — todo later
#("ne", Present) — todo after finishing the book

i_theme_prs = AccentedTuple('и·\u0304', 'c.c:c#')
je_theme_prs = AccentedTuple('\u0237е·\u0304', 'y#')
a_theme_prs = AccentedTuple('а·\u0304', 'c.cpc#')
uje_theme_prs = AccentedTuple('у·је\u0304', 'cpct')

i_theme_imv = AccentedTuple('й·', 'b.b:c.c:c#')
je_theme_imv = AccentedTuple('\u0237й·', 'x.y.y#y:z.')
a_theme_imv = AccentedTuple('а·\u0304ј', 'с.cpc#')
uje_theme_imv = AccentedTuple('у·\u0304ј', 'cpct')

ending_mo = AccentedTuple('мо', '')
ending_te = AccentedTuple('те', '')
ending_m = AccentedTuple('м', '')
ending_sh = AccentedTuple('ш', '')

i_present = Present(
   Ending(i_theme_prs, ending_m),
   Ending(i_theme_prs, ending_sh),
   Ending(i_theme_prs, ending_null),
   Ending(AccentedTuple('и·̄', 'c.c:'), AccentedTuple('мо', 'c#')),
   Ending(AccentedTuple('и·̄', 'c.c:'), AccentedTuple('те', 'c#')),
   Ending(AccentedTuple('е·̄', 'c.c:c#'), ending_null),
   Ending(i_theme_imv, ending_null),
   Ending(i_theme_imv, ending_mo),
   Ending(i_theme_imv, ending_te)
)

je_present = Present(
   Ending(je_theme_prs, ending_m),
   Ending(je_theme_prs, ending_sh),
   Ending(je_theme_prs, ending_null),
   Ending(AccentedTuple('\u0237е·\u0304', ''), AccentedTuple('мо', 'y#')),
   Ending(AccentedTuple('\u0237е·\u0304', ''), AccentedTuple('те', 'y#')),
   Ending(AccentedTuple('у·\u0304', 'y#'), ending_null),
   Ending(je_theme_imv, ending_null),
   Ending(je_theme_imv, ending_mo),
   Ending(je_theme_imv, ending_te)
)

a_present = Present(
   Ending(a_theme_prs, ending_m),
   Ending(a_theme_prs, ending_sh),
   Ending(a_theme_prs, ending_null),
   Ending(AccentedTuple('а·\u0304', 'c.cp'), AccentedTuple('мо', 'c#')),
   Ending(AccentedTuple('а·\u0304', 'c.cp'), AccentedTuple('те', 'c#')),
   Ending(AccentedTuple('а·ју\u0304', 'b:d.с.c#cp'), ending_null),
   Ending(a_theme_imv, ending_null),
   Ending(a_theme_imv, ending_mo),
   Ending(a_theme_imv, ending_te)
)

uje_present = Present(
   Ending(uje_theme_prs, ending_m),
   Ending(uje_theme_prs, ending_sh),
   Ending(uje_theme_prs, ending_null),
   Ending(uje_theme_prs, ending_mo),
   Ending(uje_theme_prs, ending_te),
   Ending(AccentedTuple('у·ју\u0304', 'cpct'), ending_null),
   Ending(uje_theme_imv, ending_null),
   Ending(uje_theme_imv, ending_mo),
   Ending(uje_theme_imv, ending_te)
)

MP_to_stems = dict(
   alpha=Stems(i_present, i_past),
   beta=Stems(a_present, a_past),
   delta=Stems(je_present, a_past),
   epsilon=Stems(uje_present, ova_past),
   zeta=Stems(uje_present, iva_past),
   eta=Stems(i_present, ie_past),
) # type: Dict[str, Stems]

def last_vowel_index(trunk: str) -> int:
   *_, last_vowel = re.finditer('[АаЕеИиОоУуAaEeIiOoUu̥]', trunk)
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

def decipher(sequence: str) -> GramInfo:

   if sequence:
      line_accents, AP, MP = sequence.split('|')
      Rs = line_accents.split('@')[0] if '@' in sequence else None
      Vs = line_accents.split('@')[1] if '@' in sequence else line_accents
      accents = Accents(
          {int(i): '\u0325' for i in Rs[1:].split(',')} if Rs else {},
          {int(i[:-1]): i[-1] for i in Vs.split(',')} if line_accents else {}
      )
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
   # TODO: here add checking if there are non-initial ``s and ^s;
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

def palatalize(sequence, mode=''):
   if mode == 'и':
      idict = {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
               'ст': 'шт', 'зд': 'жд', 'сл': 'шљ', 'зл': 'жљ',
               'шт': 'шт', 'жд': 'жд',
               'к': 'к', 'ц': 'ч', 'х': 'х', 'г': 'г',
               'ш': 'ш', 'ж': 'ж', 'ч': 'ч', 'џ': 'џ',
               'т': 'ћ', 'д': 'ђ', 'с': 'ш', 'з': 'ж',
               'л': 'љ', 'р': 'р', 'н': 'њ', 'ј': 'ј'}
   elif mode == 'ĵ':
      idict = {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
               'ст': 'шћ', 'зд': 'жђ', 'сл': 'шљ', 'зл': 'жљ',
               'шт': 'шћ', 'жд': 'жђ',
               'к': 'чј', 'ц': 'чј', 'х': 'шј', 'г': 'жј',
               'ш': 'шј', 'ж': 'жј', 'ч': 'чј', 'џ': 'џј',
               'т': 'ћ', 'д': 'ђ', 'с': 'сј', 'з': 'зј',
               'л': 'љ', 'р': 'рј', 'н': 'њ', 'ј': 'ј'}
   else:
      idict = {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
               'ст': 'шћ', 'зд': 'жђ', 'сл': 'шљ', 'зл': 'жљ',
               'шт': 'шћ', 'жд': 'жђ',
               'к': 'ч', 'ц': 'ч', 'х': 'ш', 'г': 'ж',
               'ш': 'ш', 'ж': 'ж', 'ч': 'ч', 'џ': 'џ',
               'т': 'ћ', 'д': 'ђ', 'с': 'ш', 'з': 'ж',
               'л': 'љ', 'р': 'р', 'н': 'њ', 'ј': 'ј'}

   if sequence[-2:] in ['ст', 'зд', 'сл', 'зл', 'шт', 'жд']:
      return sequence[:-2] + idict[sequence[-2:]]

   return sequence[:-1] + idict[sequence[-1]]

def prettify(text):
   idict = {'бȷ': 'бљ', 'мȷ': 'мљ', 'вȷ': 'вљ', 'фȷ': 'фљ', 'пȷ': 'пљ',
            'стȷ': 'штȷ', 'здȷ': 'ждȷ', 'слȷ': 'шљ', 'злȷ': 'жљ',
            'штȷ': 'шт', 'ждȷ': 'жд',
            'кȷ': 'ч', 'цȷ': 'ч', 'хȷ': 'ш', 'гȷ': 'ж',
            'шȷ': 'ш', 'жȷ': 'ж', 'чȷ': 'ч', 'џȷ': 'џ',
            'тȷ': 'ћ', 'дȷ': 'ђ', 'сȷ': 'ш', 'зȷ': 'ж',
            'лȷ': 'љ', 'рȷ': 'р', 'нȷ': 'њ', 'јȷ': 'ј',
            'љȷ': 'љ', 'њȷ': 'њ'}
   for key in idict:
      text = text.replace(key, idict[key])
   text = text.replace('јй', '̄ј')
   text = text.replace('й', 'и')
   return text

# TODO: def yot_palatalize(())

def conjugate(verb, AP, MP):
   prs_endings = {'и': [(('и_', ), ('м')), (('и_'), ('ш')), (('и_'), ('')),
                        (('и_'), ('мо')), (('и_'), ('те')), (('е_'), ('')),
                        'й', 'ймо', 'йте'],
                  'е': ['е_м', 'е_ш', 'е_', 'е_мо', 'е_те', 'у_',
                        'й', 'ймо', 'йте'],
                  'а': ['а_м', 'а_ш', 'а_', 'а_мо', 'а_те', 'ају_',
                        'а_ј', 'а_јмо', 'а_јте']
                 }
   inf_endings = ['ти', 'о', 'ла', 'ло', 'ли', 'ле', 'ла',
                  'х', '~', '~', 'смо', 'сте', 'ше']

   MP_dict = {'alpha':
               {'inf': verb[:-2],
                'prs': (verb[:-3], 'и'),
                'pp': (palatalize(verb[:-3], mode='и'), 'е_н')},
              'beta':
               {'inf': verb[:-2],
                'prs': (verb[:-3], 'а'),
                'pp': (verb[:-3], 'а_н')},
              'epsilon':
               {'inf': verb[:-2],
                'prs': (verb[:-5]+'уј', 'е'),
                'pp': (verb[:-3], 'а_н')},
              'delta':
               {'inf': verb[:-2],
                'prs': (palatalize(verb[:-3]), 'е'),
                'pp': (verb[:-3], 'а_н')}
             }

   for ending in inf_endings:
      print(prettify(MP_dict[MP]['inf'] + ending))
   #for ending in prs_endings[MP_dict[MP]['prs'][1]]:
   #   print (prettify(MP_dict[MP]['prs'][0] + ending))

   return None

def conjugate2(verb: str, info: GramInfo):
   accented_verb = garde(accentize(verb, info.accents))
   infinitive_dict = {'alpha': 'ити', 'beta': 'ати', 'gamma': 'нути',
                      'delta': 'ати', 'epsilon': 'овати', 'zeta': 'ивати',
                      'eta': 'ети', 'theta': 'ети', 'iota': 'ати',
                      'kappa': 'ти', 'lambda': 'ти', 'mu': 'ати'}
   if info.MP in infinitive_dict:
      verb_forms = []
      if info.AP == 'a':
         trunk = accented_verb[:-len(infinitive_dict[info.MP])]
         for stem in MP_to_stems[info.MP]:
            for ending in stem:
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
            for ending in stem:
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
         if '0̍' in form:
            form = form.replace('0', '')
            form = form.replace('̍', '')
            form = form.replace('~', '\u0304')
            to_insert = first_vowel_index(form) + 1
            form = insert(form, {to_insert: '̍'})
         form = form.replace('̍\u0304', '\u0304̍')
         form = form.replace('̍~', '̍')
         form = form.replace('~̍', '̍') # if I accidentally forgot to manage it
         form = form.replace('~', '')
         form = form.replace('0', '')
         form = form.replace('·', '')
         form = prettify(form)
         yield form

   return verb_forms

def main():
   dir_path = os.path.dirname(os.path.realpath(__file__))

   with open(dir_path + '\\a_sr_ru.yaml', encoding="utf-8") as f:
      data = yaml.load(f)
      letter_a = data['letter_a'][0]
      while True:
         raw_word = random.choice(list(letter_a.keys()))
         if 'i' in letter_a[raw_word]:
            print('{:>25} : '.format(raw_word), end="")
            deciphered = decipher(letter_a[raw_word]['i'])
            print(deciphered)
            accented_word = accentize(raw_word, deciphered.accents)
            print(accented_word)
            print(garde(accented_word))
            #conjugate(raw_word, None, deciphered.MP)
            yield from conjugate2(raw_word, deciphered)
            break
   
if __name__ == '__main__':
   for form in main():
      print(form)
