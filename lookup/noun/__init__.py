from typing import Dict, List, Iterator, Optional, Tuple
from copy import deepcopy
from ..pos import PartOfSpeech, Replacement
from ..utils import insert, garde, expose, last_vowel_index, first_vowel_index, expose_replacement
from ..paradigm_helpers import AccentedTuple, OrderedSet, nice_name, oa, accentize
from ..table import LabeledMultiform
from .paradigms import c_m
from ..charutils import cmacron, cstraight

class Noun(PartOfSpeech):
   def __init__(
      self,
      key: str, 
      kind: str, 
      info: str, 
      replacements: Tuple[Replacement, ...],
      yat:str="ekav") -> None:
      super().__init__(key, kind, info, replacements, yat)

      self.trunk = self._trunk()
      self.anim: List[str] = []
      self.suff: List[str] = []
      for x in self.gram.MP:
         y = x.split(',')
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

      for i, AP in enumerate(self.gram.AP):

         accented_noun = garde(accentize(self.key, self.gram.accents[i].r, self.gram.accents[i].v))

         if 'm' in self.gram.other and not 'o' in self.gram.other:
            trunk_ = accented_noun.replace(cstraight, '')
            # self.key is useless here; accented_noun has not only stress place,
            # it has also all the lengths in the stem which surely are of importance
            accented_trunk_ = accented_noun
         else:
            trunk_ = accented_noun.replace(cstraight, '')[:-1]
            accented_trunk_ = accented_noun[:-1]

         if 'c' in AP or 'd' in AP: # c, d are c-like paradigms
            if not self.key.endswith('а'):
               trunk = accented_trunk_.replace(cstraight, '·')
            else:
               fvi = first_vowel_index(trunk_)
               if fvi is None:
                  trunk = trunk_
               else:
                  trunk = insert(trunk_, {fvi: '·'})
         elif any([x in AP for x in 'beq']): # b, e, q are b-like paradigms
            lvi = last_vowel_index(trunk_)
            if lvi is None:
               trunk = trunk_
            else:
               trunk = insert(trunk_, {lvi+1: '·'})
         elif 'a' in AP: # a is a-like paradigm; 'o' is unused in nouns
            trunk = accented_trunk_
         else:
            raise NotImplementedError
         trunk = trunk.replace(f'{cmacron}·', f'·{cmacron}')
         trunk = trunk.replace(f'{cstraight}{cmacron}', f'{cmacron}{cstraight}')
         result.append(trunk)
      return result

   def _noun_form_is_possible(
      self,
      noun_form: str,
      variation: List[AccentedTuple],
      paradigm: str) -> bool:
      return (first_vowel_index(noun_form) != last_vowel_index(noun_form)
               or all([x not in paradigm for x in 'cde'])
               or (variation != [AccentedTuple(f'<а·{cmacron}', 'b.b:')]
               and variation != [AccentedTuple(f'<а·{cmacron}', 'b.b:e:')]))
               # this is the ā which is NOT accented in a. p. c

   def process_one_form(
      self,
      i: int, 
      noun_variant: str,
      ending_variation: List[AccentedTuple]) -> List[str]:

      iterable_noun_variant = [deepcopy(noun_variant)]
      current_AP = self.gram.AP[i]
      for w in ending_variation: # w is submorph in ending, like -ov- and -i in bog-ov-i
         iterable_noun_variant = self._append_morpheme(current_AP, iterable_noun_variant, w)
         for nnv in iterable_noun_variant:
            nnv = self.accentize(current_AP, nnv)
      return iterable_noun_variant

   def _paradigm_to_forms(self, i: int, length_inconstancy: bool, yat:str="ekav") -> Iterator[LabeledMultiform]:
      # TODO: length inconstancy currently not used
      # however, Svetozar says he will use it later
      start_AP = self.gram.AP[i].replace('?', '.')
      target_AP = self.gram.AP[i].replace('?', '.')      
      
      for label, ending in c_m(self.trunk[i], self.suff[i], self.anim[i]).labeled_endings:

         if label in self.replacements:
            yield nice_name(label), \
               list(
                  OrderedSet(
                     [expose_replacement(w_form, yat) for w_form in self.replacements[label]]
                     )
                  )
         
         else:

            ready_forms: List[str] = [] # TODO: better name

            # swapping length in case it is necessary
            to_swap_or_not = ('ø' not in ending[0][0].morpheme)
            noun_form = self.swap(self.trunk[i], to_swap_or_not, start_AP, target_AP) 

            # after that, iterating by ending variation
            for ending_variation in ending:

               # processing words like bo / bol (marked with ʟ)
               if 'ʟ' in noun_form:
                  noun_variants = [noun_form.replace('ʟ', 'ʌ'), noun_form.replace('ʟ', 'л')]
               # processing forms like akcenat/akcent (marked with Ъ)       
               elif 'Ъ' in noun_form and 'ø' in ending_variation[0].morpheme:
                  noun_variants = [noun_form.replace('Ъ', ''), noun_form.replace('Ъ', 'ъ')]
               else:
                  noun_variants = [noun_form.replace('Ъ', 'ъ')]

               # now iterating by stem (like, akcenat/akcent)

               for noun_variant in noun_variants:
                  if self._noun_form_is_possible(noun_variant, ending_variation, self.gram.AP[i]):
                     ready_forms += self.process_one_form(i, noun_variant, ending_variation)
            yield nice_name(label), \
               list(
                  OrderedSet(
                     [self._expose(w_form, yat) for w_form in ready_forms]
                     )
                  )

   def multiforms(self, *, variant: Optional[int] = None, yat:str="ekav") -> Iterator[LabeledMultiform]:
      """decline"""
      for i, AP in enumerate(self.gram.AP):
         if not (variant is not None and variant != i):
            yield from self._paradigm_to_forms(i, False, yat)
