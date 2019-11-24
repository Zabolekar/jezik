# TODO:
# ----- well-named function for recessive accent,
#       e.g. recessive(sequence) -> se̍quence
# ----- think of better name for prettify(), like alternate() or assimilate()

import re
from typing import Dict, Optional, Iterator, Tuple
from .charutils import (cring, cmacron, cstraight, cacute,
                        cgrave, cdoublegrave, ccircumflex,
                        all_vowels, any_vowel, any_of_four_accents,
                        all_accent_marks, real_accent)

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

cyr2lat_dict = {
   'й':'ĭ', 'Й':'Ĭ',
   'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'ђ':'đ', 'е':'e', 'ж':'ž', 'з':'z', 'и':'i',
   'ј':'j', 'к':'k', 'л':'l', 'љ':'lj', 'м':'m', 'н':'n', 'њ':'nj', 'о':'o', 'п':'p', 'р':'r',
   'с':'s', 'т':'t', 'ћ':'ć', 'у':'u', 'ф':'f', 'х':'h', 'ц':'c', 'ч':'č', 'џ':'dž', 'ш':'š',
   'А':'A', 'Б':'B', 'В':'V', 'Г':'G', 'Д':'D', 'Ђ':'Đ', 'Е':'E', 'Ж':'Ž', 'З':'Z', 'И':'I',
   'Ј':'J', 'К':'K', 'Л':'L', 'Љ':'Lj', 'М':'M', 'Н':'N', 'Њ':'Nj', 'О':'O', 'П':'P', 'Р':'R',
   'С':'S', 'Т':'T', 'Ћ':'Ć', 'У':'U', 'Ф':'F', 'Х':'H', 'Ц':'C', 'Ч':'Č', 'Џ':'Dž', 'Ш':'Š'
   }

def cyr2lat(lowertext: str) -> str:
   return ''.join([cyr2lat_dict.get(letter, letter) for letter in lowertext])

def last_vowel_index(trunk: str) -> Optional[int]:
   if re.search(any_vowel, trunk):
      *__, last_vowel = re.finditer(any_vowel, trunk)
      index, _ = last_vowel.span()
      return index
   return None

def first_vowel_index(trunk: str) -> Optional[int]:
   match = re.search(any_vowel, trunk)
   if match:
      return match.span()[0]
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
      form = re.sub(f'([аеиоу{cring}][{cstraight}·]?)([лљмнњрјв]ʲ?)ъ', f'\\1{cmacron}\\2ъ', form)
      for repl in repl_dict:
         form = form.replace(repl, repl_dict[repl])
      form = form.replace('ъ', '')
   match = re.search(f'[бвгдђжзјклʌљмнњпрṕсćтћфхцчџш]ʲ?{cstraight}', form)
   if match: 
      wrong_acc_index = match.span()[0]
      form = form.replace(cstraight, '')
      lvi = last_vowel_index(form[:wrong_acc_index+2])
      if lvi is None:
         raise ValueError(f"_{form[:wrong_acc_index+2]}_ does not contain any vowels")
      else:
         form = insert(form, {lvi+1: cstraight})
   return form

def prettify(text: str, yat:str="e") -> str:
   idict = palatalization_modes['ȷ']
   replaces = [
      ('([чшжј])ѣ', '\\1а'), ('(шт|жд)ѣ', '\\1а'),
      (f'јӥ{cstraight}', f'{cstraight}јӥ'), ('јӥ', f'{cmacron}ј'),
      ('ӥ', 'и'), (f'{cstraight}{cmacron}', f'{cmacron}{cstraight}'),
      (f'ʌ(а|е|и|о|у|р|œ|{cring})', 'л\\1'),
      (f'{cmacron}{cstraight}ʌ', f'{cstraight}ʌ'),
      (f'{cmacron}ʌ', 'ʌ'),
      ('о·ʌ', f'о{cmacron}·'), ('оʌ', f'о{cmacron}'),
      (f'о{cstraight}ʌ', f'о{cmacron}{cstraight}'),
      (f'о·{cmacron}ʌ', f'о·{cmacron}'), ('ʌ', 'о'),
      ('цœ', 'че'),
      ('([ҵчџњљћђшжјʲ])œ', '\\1е'), ('œ', 'о'),
      ('ʲ', '')]
   yat_replaces = {
      "e": [('ꙓ', 'е'), ('ѣ', 'е')],
      "je": [
         (f'ѣ({cstraight}?о)', 'и\\1'),
         ('лѣ', 'ље'), ('нѣ', 'ње'),
         (f'ѣ({cstraight}?[љјњ])', 'и\\1'),
         (f'ꙓ({cstraight}?[ој])', "и\\1"),
         (f'ꙓ{cmacron}', f'йје{cmacron}'),
         ('лꙓ', 'ље'), ('нꙓ', 'ње'),
         ('([бгджзкпстфхцчш]р)ꙓ', '\\1е'),
         ('[ꙓѣ]', 'је')] }
   yat_replaces["ije"] = yat_replaces["je"]

   for key in idict:
      text = text.replace(key, idict[key])
   for entity in replaces:
      text = re.sub(entity[0], entity[1], text)
   for entity in yat_replaces[yat]:
      text = re.sub(entity[0], entity[1], text)
   return text

