from typing import Callable, Dict, List, Iterator, Optional, Tuple
from ..pos import PartOfSpeech, Replacement
from ..utils import deyerify, indices, insert, garde, expose, last_vowel_index, first_vowel_index, expose_replacement
from ..paradigm_helpers import AccentedTuple, MorphemeChain, OrderedSet, nice_name, oa, accentize, appendDef
from ..table import LabeledMultiform
from .paradigms import c_m, c_f, NounStem, male_gen_pl_marked
from ..charutils import cmacron, cstraight

def _apply_neocirk(
   stem: str,
   lvi: Optional[int],
   pvi: Optional[int],
   morpheme: str,
   retraction: int
) -> List[str]: # do not change to Tuple

   """ neocircumflex is accent retraction from a newly long vowel;
   this function returns only one tuple, unlike _delete_left_bracket"""

   for _ in range(retraction):
      # word unaccented, has vowels: accentize last vowel
      if cstraight not in stem:
         if lvi is not None:
            stem = insert(stem, {lvi+1: cstraight})
            morpheme = morpheme.replace('·', '') # no further possibilities to accentize it
      elif lvi is not None and pvi is not None:
         stem = stem.replace(cstraight, '') # delete accent mark
         stem = insert(stem, {pvi+1: cstraight}) # add accent mark after pvi
         morpheme = morpheme.replace('·', '')
      #else:
         #raise IndexError(f"{stem} has not enough vowels for this operation")
   return [stem, morpheme]

