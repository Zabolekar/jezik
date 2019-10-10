from typing import Dict, List, Optional, Tuple
from .paradigm_helpers import AccentedTuple, GramInfo, oa
from .utils import first_vowel_index, last_vowel_index, indices, insert, deyerify
from .charutils import cstraight, cmacron
from .data.multidict import Replacement

def _swap(trunk: str, AP: str) -> str:
   """this function swaps last vowel of given trunk
   from long to short and vice versa"""

   lvi = last_vowel_index(trunk)
   last_macron = trunk.rfind(cmacron)

   if lvi: # if the word has vowels 
      if AP.endswith(':') and lvi+1 != last_macron and lvi+2 != last_macron:
         return insert(trunk, {lvi+1: cmacron}) # insert macron if needed

      elif AP.endswith('.') and lvi+1 != last_macron and last_macron != -1:
      # and vice versa, delete macron from the last vowel
         return trunk[:last_macron] + trunk[last_macron+1:]

   return trunk


def _apply_neocirk(word_form: str,
                   lvi: Optional[int],
                   pvi: Optional[int],
                   morpheme: str,
                   retraction: int
) -> List[str]: # do not change to Tuple

   """ neocircumflex is accent retraction from a newly long vowel;
   this function returns only one tuple, unlike _delete_left_bracket"""

   for _ in range(retraction):
      # word unaccented, has vowels: accentize last vowel
      if cstraight not in word_form: 
         if lvi is not None: 
            word_form = insert(word_form, {lvi+1: cstraight})
            morpheme = morpheme.replace('·', '') # no further possibilities to accentize it
      elif lvi is not None and pvi is not None:
         word_form = word_form.replace(cstraight, '') # delete accent mark
         word_form = insert(word_form, {pvi+1: cstraight}) # add accent mark after pvi
         morpheme = morpheme.replace('·', '')
      #else:
         #raise IndexError(f"{word_form} has not enough vowels for this operation")
   return [word_form, morpheme]


