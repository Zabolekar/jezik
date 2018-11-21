from typing import Any, Dict, Optional
from .paradigm_helpers import AccentedTuple, GramInfo #, oa
from .utils import first_vowel_index, last_vowel_index, insert

def _swap(trunk_: str, AP: str) -> str:
   # this function swaps last vowel of given trunk
   # from long to short and vice versa

   trunk_lvi = last_vowel_index(trunk_)
   last_macron = trunk_.rfind('\u0304')

   if trunk_lvi: # if the word has vowels (otherwise, do nothing):
      if AP.endswith(':') and trunk_lvi+1 != last_macron and trunk_lvi+2 != last_macron:
      # if we need to insert macron, we do it
         word_form = insert(trunk_, {trunk_lvi+2: '\u0304'})

      elif AP.endswith('.') and trunk_lvi+1 != last_macron and last_macron != -1:
      # and vice versa, we delete macron from the last vowel in case it is there
         word_form = trunk_[:last_macron] + trunk_[last_macron+1:] 

      else:
         word_form = trunk_
         #print(f'word {word_form} got vowels, but macron is ahead of middle dot!')
   else:
      word_form = trunk_
   return word_form

def _apply_neocirk(word_form: str, lvi: Optional[int], fvi: Optional[int], pvi: Optional[int],
                   morpheme: str, retraction: bool):
   # neocircumflex is accent retraction from a newly long vowel

   if retraction:
      if lvi is not None and pvi is not None:
         word_form = insert(word_form, {lvi+1: '\u0304'}) #macronize last vowel
         word_form = word_form.replace('\u030d', '') # delete accent mark
         word_form = insert(word_form, {pvi+1: '\u030d'}) # add accent mark after pvi
         morpheme = morpheme.replace('·', '') # no further possibilities to accentize it
      else:
         raise IndexError(f"{word_form} has not enough vowels for this operation")
   return word_form, morpheme

class PartOfSpeech():
   def __init__(self, key: str, value: Dict[str, Any], yat:str="ekav") -> None:
      self.key = key 
      self.value = value 
      i, t = self.value['i'].split(';'), self.value['t'] 
      self.info = GramInfo(i, t) 

   def swap(self, trunk_: str, length_inconstant: bool, AP: str, target_AP: str) -> str:
      # at first we process words like boos ~ bosa
      if length_inconstant and AP == target_AP:
         word_form = _swap(trunk_, AP)
      # this part is about words where length is the same in most forms:
      else:
         word_form = trunk_
      return word_form

   def _delete_right_bracket(self, word_form: str, morpheme: str, i: int):
      if morpheme.startswith('>') and self.info.AP[i] not in ['d:', 'e:']:
         word_form = word_form.replace('\u0304', '')
      morpheme = morpheme.replace('>', '')
      return (word_form, morpheme)

   def _delete_left_bracket(self, word_form: str, morpheme: str, accent: str, i: int):
  
      retraction = False

      if morpheme.startswith('<'): # so far only '-ā' is like that

         # 1. handling yers and defining if the word has neocircumflex:
         # if morpheme is genitive -ā (so far the only one with '<'),
         # stem has mobile vowel, ending is accented,
         # gender is not feminine (i.e. m/n),
         # and, at last, word is not komunizam-like exception (a.p. q),
         # then word DOES have neocircumflex retraction
         # and yer is FORCEDLY clarified to an 'a' sound;
         # other yers will be handled afterwards by the common yer rule
         if 'ъ' in word_form \
            and self.info.AP[i] in accent \
            and not 'q' in self.info.AP[i] \
            and 'm' in self.info.other or 'n' in self.info.other:
            retraction = True 

         word_form = word_form.replace('ъ', 'а')

         # 2. finding vowel places that will be of importance
         lvi = last_vowel_index(word_form)
         fvi = first_vowel_index(word_form)
         pvi = last_vowel_index(word_form[:lvi]) # penultimate vowel index

         # 3. handling strange new exceptions like komunizam
         if '·' in word_form and self.info.AP[i] == 'q.' and lvi:
            word_form = insert(word_form.replace('·', ''), {lvi: '·'})

         # 4. if we have neocircumflex retraction, we apply it
         word_form, morpheme = _apply_neocirk(word_form, lvi, fvi, pvi, morpheme, retraction)

         #. 5. we insert macron after lvi if needed (TODO: when??)
         if not retraction:
            if not '\u0304' in word_form[lvi:] and lvi is not None:
               word_form = insert(word_form, {lvi+1: '\u0304'})
               word_form = word_form.replace('\u0304·', '·\u0304')
            # 6. in some cases (TODO: when??) we delete all macrons and reinsert a new one at pvi
            if lvi != fvi and '\u0304\u030d' in word_form[lvi:] \
                  and not '\u0304' in word_form[:lvi] \
                  and not 'q' in self.info.AP[i] \
                  and not 'c?' in self.info.AP[i]:
               if pvi is not None:     
                  word_form = word_form.replace('\u030d', '')
                  word_form = insert(word_form, {pvi+1: '\u030d'})
               # 7. and we raise IndexError if it is not possible
               else:
                  raise IndexError(f"{word_form} has not enough vowels for this operation")
                  
      morpheme = morpheme.replace('<', '')
      
      return (word_form, morpheme)

   def _append_morpheme(self, i: int, word_form: str, ending_part: AccentedTuple) -> str:
       
      # first we delete '>' (= delete all macrons in the word)
      # then we delete '<' (= lengthen the last vowel in the stem)

      morpheme = ending_part.morpheme
      accent = ending_part.accent

      word_form, morpheme = self._delete_right_bracket(word_form, morpheme, i)
      word_form, morpheme = self._delete_left_bracket(word_form, morpheme, accent, i)

      # if this ending_part IS ACCENTED in this AP,
      # then first we delete the now unnecessary accent in the stem in case it is there;
      # second we put the accent into the ending_part,
      # the word hereby being accented;
      # and if it shouldn't, we just do nothing and leave it unaccented;
      # after that, we append the morpheme

      if self.info.AP[i] in ending_part.accent:
         #if self.info.AP[i] in oa:
         word_form = word_form.replace('\u030d', '') # straight
         if (self.info.AP[i] in ['b.', 'b:', 'd:', 'e:']) and '\u030d' in word_form and not '0' in morpheme:
            morpheme = morpheme.replace('·', '')
         if  'q' in self.info.AP[i]:
            morpheme = morpheme.replace('0', '')
         morpheme = morpheme.replace('·', '\u030d') # to straight
      return word_form + morpheme
