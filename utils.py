# TODO:
# ----- well-named function for recessive accent,
#       e.g. recessive(sequence) -> se̍quence
# ----- think of better name for prettify(), like alternate() or assimilate()

import re
from typing import Dict, Optional, Iterator, Tuple

palatalization_modes: Dict[str, Dict[str, str]] = {
   'и': {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
         'ст': 'шт', 'зд': 'жд', 'сл': 'шљ', 'зл': 'жљ',
         'шт': 'шт', 'жд': 'жд', 'ск': 'шт', 'зг': 'жд',
         'к': 'к', 'ц': 'ч', 'х': 'х', 'г': 'г',
         'ш': 'ш', 'ж': 'ж', 'ч': 'ч', 'џ': 'џ',
         'т': 'ћ', 'д': 'ђ', 'с': 'ш', 'з': 'ж',
         'л': 'љ', 'р': 'р', 'н': 'њ', 'ј': 'ј'},
   'ĵ': {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
         'ст': 'шћ', 'зд': 'жђ', 'сл': 'шљ', 'зл': 'жљ',
         'шт': 'шћ', 'жд': 'жђ', 'ск': 'шт', 'зг': 'жд',
         'к': 'чј', 'ц': 'чј', 'х': 'шј', 'г': 'жј',
         'ш': 'шј', 'ж': 'жј', 'ч': 'чј', 'џ': 'џј',
         'т': 'ћ', 'д': 'ђ', 'с': 'сј', 'з': 'зј',
         'л': 'љ', 'р': 'рј', 'н': 'њ', 'ј': 'ј'},
   '': {'б': 'бљ', 'м': 'мљ', 'в': 'вљ', 'ф': 'фљ', 'п': 'пљ',
        'ст': 'шћ', 'зд': 'жђ', 'сл': 'шљ', 'зл': 'жљ',
        'шт': 'шћ', 'жд': 'жђ', 'ск': 'шт', 'зг': 'жд',
        'к': 'ч', 'ц': 'ч', 'х': 'ш', 'г': 'ж',
        'ш': 'ш', 'ж': 'ж', 'ч': 'ч', 'џ': 'џ',
        'т': 'ћ', 'д': 'ђ', 'с': 'ш', 'з': 'ж',
        'л': 'љ', 'р': 'р', 'н': 'њ', 'ј': 'ј'},
   'ȷ': {'бȷ': 'бљ', 'мȷ': 'мљ', 'вȷ': 'вљ', 'фȷ': 'фљ', 'пȷ': 'пљ',
         'стȷ': 'шт', 'здȷ': 'жд', 'слȷ': 'шљ', 'злȷ': 'жљ',
         'штȷ': 'шт', 'ждȷ': 'жд',  'скȷ': 'шт', 'згȷ': 'жд',
         'кȷ': 'ч', 'цȷ': 'ч', 'хȷ': 'ш', 'гȷ': 'ж',
         'шȷ': 'ш', 'жȷ': 'ж', 'чȷ': 'ч', 'џȷ': 'џ',
         'тȷ': 'ћ', 'дȷ': 'ђ', 'сȷ': 'ш', 'зȷ': 'ж',
         'лȷ': 'љ', 'рȷ': 'р', 'нȷ': 'њ', 'јȷ': 'ј',
         'љȷ': 'љ', 'њȷ': 'њ',
         'кʹ': 'ц', 'гʹ': 'з', 'хʹ': 'с',
         'кʺе': 'че', 'цʺе': 'че', 'гʺ': 'ж', 'хʺ': 'ш',
         'ʹ': '', 'ʺ': '', 'ȷ': ''}
}

all_vowels = "АаЕеИиОоУуӤӥŒœꙒꙓѢѣAaEeIiOoUu\u0325"
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

def indices(trunk: str) -> Tuple[Optional[int], Optional[int], Optional[int]]:
   lvi = last_vowel_index(trunk)
   fvi = first_vowel_index(trunk)
   pvi = last_vowel_index(trunk[:lvi])
   return lvi, fvi, pvi

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
   digraphs = ['ст', 'зд', 'сл', 'зл', 'шт', 'жд', 'ск', 'зг']
   if sequence[-2:] in digraphs:
      return sequence[:-2] + idict[sequence[-2:]]

   return sequence[:-1] + idict[sequence[-1]]

def deyerify(form: str) -> str:
   repl_dict = {"стън": "сн",
                "(бък": "пк", "дък": "тк", "ђък": "ћк",
                "жък": "шк", "зък": "ск", "џък": "чк",
                "бъц": "пц", "ђъц": "ћц", "дъц": "ц", "тъц": "ц",
                "жъц": "шц", "зц": "сц", "џц": "чц",
                "бъч": "пч", "ђъч": "ћч", "дъч": "ч", "тъч": "ч",
                "жъч": "шч", "зч": "шч", "сч": "шч", "џч": "ч"} 
   if 'ø' in form:
      form = form.replace('ø', '').replace('ъ', 'а')
   else:
      form = re.sub('([аеиоу\u0325][\u030d·]?)([лљмнњрṕјв])ъ', '\\1\u0304\\2ъ', form)
      for repl in repl_dict:
         form = form.replace(repl, repl_dict[repl])
      form = form.replace('ъ', '')
   match = re.search('[бвгдђжзјклʌљмнњпрṕсćтћфхцчџш]\u030d', form)
   if match: # if 
      wrong_acc_index = match.span()[0]
      form = form.replace('\u030d', '')
      lvi = last_vowel_index(form[:wrong_acc_index+2])
      if lvi is None:
         raise ValueError(f"_{form[:wrong_acc_index+2]}_ does not contain any vowels")
      else:
         form = insert(form, {lvi+1: '\u030d'})
   return form

