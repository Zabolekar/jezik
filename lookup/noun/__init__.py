from re import sub as rsub
from typing import Callable, Dict, List, Iterator, Optional, Tuple
from ..pos import PartOfSpeech, Replacement
from ..utils import (
   deyerify, indices, insert, garde, ungarde, expose,
   last_vowel_index, first_vowel_index, expose_replacement
   )
from ..paradigm_helpers import (
   AccentedTuple, MorphemeChain, OrderedSet, nice_name, oa, accentize, appendDef
   )
from ..table import LabeledMultiform
from .paradigms import c_m, c_f, NounStem, male_gen_pl_marked, female_gen_pl_i
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
      accented_keys: str,
      kind: str,
      info: str,
      replacements: Tuple[Replacement, ...],
      amendments: Tuple[Replacement, ...]
   ) -> None:
      super().__init__(key, accented_keys, kind, info, replacements, amendments)

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
      keys = self.accented_keys
      for i, AP in enumerate(self.gram.AP):
         accented_noun = garde(accentize(keys[i]))
         if self.label("m") and not self.label('o') and not self.label('a'): # TODO rethink
            trunk_ = accented_noun.replace(cstraight, '')
            accented_trunk_ = accented_noun
         elif self.label("f") and accented_noun.endswith('а'):
            trunk_ = accented_noun.replace(cstraight, '')[:-1]
            accented_trunk_ = accented_noun[:-1]
         elif self.label("f") and accented_noun.endswith('а' + cstraight):
            trunk_ = accented_noun.replace(cstraight, '')[:-1]
            accented_trunk_ = accented_noun[:-2]
         elif self.label("f"):
            trunk_ = accented_noun.replace(cstraight, '')
            accented_trunk_ = accented_noun
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
      if first_vowel_index(noun_form) != last_vowel_index(noun_form):
         return True
      if all(x not in paradigm for x in 'cde0'):
         return True
      if variation not in male_gen_pl_marked:
         return True
      return False

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
       ...
       without yers, in cases like jèzik : jȅzīkā:
       stem has no mobile vowel, stem is accented,
       word is not feminine, accented vowel is not the first one
      """
      result = []
      if morpheme.startswith('<'): # so far only '-ā' is like that

         # 1. finding vowel places that will be of importance
         lvi, _, pvi = indices(stem)

         # 2 handling óvca > ovácā and óvan > ovánā
         if cmacron in stem:
            if (self.label("f") and current_AP in ('c:', 'g:')) \
               or (self.label("m") and current_AP in ('a¿') and not 'œ' in stem):
               stem = stem.replace(cmacron, '')

         # 3 handling yers and predefining retractions
         retraction = [0]
         if self.label('m'):
            if ('ъ' in stem or 'ꚜ' in stem) and current_AP in accent and current_AP == 'b:':
               retraction = [2, 1] #  Макѐдо̄на̄ца̄ & Македóна̄ца̄
            elif ('ъ' in stem or 'ꚜ' in stem) and current_AP in accent and current_AP in ('a:',  'c:', 'f.'):
               retraction = [2] # но̏ва̄ца̄
            elif 'd' in current_AP and 'œв' in stem: # у́до̄ва̄
               retraction = [1]
            elif pvi is not None and 'ъ' not in stem and 'ꚜ' not in stem \
               and current_AP not in accent:
               if current_AP == 'a.':
                  retraction = [1] # је̏зӣка̄
            elif 'b.' in current_AP and 'ъц' in stem and 'œ' in stem:
                  retraction = [1] # о̀че̄ва̄
            elif 'œв' in stem and 'c?' in current_AP:
               retraction = [2, 1, 0] # бо̏го̄ва̄, бо̀го̄ва̄, бого́ва̄
            elif 'œв' in stem and 'b' in current_AP: #and 'ъ' not in stem and 'ꚜ' not in stem:
               retraction = [2, 1] # гро̏ше̄ва̄ & гро̀ше̄ва̄, би̏ко̄ва̄ & бѝко̄ва̄
         elif self.label('f'):
            if pvi is not None and 'ъ' not in stem and 'ꚜ' not in stem \
               and current_AP not in accent and current_AP not in ('a¡'):
               retraction = [1] # па̏ртӣја̄

         if not 'œ' in stem: # TODO one day think about better condition
            stem = stem.replace('ъ', 'а').replace('ꚜ', 'а')
         else:
            stem = deyerify(stem)

         # 4. a renewed set of indices, since ъ/ꚜ has become а
         lvi, _, pvi = indices(stem)

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

      declension_is_regular: bool = True
      if self.label("m"):
         lbld_endings = c_m(self.trunk[i], self.suff[i], self.anim[i]).labeled_endings
      elif self.label("f"):
         lbld_endings = c_f(self.trunk[i], self.accented_keys[i].endswith('а')).labeled_endings
      else:
         lbld_endings = iter([])
         declension_is_regular = False

      if self.label("f") and self.gram.MP[i]: # processing GPl like magli (not **magala)
         form_with_i = [ungarde(deyerify(x)) for x in
            self.process_one_form(self.gram.AP[i], self.trunk[i], female_gen_pl_i)
         ]
         if "i" in self.gram.MP[i]:
            self.replacements["pl gen"] = form_with_i
         elif "j" in self.gram.MP[i]:
            self.amendments["pl gen"] = form_with_i

      if declension_is_regular:
         for label, ending in lbld_endings:
            if label in self.replacements:
               result = [expose_replacement(form, yat, latin) for form in self.replacements[label]]
               yield nice_name(label), list(OrderedSet(result))

            else:
               ready_forms: List[str] = [] # TODO: better name

               # swapping length in case it is necessary
               to_swap_or_not = ('ø' not in ending[0][0].morpheme and '.' in start_AP)
               noun_form = self.swap(self.trunk[i], to_swap_or_not, self.gram.AP[i], target_AP)

               # after that, iterating by ending variation
               for ending_variation in ending:
                  # processing words like bo / bol (marked with ʟ)
                  if 'ʟ' in noun_form:
                     noun_variants = [noun_form.replace('ʟ', 'ʌ'), noun_form.replace('ʟ', 'л')]
                  # processing kavga : kavgi ~ kavzi (marked with ¦¦)
                  elif '¦¦' in noun_form:
                     noun_variants = [noun_form.replace('¦¦', '¦'), noun_form.replace('¦¦', '')]
                  # processing forms like žet(a)va
                  elif 'ꙏ' in noun_form:
                     noun_variants = [
                        noun_form.replace('ꙏ', 'ъ'),
                        rsub('([лмнрјв]ꙏ)', f'{cmacron}\\1', noun_form).replace('ꙏ', '')
                     ]
                  # processing forms like akcenat/akcent (marked with Ъ)
                  elif 'Ъ' in noun_form and 'ø' in ending_variation[0].morpheme:
                     noun_variants = [noun_form.replace('Ъ', ''), noun_form.replace('Ъ', 'ꚜ')]
                  else:
                     noun_variants = [noun_form.replace('Ъ', 'ꚜ')]

                  # now iterating by stem (like, akcenat/akcent)

                  for noun_variant in noun_variants:
                     if self._noun_form_is_possible(
                        noun_variant, ending_variation, self.gram.AP[i]):
                        new_ready_form = self.process_one_form(
                           self.gram.AP[i], noun_variant, ending_variation)
                        ready_forms += new_ready_form

               if label in self.amendments:
                  ready_forms += [
                     expose_replacement(w_form, yat, latin)
                     for w_form in self.amendments[label]
                  ]

               result = [self._expose(form, yat, latin) for form in ready_forms]
               yield nice_name(label), list(OrderedSet(result))

      else:
         for label, am_forms in self.amendments.items():
            result = [
               self._expose(form, yat, latin)
               for form in
               [expose_replacement(form, yat, latin) for form in am_forms]
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
      for i, _ in enumerate(self.gram.AP):
         if not (variant is not None and variant != i):
            yield from self._paradigm_to_forms(i, False, yat, latin)