class Noun(PartOfSpeech):
   def __init__(
      self,
      key: str,
      kind: str,
      info: str,
      replacements: Tuple[Replacement, ...],
      amendments: Tuple[Replacement, ...]
   ) -> None:
      super().__init__(key, kind, info, replacements, amendments)

      self.trunk = self._trunk()
      self.anim: List[str] = []
      self.suff: List[str] = []
      for paramList in self.gram.MP:
         params = paramList.split(',')
         self.suff = appendDef(self.suff, params, ['+', '±'], '_')
         self.anim = appendDef(self.anim, params, ['an'], 'in')

   @staticmethod
   def _expose(form: str, yat:str="e", latin:bool=False) -> str:
      return expose(form, yat, latin)

   def _trunk(self) -> List[str]:
      result = []

      for i, AP in enumerate(self.gram.AP):
         accented_noun = garde(accentize(self.key, self.gram.accents[i].r, self.gram.accents[i].v))
         if self.label("m") and not self.label('o'):
            trunk_ = accented_noun.replace(cstraight, '')
            # self.key is useless here; accented_noun has not only stress place,
            # it has also all the lengths in the stem which surely are of importance
            accented_trunk_ = accented_noun
         elif self.label("f") and accented_noun.endswith('а'): # TODO How do we call zlost-like f ang sluga-like m?
            trunk_ = accented_noun.replace(cstraight, '')[:-1]
            accented_trunk_ = accented_noun[:-1]
         elif self.label("f") and accented_noun.endswith(cstraight):
            trunk_ = accented_noun.replace(cstraight, '')[:-1]
            accented_trunk_ = accented_noun[:-2]
         else:
            trunk_ = accented_noun.replace(cstraight, '')[:-1]
            accented_trunk_ = accented_noun[:-1]

         if any(x in AP for x in 'cdfg'): # c, d, f (?), g are c-like paradigms
            if not self.key.endswith('а'):
               trunk = accented_trunk_.replace(cstraight, '·')
            else:
               fvi = first_vowel_index(trunk_)
               if fvi is None:
                  trunk = trunk_
               else:
                  trunk = insert(trunk_, {fvi: '·'})
         elif any(x in AP for x in 'beq'): # b, e, q are b-like paradigms
            lvi = last_vowel_index(trunk_)
            if lvi is None:
               trunk = trunk_
            else:
               trunk = insert(trunk_, {lvi+1: '·'})
         elif 'a' in AP: # a is a-like paradigm; 'o' is unused in nouns
            trunk = accented_trunk_
         elif '0' in AP: # 0 means that all forms are prescribed, not generated
            trunk = accented_trunk_
         else:
            raise NotImplementedError
         trunk = trunk.replace(f'{cmacron}·', f'·{cmacron}')
         trunk = trunk.replace(f'{cstraight}{cmacron}', f'{cmacron}{cstraight}')
         result.append(trunk)
      return result

   @staticmethod
   def _noun_form_is_possible(
      noun_form: str,
      variation: List[AccentedTuple],
      paradigm: str
   ) -> bool:
      return (first_vowel_index(noun_form) != last_vowel_index(noun_form)
               or all(x not in paradigm for x in 'cde0')
               or (variation not in male_gen_pl_marked))
               # this is the ā which is NOT accented in a. p. c
               # TODO better make it a variable in Paradigms and import it here

   def _delete_left_bracket(
      self,
      stem: str,
      morpheme: str,
      accent: str,
      current_AP: str
   ) -> List[List[str]]:
      """
      This function is so far for nouns only.
      It explicitly uses noun AP names.
      handling yers and defining if the word has neocircumflex:
       if morpheme is genitive -ā,
       stem has mobile vowel, ending is accented,
       gender is not feminine (i.e. m/n),
       and, at last, word is not komunizam-like exception (a.p. q),
       then word DOES have neocircumflex retraction
       and yer is FORCEDLY clarified to an 'a' sound;
       other yers will be handled afterwards by the common yer rule
      
       without yers, in cases like jèzik : jȅzīkā:
       stem has no mobile vowel, stem is accented,
       word is not feminine, accented vowel is not the first one
      """
      result = []
      if morpheme.startswith('<'): # so far only '-ā' is like that

         # 1. finding vowel places that will be of importance
         lvi, fvi, pvi = indices(stem)

         # 2 handling óvca > ovácā
         if cmacron in stem and self.label("f") and current_AP in ('c:', 'g:'):
            stem = stem.replace(cmacron, '')

         # 3 handling yers and predefining retractions
         retraction = [0]
         if self.label('m'):
            if 'ъ' in stem and current_AP in accent \
               and current_AP in ['a:', 'b:', 'c:', 'f.']:
               retraction = [2] # Макѐдо̄на̄ца̄, но̏ва̄ца̄
            elif (('d' in current_AP and 'œв' in stem)
               or (pvi is not None and 'ъ' not in stem \
               and current_AP not in accent \
               and (current_AP in ['a.', 'a!']) \
               or ('b.' in current_AP and 'ъ' in stem and 'œ' in stem))):
               retraction = [1] # је̏зӣка̄, а̀ма̄не̄та̄, о̀че̄ва̄
            elif 'œв' in stem and 'c?' in current_AP:
               retraction = [2, 1, 0] # бо̏го̄ва̄, бо̀го̄ва̄, бого́ва̄
            elif 'œв' in stem and 'b' in current_AP and not 'ъ' in stem:
               retraction = [2, 1] # гро̏ше̄ва̄ & гро̀ше̄ва̄, би̏ко̄ва̄ & бѝко̄ва̄

         if not 'œ' in stem: # TODO one day think about better condition
            stem = stem.replace('ъ', 'а')
         else:
            stem = deyerify(stem)

         # 4. a renewed set of indices, since ъ has become а
         lvi, fvi, pvi = indices(stem)

         # 5. handling strange new exceptions like komunizam
         if '·' in stem and current_AP == 'q.' and lvi is not None:
            stem = insert(stem.replace('·', ''), {lvi: '·'})

         # 6. we insert macron after lvi if last vowel is short
         if not cmacron in stem[lvi:] and lvi is not None:
            stem = insert(stem, {lvi+1: cmacron}).replace(f'{cmacron}·', f'·{cmacron}')

         # 7. if we have neocircumflex retraction, we apply it
         for case in retraction:
            result.append(_apply_neocirk(stem, lvi, pvi, morpheme, case))

      else:
         result = [[stem, morpheme]]

      return [[x[0], x[1].replace('<', '')] for x in result]

   def _paradigm_to_forms(
      self,
      i:int,
      length_inconstancy:bool,
      yat:str="e",
      latin:bool=False
   ) -> Iterator[LabeledMultiform]:

      start_AP = self.gram.AP[i].replace('?', '.')
      target_AP = self.gram.AP[i].replace('?', '.')

      declension_type: Optional[Callable[[str, str, str], NounStem]]
      if self.label("m"):
         declension_type = c_m
      elif self.label("f"):
         declension_type = c_f
      else:
         declension_type = None

      if declension_type is not None:
         for label, ending in declension_type(self.trunk[i], self.suff[i], self.anim[i]).labeled_endings:

            if label in self.replacements:
               result = [expose_replacement(form, yat, latin) for form in self.replacements[label]]
               yield nice_name(label), list(OrderedSet(result))

            else:

               ready_forms: List[str] = [] # TODO: better name

               # swapping length in case it is necessary
               to_swap_or_not = ('ø' not in ending[0][0].morpheme and '.' in start_AP)
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
                        ready_forms += self.process_one_form(self.gram.AP[i], noun_variant, ending_variation)

               if label in self.amendments:
                  ready_forms += [expose_replacement(w_form, yat, latin) for w_form in self.amendments[label]]

               result = [self._expose(form, yat, latin) for form in ready_forms]
               yield nice_name(label), list(OrderedSet(result))

      else:
         for label in self.amendments:
            result = [
               self._expose(form, yat, latin)
               for form in
               [expose_replacement(form, yat, latin) for form in self.amendments[label]]
            ]
            yield nice_name(label), list(OrderedSet(result))


   def multiforms(
      self,
      *,
      variant: Optional[int] = None,
      yat:str="e",
      latin:bool=False
   ) -> Iterator[LabeledMultiform]:
      """decline"""
      for i, AP in enumerate(self.gram.AP):
         if not (variant is not None and variant != i):
            yield from self._paradigm_to_forms(i, False, yat, latin)
