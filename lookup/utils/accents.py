import re
from typing import Pattern
from . import characters as c
from .charutils import all_vowels, any_of_four_accents
from .text_utils import first_vowel_index, insert, swap

# Naming of things added for optimization purposes:
#   <name>_c − <name> but with compiled regexes
#   <name>_translator — a translation table used by `str.translate`
#   _<funcname>_<name> — a thing used by function `funcname`

_garde_four_accents_c: Pattern = re.compile(any_of_four_accents)
_garde_translator = str.maketrans({
   c.doublegrave: c.straight,
   c.circumflex: f'{c.macron}{c.straight}'
})

def _replace_at(text:str, index:int, new:str) -> str:
   return text[:index] + new + text[index+1:]

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
                     if result[i+1] == c.grave:
                        insert_bool = True
                        word2 = _replace_at(word2, i+1, '•')
                     elif result[i+1] == c.acute:
                        insert_bool = True
                        word2 = _replace_at(word2, i+1, c.macron)
                     elif result[i+1] == c.doublegrave:
                        word2 = _replace_at(word2, i+1, c.straight)
                     elif result[i+1] == c.circumflex:
                        word2 = _replace_at(word2, i+1, c.straight)
                        insert_dict[i+1] = c.macron

         word3 = insert(word2, insert_dict)
         word3 = swap(word3.replace('•', ''), c.straight, c.macron)
         result = word3

      else:
         excl_index = max(short_desc_index, long_desc_index)
         result = insert(result, {excl_index-1: '!'})
         result = result.translate(_garde_translator)
   return result

_make_recessive_translator = str.maketrans({
   '0': None,
   c.straight: None,
   '~': c.macron
})

def make_recessive(form:str) -> str:
   if '0̍' in form: # 0 means accent on the firstmost syllable
      form = form.translate(_make_recessive_translator)
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
