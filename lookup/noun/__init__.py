from re import search as rsearch
from typing import Callable, List, Iterator, Optional, Tuple

from .paradigms import stem_male, stem_female, stem_neutral, male_gen_pl_marked, female_gen_pl_i
from ..charutils import c
from ..paradigm_helpers import AccentedTuple, uniq, nice_name, accentize, append_def, has
from ..pos import PartOfSpeech, Replacement
from ..table import LabeledMultiform
from ..utils import (
   deyerify, decurlyerify, purify, ungarde, compose1, indices, insert, garde,
   expose, last_vowel_index, first_vowel_index, expose_replacement, swap
)


def _apply_neocirk(
   stem:str,
   lvi:Optional[int],
   pvi:Optional[int],
   morpheme:str,
   retraction:int
) -> List[str]: # do not change to Tuple

   """
   neocircumflex is accent retraction from a newly long vowel;
   this function returns only one tuple, unlike _delete_left_bracket
   """

   for _ in range(retraction):
      # word unaccented, has vowels: accentize last vowel
      if c.straight not in stem:
         if lvi is not None:
            stem = insert(stem, {lvi+1: c.straight})
            morpheme = morpheme.replace('·', '') # no further possibilities to accentize it
      elif lvi is not None and pvi is not None:
         stem = stem.replace(c.straight, '') # delete accent mark
         stem = insert(stem, {pvi+1: c.straight}) # add accent mark after pvi
         morpheme = morpheme.replace('·', '')
   return [stem, morpheme]


noun_gpl_transform: Callable[[str], str] = compose1(
   ungarde,
   purify,
   deyerify,
   decurlyerify
)