def deaccentize(text: str) -> str:
   accented = {'ȁȃâáàā': 'a', 'ȅȇêéèē': 'e', 'ȉȋîíìīĭ': 'i',
               'ȕȗûúùū': 'u', 'ȑȓŕ': 'r', 'ȀȂÂÁÀĀ': 'A',
               'ȄȆÊÉÈĒ': 'E', 'ȈȊÎÍÌĪĬ': 'I', 'ȔȖÛÚÙŪ': 'U',
               'ȐȒŔ': 'R', 'ȍȏôóòō': 'o', 'ȌȎÔÓÒŌ': 'O',
               'ӣѝй': 'и', 'ѐ': 'е', 'ӢЍЙ': 'И', 'Ѐ': 'Е'}
   for accent in all_accent_marks:
      text = text.replace(accent, '')
   for letters in accented:
      for letter in letters:
         text = text.replace(letter, accented[letters])

   return text

def garde(word: str) -> str: # Garde's accentuation
   result = word
   while re.findall(any_of_four_accents, result): # while word is ungarded-like:

      short_desc_index = result.rfind(cdoublegrave)
      long_desc_index = result.rfind(ccircumflex)
      real_fvi = first_vowel_index(result)
      fvi = real_fvi if real_fvi is not None else -100

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
                  insert_dict[i+1] = cstraight
                  insert_bool = False
               else:
                  if len(result) > i+1:
                     if result[i+1] == cgrave:
                        insert_bool = True
                        word2 = re.sub("^(.{" + str(i+1) + "}).", r"\g<1>" + '•', word2)
                     elif result[i+1] == cacute:
                        insert_bool = True
                        word2 = re.sub("^(.{" + str(i+1) + "}).", r"\g<1>" + cmacron, word2)
                     elif result[i+1] == cdoublegrave:
                        word2 = re.sub("^(.{" + str(i+1) + "}).",
                                       r"\g<1>" + cstraight,
                                       word2)
                     elif result[i+1] == ccircumflex:
                        word2 = re.sub("^(.{" + str(i+1) + "}).",
                                       r"\g<1>" + cstraight,
                                       word2)
                        insert_dict[i+1] = cmacron

         word3 = insert(word2, insert_dict)
         word3 = re.sub('•', '', word3) # delete
         word3 = re.sub(f'{cstraight}{cmacron}',
                        f'{cmacron}{cstraight}',
                        word3) #swap length and accent
         result = word3

      else:
         excl_index = max(short_desc_index, long_desc_index)
         result = insert(result, {excl_index-1: '!'})
         result = result.replace(cdoublegrave, cstraight)
         result = result.replace(ccircumflex, f'{cmacron}{cstraight}')
   return result

def zeroify(form: str) -> str:
   if '0̍' in form: # 0 means accent on the firstmost syllable
      form = (form
              .replace('0', '')
              .replace(cstraight, '')
              .replace('~', cmacron))
      fvi = first_vowel_index(form)
      if fvi is None:
         raise ValueError(f"{form} does not contain any vowels")
      else:
         to_insert = fvi + 1
         form = insert(form, {to_insert: cstraight}) # straight accent
   return form

def purify(form: str) -> str:
   return (form.replace('~', '')
               .replace('0', '')
               .replace('·', '')
               .replace(f'{cstraight}{cmacron}', f'{cmacron}{cstraight}')
           )

def ungarde(form: str) -> str:
   chars = list(form) # splitting string into characters
   while cstraight in chars:
      old_accent_index = chars.index(cstraight)
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
         chars.insert(new_accent_index, cgrave) #rising
      elif old_accent_index == 0:
         chars.insert(1, cdoublegrave) #falling
      else:
         chars.insert(old_accent_index, cdoublegrave) #falling

   return ("".join(chars)
             .replace(f'{cgrave}{cmacron}', cacute) #long rising
             .replace(f'{cmacron}{cdoublegrave}', ccircumflex)
             .replace(f'{cdoublegrave}{cmacron}', ccircumflex)) #long falling

def debracketify(form: str) -> str:
      if '>' in form:
         barrier = form.find('>')
         first_piece = form[:barrier]
         first_piece = first_piece.replace(cmacron, '')
         second_piece = form[barrier:].replace('>', '')
         form = first_piece + second_piece
      return form

def je2ije(form: str) -> str:
   return form.replace(
         f'йје{cacute}', f'ије{cgrave}').replace(
         f'йје{ccircumflex}', f'и{cdoublegrave}је').replace(
         f'йје{cmacron}', 'ије')

def expose(form: str, yat:str="e", latin:bool=False) -> str:
   """all transformations from internal to external representation;
   ijekavian two-syllable yat appears only here, not in yat_replaces,
   otherwise ungarde() produces wrong results, i.e. **snìjeg"""
   result = ungarde(
      prettify(
         purify(zeroify(debracketify(deyerify(form)))),
         yat
      )
   )
   if yat == "ije":
      result = je2ije(result)
   if latin:
      result = cyr2lat(result)
   return result

def expose_replacement(form: str, yat:str="e", latin:bool=False) -> str:
   result = prettify(
      purify(zeroify(debracketify(deyerify(form)))),
      yat
   )
   for x in real_accent:
      result = result.replace(x, real_accent[x])
   if yat == "ije":
      result = je2ije(result)
   if latin:
      result = cyr2lat(result)
   return result