class PartOfSpeech():
   def __init__(
      self,
      key: str,
      kind: str,
      info: str,
      replacements: Tuple[Replacement, ...],
      amendments: Tuple[Replacement, ...]
   ) -> None:
      self.key = key.split('\\')[0]
      self.gram = GramInfo(kind, info.split(';'))
      self.replacements: Dict[str, List[str]] = dict(replacements)
      self.amendments: Dict[str, List[str]] = dict(amendments)

   def label(self, lbl: str) -> bool:
      return lbl in self.gram.other

   @staticmethod
   def accentize(current_AP: str, word: str) -> str:
      if current_AP not in oa:
         word = word.replace(cstraight, '')
      if cstraight not in word: # straight
         return word.replace('·', cstraight, 1) # to straight
      return word.replace('·', '')

   @staticmethod
   def swap(trunk: str, length_inconstant: bool, AP: str, target_AP: str) -> str:
      """ swap words like boos ~ bosa, otherwise pass"""
      if length_inconstant and AP == target_AP:
         return _swap(trunk, AP)
      return trunk

   def _delete_left_bracket(
      self,
      word_form: str,
      morpheme: str,
      accent: str,
      current_AP: str
   ) -> List[List[str]]:
      """
      This function is so far for nouns only.
      It explicitly uses noun AP names.
      So it better be placed somewhere else? TODO
      """
      result = []
      if morpheme.startswith('<'): # so far only '-ā' is like that
         # 1. handling yers and defining if the word has neocircumflex:
         # if morpheme is genitive -ā,
         # stem has mobile vowel, ending is accented,
         # gender is not feminine (i.e. m/n),
         # and, at last, word is not komunizam-like exception (a.p. q),
         # then word DOES have neocircumflex retraction
         # and yer is FORCEDLY clarified to an 'a' sound;
         # other yers will be handled afterwards by the common yer rule
         #
         # without yers, in cases like jèzik : jȅzīkā:
         # stem has no mobile vowel, stem is accented,
         # word is not feminine, accented vowel is not the first one

         # 2. finding vowel places that will be of importance
         lvi, fvi, pvi = indices(word_form)

         # 2.5 handling óvca > ovácā
         if cmacron in word_form and self.label("f") and current_AP in ('c:', 'g:'):
            word_form = word_form.replace(cmacron, '')

         # 2.7 handling yers and predefining retractions
         retraction = [0]
         if self.label('m'):
            if 'ъ' in word_form and current_AP in accent \
               and current_AP in ['a:', 'b:', 'c:', 'f.']:
               retraction = [2] # Макѐдо̄на̄ца̄, но̏ва̄ца̄
            elif (('d' in current_AP and 'œв' in word_form)
               or (pvi is not None and 'ъ' not in word_form \
               and current_AP not in accent \
               and (current_AP in ['a.', 'a!']) \
               or ('b.' in current_AP and 'ъ' in word_form and 'œ' in word_form))):
               retraction = [1] # је̏зӣка̄, а̀ма̄не̄та̄, о̀че̄ва̄
            elif 'œв' in word_form and 'c?' in current_AP:
               retraction = [2, 1, 0] # бо̏го̄ва̄, бо̀го̄ва̄, бого́ва̄
            elif 'œв' in word_form and 'b' in current_AP and 'ъ' not in word_form:
               retraction = [2, 1] # гро̏ше̄ва̄ & гро̀ше̄ва̄, би̏ко̄ва̄ & бѝко̄ва̄

         if not 'œ' in word_form: # TODO one day think about better condition
            word_form = word_form.replace('ъ', 'а')
         else:
            word_form = deyerify(word_form)

         # a renewed set of indices, since ъ has become а
         lvi, fvi, pvi = indices(word_form)

         # 3. handling strange new exceptions like komunizam
         if '·' in word_form and current_AP == 'q.' and lvi is not None:
            word_form = insert(word_form.replace('·', ''), {lvi: '·'})

         # 4. we insert macron after lvi if last vowel is short
         if not cmacron in word_form[lvi:] and lvi is not None:
            word_form = insert(word_form, {lvi+1: cmacron}).replace(f'{cmacron}·', f'·{cmacron}')

         # 5. if we have neocircumflex retraction, we apply it
         for case in retraction:
            result.append(_apply_neocirk(word_form, lvi, pvi, morpheme, case))

         if retraction == [0]:

            # 6. in some cases (TODO: when??) we delete all straight accents and reinsert a new one at pvi
            if lvi != fvi and pvi is not None \
               and f"{cmacron}{cstraight}" in word_form[lvi:] \
                  and not cmacron in word_form[:lvi] \
                  and not 'q' in current_AP \
                  and not 'c?' in current_AP:

               word_form = word_form.replace(cstraight, '')
               word_form = insert(word_form, {pvi+1: cstraight})

      else:
         result = [[word_form, morpheme]]
      for pair in result:
         pair[1] = pair[1].replace('<', '')
      return result

   def _append_morpheme(
      self,
      current_AP: str,
      word_form: List[str],
      ending_part: AccentedTuple
   ) -> List[str]:

      connectenda: List[List[str]] = []

      for word_subform in word_form:

         morpheme, accent = ending_part.morpheme, ending_part.accent

         if current_AP not in ('c:', 'g:'):
            morpheme = morpheme.replace('>>', '')

         # deleting the first of two accents (is it OK to have it here?)
         if current_AP in accent and cstraight in word_subform:
            word_subform = word_subform.replace(cstraight, '')

         # first we delete '>' (= delete all macrons in the word)
         # then we delete '<' (= lengthen the last vowel in the stem)

         if morpheme.startswith('>') and current_AP in ['d:', 'e:', 'f.']:
            morpheme = morpheme.replace('>', '')
         connectenda += self._delete_left_bracket(word_subform, morpheme, accent, current_AP)

      # if this ending_part IS ACCENTED in this AP,
      # then first we delete the now unnecessary accent in the stem in case it is there;
      # second we put the accent into the ending_part,
      # the word hereby being accented;
      # and if it shouldn't, we just do nothing and leave it unaccented;
      # after that, we append the morpheme
      # TODO: understand all this "in [paradigm list]" stuff;
      # I already see it is needed here, but it seems unlogical

      result = []

      for pair in connectenda:
         # accentizing endings (?)
         if current_AP in ending_part.accent:
            #if self.gram.AP[i] not in ['c?']:
            #word_form = word_form.replace('\u030d', '')
            if cstraight in word_form and not '0' in pair[1]: # TODO: provide example for this
               pair[1] = pair[1].replace('·', '')
            if 'q' in current_AP:
               pair[1] = pair[1].replace('0', '')
            pair[1] = pair[1].replace('·', cstraight)
            pair[0] = pair[0].replace('·', '')
         # accentizing non-enclinomical words (finally!)
         # this line of code also helped solving 'aludirati' bug
         # (when too many enclinomena appear, like **ȁludīrām)
         elif cstraight not in pair[0]:
            pair[0] = pair[0].replace('·', cstraight)

         result_word = pair[0] + pair[1]

         # accentizing enclinomena (words without accent)
         #if all(x not in current_AP for x in ['o', 'a', 'b', 'e']) and # TODO: is this line needed?
         if cstraight not in result_word:
            fvi = first_vowel_index(result_word)
            if fvi is None and 'ъ' in result_word and 'ø' in result_word: # сънø > сан etc.
               fvi = result_word.find('ъ')
            if fvi is not None:
               result_word = insert(result_word, {fvi+1: cstraight})

         result.append(result_word)

      return result
