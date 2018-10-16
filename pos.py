from typing import Any, Dict
from .paradigm_helpers import AccentedTuple, GramInfo, oa
from .utils import swap_length, first_vowel_index, last_vowel_index, insert

class PartOfSpeech():
   def __init__(self, key: str, value: Dict[str, Any], yat:str="ekav") -> None:
      self.key = key 
      self.value = value 
      i, t = self.value['i'].split(';'), self.value['t'] 
      self.info = GramInfo(i, t) 

   def _swap(self, trunk_: str, length_inconstant: bool, AP: str, target_AP: str) -> str:
      # at first we process words like boos ~ bosa
      if length_inconstant and AP == target_AP:
         word_form = swap_length(trunk_, AP)
      # this part is about words where length is the same in most forms:
      else:
         word_form = trunk_
      return word_form

   def _append_morpheme(self, i: int, word_form: str, ending_part: AccentedTuple) -> str:
      # if this ending_part should be accented in this AP,
      # then first we delete the now unnecessary accent in the stem in case it is there;
      # second we put the accent into the ending_part,
      # the word hereby being accented;
      # and if it shouldn't, we just do nothing and leave it unaccented;
      # after that, we append the morpheme
      morpheme = ending_part.morpheme
      if morpheme.startswith('>') and self.info.AP[i] not in ['d:', 'e:']:
         word_form = word_form.replace('\u0304', '')
      morpheme = morpheme.replace('>', '')
      twofold_neocirk = False
      if morpheme.startswith('<'): # so far only '-ā' is like that
         if 'ъ' in word_form and self.info.AP[i] in ending_part.accent \
                             and not 'q' in self.info.AP[i] \
                             and 'm' in self.info.other:
            twofold_neocirk = True 

         word_form = word_form.replace('ъ', 'а')

         lvi = last_vowel_index(word_form)
         fvi = first_vowel_index(word_form)
         pvi = last_vowel_index(word_form[:lvi]) # penultimate vowel index

         if '·' in word_form and self.info.AP[i] == 'q.' and lvi:
            word_form = insert(word_form.replace('·', ''), {lvi: '·'})

         if twofold_neocirk:
            if lvi is not None and pvi is not None:
               word_form = insert(word_form, {lvi+1: '\u0304'})
               word_form = word_form.replace('\u030d', '')
               word_form = insert(word_form, {pvi+1: '\u030d'})
               morpheme = morpheme.replace('·', '')           
            else:
               raise IndexError(f"{word_form} has not enough vowels for this operation")
         else:
            if not '\u0304' in word_form[lvi:] and lvi is not None:
               word_form = insert(word_form, {lvi+1: '\u0304'})
               word_form = word_form.replace('\u0304·', '·\u0304')
                  
            if lvi != fvi and '\u0304\u030d' in word_form[lvi:] \
                  and not '\u0304' in word_form[:lvi] \
                  and not 'q' in self.info.AP[i]:
               if pvi is not None:     
                  word_form = word_form.replace('\u030d', '')
                  word_form = insert(word_form, {pvi+1: '\u030d'})
               else:
                  raise IndexError(f"{word_form} has not enough vowels for this operation")
      morpheme = morpheme.replace('<', '')
      if self.info.AP[i] in ending_part.accent:
         if self.info.AP[i] in oa:
            word_form = word_form.replace('\u030d', '') # straight
         if (self.info.AP[i] in ['b.', 'b:', 'd:', 'e:']) and '\u030d' in word_form and not '0' in morpheme:
            morpheme = morpheme.replace('·', '')
         if  'q' in self.info.AP[i]:
            morpheme = morpheme.replace('0', '')
         morpheme = morpheme.replace('·', '\u030d') # to straight
      return word_form + morpheme
