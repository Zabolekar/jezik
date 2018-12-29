from typing import Any, Dict, List, Iterator, Optional
from copy import deepcopy
from ..pos import PartOfSpeech
from ..utils import insert, garde, expose, last_vowel_index, first_vowel_index
from ..paradigm_helpers import AccentedTuple, OrderedSet, nice_name, oa, accentize
from ..table import LabeledMultiform
from .paradigms import c_m

class Noun(PartOfSpeech):
   def __init__(self, key: str, value: Dict[str, Any], yat:str="ekav") -> None:
      super().__init__(key, value, yat)

      self.trunk = self._trunk()
      self.anim: List[str] = []
      self.suff: List[str] = []
      self.vocative: List[str] = []
      for x in self.info.MP:
         y = x.split(',')
         if 'u' in y:
            self.vocative.append('u')
         elif 'ue' in y:
            self.vocative.append('ue')
         else:
            self.vocative.append('e')
         if '+' in y:
            self.suff.append('+')
         elif '±' in y:
            self.suff.append('±')
         else:
            self.suff.append('_')
         if 'an' in y:
            self.anim.append('an')
         else:
            self.anim.append('in')

   def _expose(self, form: str, yat:str="ekav") -> str:
      return expose(form, yat)

   def _trunk(self) -> List[str]:
      result = []

      for i, AP in enumerate(self.info.AP):

         accented_noun = garde(accentize(self.key, self.info.accents[i].r, self.info.accents[i].v))

         if 'm' in self.info.other and not 'o' in self.info.other:
            trunk_ = accented_noun.replace('\u030d', '')
            # self.key is useless here; accented_noun has not only stress place,
            # it has also all the lengths in the stem which surely are of importance
            accented_trunk_ = accented_noun
         else:
            trunk_ = accented_noun.replace('\u030d', '')[:-1]
            accented_trunk_ = accented_noun[:-1]

         if 'c' in AP or 'd' in AP: # c, d are c-like paradigms
            if not self.key.endswith('а'):
               trunk = accented_trunk_.replace('\u030d', '·')
            else:
               fvi = first_vowel_index(trunk_)
               if fvi is None:
                  trunk = trunk_
               else:
                  trunk = insert(trunk_, {fvi: '·'})
         elif 'b' in AP or 'e' in AP or 'q' in AP: # b, e, q are b-like paradigms
            lvi = last_vowel_index(trunk_)
            if lvi is None:
               trunk = trunk_
            else:
               trunk = insert(trunk_, {lvi+1: '·'})
         elif 'a' in AP: # a is a-like paradigm; 'o' is unused in nouns
            trunk = accented_trunk_
         else:
            raise NotImplementedError
         trunk = trunk.replace('\u0304·', '·\u0304')
         trunk = trunk.replace('\u030d\u0304', '\u0304\u030d')
         result.append(trunk)
      return result

   def _noun_form_is_possible(self, noun_form: str, variation: AccentedTuple, paradigm: str):
      return not(first_vowel_index(noun_form) == last_vowel_index(noun_form)
                 and ('c' in paradigm or 'd' in paradigm)
                 and variation == [AccentedTuple('<а·\u0304', 'b.b:e:')])
                 # this is the ā which is NOT accented in a. p. c

   def process_one_form(self, i: str, noun_variant: str, ending_variation: List[AccentedTuple]) -> List[str]:

      iterable_noun_variant = [deepcopy(noun_variant)]
      for w in ending_variation: # w is submorph in ending, like -ov- and -i in bog-ov-i
         iterable_noun_variant = self._append_morpheme(self.info.AP[i], iterable_noun_variant, w)
         for nnv in iterable_noun_variant:
            nnv = self.accentize(i, nnv)
      return iterable_noun_variant

   def _paradigm_to_forms(self, i, length_inconstancy, yat:str="ekav"):

      start_AP = self.info.AP[i].replace('?', '.')
      target_AP = self.info.AP[i].replace('?', '.')      
      
      for label, ending in c_m(self.suff[i], self.anim[i], self.vocative[i]).labeled_endings:

         ready_forms: List[str] = [] # TODO: better name

         # swapping length in case it is necessary
         to_swap_or_not = ('ø' not in ending[0][0].morpheme)
         noun_form = self.swap(self.trunk[i], to_swap_or_not, start_AP, target_AP) 

         # after that, iterating by ending variation
         for ending_variation in ending:

            # processing forms like akcenat/akcent (marked with Ъ)

            if 'Ъ' in noun_form and 'ø' in ending_variation[0].morpheme:
               noun_variants = [noun_form.replace('Ъ', ''), noun_form.replace('Ъ', 'ъ')]
            else:
               noun_variants = [noun_form.replace('Ъ', 'ъ')]

            # now iterating by stem (like, akcenat/akcent)

            for noun_variant in noun_variants:
               if self._noun_form_is_possible(noun_variant, ending_variation, self.info.AP[i]):
                  ready_forms += self.process_one_form(i, noun_variant, ending_variation)
         yield nice_name(label), list(OrderedSet([self._expose(w_form, yat) for w_form in ready_forms]))

   def multiforms(self, *, variant: Optional[int] = None, yat:str="ekav") -> Iterator[LabeledMultiform]:
      """decline"""
      for i, AP in enumerate(self.info.AP):
         if not (variant is not None and variant != i):
            yield from self._paradigm_to_forms(i, False, yat)
