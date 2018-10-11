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
      if morpheme.startswith('>') and self.info.AP[i] != 'd:':
         word_form = word_form.replace('\u0304', '')
      morpheme = morpheme.replace('>', '')
      if morpheme.startswith('<'):
         lvi = last_vowel_index(word_form)
         if not '\u0304' in word_form[lvi:] and lvi is not None:
            word_form = insert(word_form, {lvi+1: '\u0304'})
            word_form = word_form.replace('\u0304·', '·\u0304')
            fvi = first_vowel_index(word_form)
            if lvi != fvi and '\u0304\u030d' in word_form[lvi:] \
                  and not '\u0304' in word_form[:lvi] :
               pvi = last_vowel_index(word_form[:lvi]) # penultimate vowel index
               if pvi:     
                  word_form = word_form.replace('\u030d', '')
                  word_form = insert(word_form, {pvi+1: '\u030d'})
               else:
                  raise IndexError(f"{word_form} has not enough vowels for this operation")
      morpheme = morpheme.replace('<', '')
      if self.info.AP[i] in ending_part.accent:
         if self.info.AP[i] in oa:
            word_form = word_form.replace('\u030d', '') # straight
         if ('b' in self.info.AP[i] or 'd' in self.info.AP[i]) and '\u030d' in word_form and not '0' in morpheme:
            morpheme = morpheme.replace('·', '')
         #print('do: ', ending_part.morpheme)
         morpheme = morpheme.replace('·', '\u030d') # to straight
         #print('posle: ', morpheme)
      return word_form + morpheme
      