def prettify(text: str, yat:str='ekav') -> str:
   idict = palatalization_modes['ȷ']
   replaces = [ ('јӥ', '\u0304ј'), ('ӥ', 'и'),
                ('ʌ(а|е|и|о|у|р|œ|\u0325)', 'л\\1'), ('̄̍ʌ', '̍ʌ'), ( '̄ʌ', 'ʌ'),
                ('о·ʌ', 'о\u0304·'), ('оʌ', 'о\u0304'), ('о\u030dʌ', 'о\u0304\u030d'),
                ('о·\u0304ʌ', 'о·\u0304'), ('ʌ', 'о'),
                ('([цчџњљћђшжјṕ])œ', '\\1е'), ('œ', 'о'),
                ('ṕ', 'р'), ('ć', 'с')]
   yat_replaces = { 'ekav': [('ꙓ', 'е'), ('ѣ', 'е')],
                    'jekav': [('ѣ(\u030d?о)', 'и\\1'),
                              ('лѣ', 'ље'), ('нѣ', 'ње'),
                              ('ѣ(\u030d?[љјњ])', 'и\\1'),
                              ('ꙓ(\u030d?[ој])', "и\\1"), ('ꙓ̄', 'йје̄'),
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
               'ӣѝй': 'и', 'ѐ': 'е', 'ӢЍЙ': 'И', 'Ѐ': 'Е'}
   for accent in accents:
      text = text.replace(accent, '')
   for letters in accented:
      for letter in letters:
         text = text.replace(letter, accented[letters])

   return text

def garde(word: str) -> str: # Garde's accentuation
   
   result = word
   while re.findall("[\u0300\u0301\u030f\u0311]", result): # while word is ungarded-like:

      short_desc_index = result.rfind('\u030f') # short falling index
      long_desc_index = result.rfind('\u0311') # long falling index
      real_fvi = first_vowel_index(result)
      fvi = real_fvi if real_fvi is not None else -10

      # if not 'there is a falling accent and it is not of the first syllable'
      # then the word is garded the usual way
      if not ((fvi + 1 != short_desc_index and short_desc_index != -1) \
           or (fvi + 1 != long_desc_index and long_desc_index != -1)):
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
                  insert_dict[i+1] = '\u030d' # straight accent
                  insert_bool = False
               else:
                  if len(result) > i+1:
                     if result[i+1] == '\u0300': # `
                        insert_bool = True
                        word2 = re.sub("^(.{" + str(i+1) + "}).", r"\g<1>" + '•', word2)
                     elif result[i+1] == '\u0301': # ´
                        insert_bool = True
                        word2 = re.sub("^(.{" + str(i+1) + "}).", r"\g<1>" + '\u0304', word2)
                     elif result[i+1] == '\u030f': # ¨
                        word2 = re.sub("^(.{" + str(i+1) + "}).",
                                       r"\g<1>" + '\u030d',
                                       word2)  # straight accent
                     elif result[i+1] == '\u0311': # ^
                        word2 = re.sub("^(.{" + str(i+1) + "}).",
                                       r"\g<1>" + '\u030d',
                                       word2) # straight accent
                        insert_dict[i+1] = '\u0304' # _

         word3 = insert(word2, insert_dict)
         word3 = re.sub('•', '', word3) # delete
         word3 = re.sub('\u030d\u0304', '\u0304\u030d', word3) #swap length \u0304 and accent \u030d
         result = word3
      
      else:
         excl_index = max(short_desc_index, long_desc_index)
         result = insert(result, {excl_index-1: '!'})
         result = result.replace('\u030f', '\u030d').replace('\u0311', '\u0304\u030d')
      
   return result
      
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

def ungarde(form: str) -> str:

   chars = list(form)
   while '\u030d' in chars:
      old_accent_index = chars.index("\u030d")
      chars.pop(old_accent_index)

      new_accent_index = old_accent_index - 1
      vowel_count = 0
      shifted = False
      while new_accent_index >= 0:
         if chars[new_accent_index] == "!":
            chars.pop(new_accent_index)
            old_accent_index -= 1
            break
         if chars[new_accent_index] in "aeiouAEIOUаеиоуАЕИОУ\u0325":
            vowel_count += 1
            if vowel_count == 2:
               shifted = True
               new_accent_index += 1
               break
         new_accent_index -= 1

      if shifted:
         chars.insert(new_accent_index, "\u0300") #rising
      else:
         chars.insert(old_accent_index, "\u030f") #falling

   return ("".join(chars)
             .replace("\u0300\u0304", "\u0301") #long rising
             .replace("\u0304\u030f", "\u0311")) #long falling

def expose(form: str, yat:str='ekav') -> str:
   "all transformations from internal to external representation"
   return ungarde(prettify(purify(zeroify(deyerify(form))), yat))