class Noun(PartOfSpeech):
   def __init__(
      self,
      key:str,
      accented_keys:str,
      kind:str,
      info:str,
      replacements:Tuple[Replacement, ...],
      amendments:Tuple[Replacement, ...]
   ) -> None:
      super().__init__(key, accented_keys, kind, info, replacements, amendments)

      self.trunk = self._trunk()
      self.anim: List[str] = []
      self.suff: List[str] = []

      for paramList in self.gram.MP:
         params = paramList.split(',')
         self.suff = append_def(self.suff, params, ['+', '±'], '_')
         self.anim = append_def(self.anim, params, ['an'], 'in')

   @staticmethod
   def _expose(form:str, yat:str="e", latin:bool=False) -> str:
      return expose(form, yat, latin)

   def _trunk(self) -> List[str]:
      result = []
      keys = self.accented_keys
      for i, AP in enumerate(self.gram.AP):
         accented_noun = garde(accentize(keys[i]))

         if self.label("m") and not self.label('o') and not self.label('a'): # TODO rethink
            trunk_ = accented_noun.replace(c.straight, '')
            accented_trunk_ = accented_noun
         elif self.label("f") and accented_noun.endswith('а'):
            trunk_ = accented_noun.replace(c.straight, '')[:-1]
            accented_trunk_ = accented_noun[:-1]
         elif self.label("f") and accented_noun.endswith('а' + c.straight):
            trunk_ = accented_noun.replace(c.straight, '')[:-1]
            accented_trunk_ = accented_noun[:-2]
         elif self.label("f"):
            trunk_ = accented_noun.replace(c.straight, '')
            accented_trunk_ = accented_noun
         else: # TODO add ime-podne-...
            trunk_ = accented_noun.replace(c.straight, '')[:-1]
            if accented_noun.endswith(c.straight): # zlo
               accented_trunk_ = accented_noun.replace(c.straight, '')[:-1]
            else:
               accented_trunk_ = accented_noun[:-1]
            if accented_noun.endswith('е') and accented_noun[-2] not in 'ђјљњћџчшж':
               trunk_ += 'ʲ'
               accented_trunk_ += 'ʲ'


         if has(AP, *tuple("cdfg")): # c, d, f (?), g are c-like paradigms
            if not self.key.endswith('а'):
               trunk = accented_trunk_.replace(c.straight, '·')
            else:
               fvi = first_vowel_index(trunk_)
               if fvi is None:
                  trunk = trunk_
               else:
                  trunk = insert(trunk_, {fvi: '·'})
         elif has(AP, 'b', 'e', 'q'): # b, e, q are b-like paradigms
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
            raise NotImplementedError(trunk_ + " " + accented_trunk_ + " " + AP)

         trunk = swap(trunk, c.macron, '·')
         trunk = swap(trunk, c.straight, c.macron)
         result.append(trunk)
      return result

   @staticmethod
   def _noun_form_is_possible(
      noun_form:str,
      variation:List[AccentedTuple],
      paradigm:str
   ) -> bool:
      if first_vowel_index(noun_form) != last_vowel_index(noun_form):
         return True
      if not has(paradigm, *tuple('cde0')):
         return True
      if variation not in male_gen_pl_marked:
         return True
      return False

   def _delete_left_bracket(
      self,
      stem:str,
      morpheme:str,
      accent:str,
      current_AP:str
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
         if c.macron in stem:
            if (
               (self.label("f") and current_AP in ('c:', 'g:')) or
               (self.label("m") and current_AP in ('a¿',) and not 'œ' in stem)
            ):
               stem = stem.replace(c.macron, '')

         # 3 handling yers and predefining retractions
         retraction = [0]
         if self.label('m'):
            if (
               has(stem, 'ъ', 'ꚜ') and
               current_AP in accent and
               current_AP == 'b:'
            ):
               retraction = [2, 1] #  Макѐдо̄на̄ца̄ & Македóна̄ца̄
            elif (
               has(stem, 'ъ', 'ꚜ') and
               current_AP in accent and
               current_AP in ('a:', 'c:', 'f.')
            ):
               retraction = [2] # но̏ва̄ца̄
            elif 'd' in current_AP and 'œв' in stem: # у́до̄ва̄
               retraction = [1]
            elif (
               pvi is not None and
               not has(stem, 'ъ', 'ꚜ') and
               current_AP not in accent
            ):
               if current_AP == 'a.':
                  retraction = [1] # је̏зӣка̄
            elif 'b.' in current_AP and 'ъц' in stem and 'œ' in stem:
                  retraction = [1] # о̀че̄ва̄
            elif 'œв' in stem and 'c?' in current_AP:
               retraction = [2, 1, 0] # бо̏го̄ва̄, бо̀го̄ва̄, бого́ва̄
            elif 'œв' in stem and 'b' in current_AP:
               retraction = [2, 1] # гро̏ше̄ва̄ & гро̀ше̄ва̄, би̏ко̄ва̄ & бѝко̄ва̄
         elif self.label('f'):
            if (
               pvi is not None and
               not has(stem, 'ъ', 'ꚜ') and
               current_AP not in accent and
               current_AP not in ('a¡',)
            ):
               retraction = [1] # па̏ртӣја̄
         elif self.label('n'):
            if (
               (current_AP in ('g.', 'b:', 'a.')) or
               # sèlo:sêlа̄, písmo:pîsа̄mа̄, kòleno:kо̏lе̄nа̄
               (
                  current_AP in ('b.','b:') and
                  has(stem, 'ъ', 'ꚜ') and
                  (
                     rsearch('[лрмнвјљњ][ъꚜ]', stem) # NB vesálа̄!
                     or stem.endswith('ц') # nе̏bа̄cа̄
                  )
               )
               # bŕvno: bȑvа̄nа̄, pisàmce:pìsamа̄cа̄, písmo:pîsа̄mа̄
            ):
               retraction = [2]



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
         if not c.macron in stem[lvi:] and lvi is not None:
            stem = swap(insert(stem, {lvi+1: c.macron}), c.macron, '·')

         # 7. if we have neocircumflex retraction, we apply it
         for case in retraction:
            result.append(_apply_neocirk(stem, lvi, pvi, morpheme, case))

      else:
         result = [[stem, morpheme]]

      return [[base, aff.replace('<', '')] for (base, aff) in result]

   def _paradigm_to_forms(
      self,
      i:int,
      length_inconstant:bool,
      yat:str="e",
      latin:bool=False
   ) -> Iterator[LabeledMultiform]:
      """
      Takes the SELF (i.e. whole info about the word) with additional parameters
      and produces the whole inflection table, yielding form by form.
      Still, only one paradigm at a time is produced.
      """

      start_AP = self.gram.AP[i].replace('?', '.')

      declension_is_regular: bool = True
      if self.label("m"):
         lbld_endings = stem_male(self.trunk[i], self.suff[i], self.anim[i]).labeled_endings
      elif self.label("n"): # TODO vreme-ime
         lbld_endings = stem_neutral().labeled_endings
      elif self.label("f"):
         ends_with_a = self.accented_keys[i].endswith('а')
         lbld_endings = stem_female(ends_with_a).labeled_endings
      else:
         lbld_endings = iter([])
         declension_is_regular = False

      if self.label("f") and self.gram.MP[i]: # processing GPl like magli (not **magala)
         form_with_i = [
            noun_gpl_transform(x)
            for x in
            self.process_one_form(self.gram.AP[i], self.trunk[i], female_gen_pl_i)
         ] # curly yer must be deleted BEFORE general deyerifying, so mind the order
         if "i" in self.gram.MP[i]:
            self.replacements["pl gen"] = form_with_i
         elif "j" in self.gram.MP[i]:
            self.amendments["pl gen"] = form_with_i

      if declension_is_regular:
         for label, ending in lbld_endings:
            if label in self.replacements:
               result = [
                  expose_replacement(form, yat, latin)
                  for form in
                  self.replacements[label]
               ]
               yield nice_name(label), uniq(result)

            else:
               ready_forms: List[str] = [] # TODO: better name

               # swapping length in case it is necessary
               to_swap_or_not = ('ø' not in ending[0][0].morpheme and '.' in start_AP)
               noun_form = self.swap(self.trunk[i], to_swap_or_not, self.gram.AP[i], start_AP)

               # after that, iterating by ending variation
               for ending_variation in ending:
                  # processing words like bo / bol (marked with ʟ)
                  if 'ʟ' in noun_form:
                     noun_variants = [noun_form.replace('ʟ', 'ʌ'), noun_form.replace('ʟ', 'л')]
                  # processing kavga : kavgi ~ kavzi (marked with ¦¦)
                  elif '¦¦' in noun_form:
                     noun_variants = [noun_form.replace('¦¦', '¦'), noun_form.replace('¦¦', '')]
                  # processing forms like žet(a)va (marked with ꙏ)
                  elif 'ꙏ' in noun_form:
                     noun_variants = [noun_form.replace('ꙏ', 'ъ'), decurlyerify(noun_form)]
                  # processing forms like akcenat/akcent (marked with Ъ)
                  elif 'Ъ' in noun_form and 'ø' in ending_variation[0].morpheme:
                     noun_variants = [noun_form.replace('Ъ', ''), noun_form.replace('Ъ', 'ꚜ')]
                  else:
                     noun_variants = [noun_form.replace('Ъ', 'ꚜ')]

                  # now iterating by stem (like, akcenat/akcent)

                  for noun_variant in noun_variants:
                     if self._noun_form_is_possible(
                        noun_variant, ending_variation, self.gram.AP[i]
                     ):
                        new_ready_form = self.process_one_form(
                           self.gram.AP[i], noun_variant, ending_variation
                        )
                        ready_forms += new_ready_form

               if label in self.amendments:
                  ready_forms += [
                     expose_replacement(w_form, yat, latin)
                     for w_form in self.amendments[label]
                  ]

               result = [self._expose(form, yat, latin) for form in ready_forms]
               yield nice_name(label), uniq(result)

      else:
         for label, am_forms in self.amendments.items():
            result = [
               self._expose(form, yat, latin)
               for form in
               [expose_replacement(form, yat, latin) for form in am_forms]
            ]
            yield nice_name(label), uniq(result)


   def multiforms(
      self,
      *,
      variant:Optional[int]=None,
      yat:str="e",
      latin:bool=False
   ) -> Iterator[LabeledMultiform]:
      """decline
      Launch _paradigm_to_forms as many times as needed,
      i.e. as many different accentuations a word has.
      """
      for i, _ in enumerate(self.gram.AP):
         if not (variant is not None and variant != i):
            yield from self._paradigm_to_forms(
               i=i,
               length_inconstant=False,
               yat=yat,
               latin=latin
            )
