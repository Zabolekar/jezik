from typing import Dict, List, Tuple
from .paradigm_helpers import AccentedTuple, GramInfo, MorphemeChain, oa
from .utils import first_vowel_index, last_vowel_index, insert
from .charutils import all_vowels, cstraight, cmacron, cring
from .data.multidict import Replacement

def _swap(trunk: str) -> str:
   """this function swaps last vowel of given trunk
   from long to short and vice versa"""
   lvi = last_vowel_index(trunk)
   last_macron = trunk.rfind(cmacron)

   if lvi is not None: # if the word has vowels
      if last_macron not in (lvi+1, lvi+2):
         return insert(trunk, {lvi+1: cmacron}) # insert macron if needed

      elif last_macron != -1:
      # and vice versa, delete macron from the last vowel
         return trunk[:last_macron] + trunk[last_macron+1:]

   return trunk

class PartOfSpeech():
   def __init__(
      self,
      key: str,
      accented_keys: str,
      kind: str,
      info: str,
      replacements: Tuple[Replacement, ...],
      amendments: Tuple[Replacement, ...]
   ) -> None:
      self.accented_keys = accented_keys.split(",")
      self.kind = kind
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
      if length_inconstant and AP != target_AP:
         return _swap(trunk)
      return trunk

   def _delete_left_bracket(
      self,
      stem: str,
      morpheme: str,
      accent: str,
      current_AP: str
   ) -> List[List[str]]:
      # see a huge algorithm with the same name in Noun
      return [[stem, morpheme]]

   def _append_morpheme(
      self,
      current_AP: str,
      stems: List[str],
      ending_part: AccentedTuple
   ) -> List[str]:

      connectenda: List[List[str]] = []

      for stem in stems:
         # syllable 'r'
         morpheme, accent = ending_part.morpheme, ending_part.accent
         if self.kind.startswith('V') and len(self.kind.split("\\")) > 3:
            stem_ = stem.replace(cmacron, '')
            morpheme_ = ''.join([x for x in morpheme if x.isalpha() and x not in "ʹʺ"])
            if stem_[-1] == 'р' and stem_[-2] not in all_vowels and morpheme_:
               if morpheme_[0] not in all_vowels:
                  stem = stem + cring
                  stem = stem.replace(cmacron + cring, cring + cmacron)

            if stem.endswith('р' + cmacron) and morpheme_:
               if morpheme_[0] in all_vowels:
                  stem = stem[:-1]

         # declickify (ʘ) -- special double '0' in nesti-verbs
         if self.kind.startswith('V'):
            if current_AP in ('eʹxʺ'):
               morpheme = morpheme.replace('ʘ', '')
         morpheme = morpheme.replace('ʘ', '0')

         if current_AP not in ('c:', 'g:'):
            morpheme = morpheme.replace('>>', '')

         # deleting the first of two accents (is it OK to have it here?)
         if current_AP in accent and cstraight in stem:
            stem = stem.replace(cstraight, '')

         # first we delete '>' (= delete all macrons in the word)
         # then we delete '<' (= lengthen the last vowel in the stem)

         if morpheme.startswith('>') and current_AP in ['d:', 'e:', 'f.']:
            morpheme = morpheme.replace('>', '')
         connectenda += self._delete_left_bracket(stem, morpheme, accent, current_AP)

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
         if current_AP in accent:
            if cstraight in pair[0] and not '0' in pair[1]:
               # e.g. ['Аргенти̍·̄на̄ц', 'а̄'] or ['вр̥х>œ̍̄в', 'а̄']
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
         # accentizing enclinomena (words without accent that receive automatic accent on first syllable)
         if cstraight not in result_word: # result_word is enclinomen
            fvi = first_vowel_index(result_word)
            if fvi is None and 'ъ' in result_word and 'ø' in result_word: # сънø > сан etc.
               fvi = result_word.find('ъ')
            if fvi is not None:
               result_word = insert(result_word, {fvi+1: cstraight})

         result.append(result_word)

      return result

   def process_one_form(
      self,
      current_AP: str,
      stem: str,
      morphChain: MorphemeChain,
      iterative:bool=True
   ) -> List[str]:

      if iterative:
         iterable_form = [stem]
         for submorph in morphChain: # w is submorph in ending, like -ov- and -i in bog-ov-i
            iterable_form = self._append_morpheme(current_AP, iterable_form, submorph)
         return iterable_form
      else:
         return self._append_morpheme(current_AP, [stem], morphChain[0])
