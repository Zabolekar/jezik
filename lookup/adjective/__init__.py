from typing import Dict, List, Iterator, Optional, Tuple
import re
from ..table import LabeledMultiform
from ..pos import PartOfSpeech, Replacement
from ..utils import insert, garde, expose, last_vowel_index, expose_replacement
from ..paradigm_helpers import AccentedTuple, nice_name, oa, accentize, uniq
from .paradigms import AdjParadigm, short_adj, long_adj, mixed_adj
from ..charutils import cmacron, cstraight

adj_AP_pairs = (
   ('a.,a.', 'A.'),
   ('0,a.', 'a.'),
   ('a:,a:', 'A:'),
   ('b:,b:', 'B:'),
   ('0,a:', 'a:'),
   ('0,c.', 'c.'),
   ('b.,b.', 'B.'),
   ('b.,c.', 'K.'),
   ('0,c:', 'c:'),
   ('b:,c.', 'K:.'),
   ('a.,c.', 'L.'),
   ('b?,b.', 'B?.'),
   ('a.,a:', 'A.:'),
   ('d:,b:', 'M:'),
   ('d.,b.', 'M.'),
   ('b:,c:', 'K:'),
   ('a:,c.', 'L:.'),
   ('b.,b:', 'B.:'),
   ('d.,c.', 'N.')
)  # rules: 0,x is x; x,x is X; bc ac db dc become KLMN;
   # leave one length mark if they are the same,
   # two length marks if they are different

adj_AP_to_inner_AP = {b:a for a,b in adj_AP_pairs}

class Adjective(PartOfSpeech):
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
      
      inner_APs = [adj_AP_to_inner_AP[AP].split(',') for AP in self.gram.AP]
      self.short_AP, self.long_AP = zip(*inner_APs)

      self.trunk = self._trunk()

   # different
   @staticmethod
   def _expose(form:str, yat:str="e", latin:bool=False) -> str:
      return expose(form, yat, latin)

   # different for Verb and Adjective
   def _trunk(self) -> List[str]:
      result = []

      for number, item in enumerate(self.accented_keys):
         accented_adj = garde(accentize(item))

         if self.label('ov'):
            trunk = accented_adj
         elif self.label('all'):
            if 'ъ' + cstraight in accented_adj:
               trunk = accented_adj[:-2] + accented_adj[-1]
            else:
               trunk = accented_adj
         elif self.label('ski'):
            trunk = re.sub(f'{cmacron}{cstraight}$', cmacron, accented_adj)[:-2]
         if not 'a' in self.gram.AP[number]:
            lvi = last_vowel_index(trunk)
            if lvi is None:
               #raise ValueError(f"{trunk} does not contain any vowels")
               pass
            else:
               if lvi > -1:
                  trunk = insert(trunk, {lvi + 1: '·'})
         result.append(trunk)
      return result

   # Adjective-specific. Verb has its own
   @staticmethod
   def _adj_form_is_possible(adj_form:str) -> bool:
      return re.search('[њљћђшжчџјʲ]œ.+ме$', adj_form) is None

   # Adjective-only. Verb should have its own one
   def _paradigm_to_forms(
      self,
      paradigm:AdjParadigm,
      i:int,
      length_inconstant:bool,
      yat:str="e",
      latin:bool=False
   ) -> Iterator[LabeledMultiform]:
      """
      Current subparadigm: short or long AP (they behave differently)
      i: index of the variation (by variation we mean things like зу̑бнӣ зу́бнӣ)
      """
      current_AP = self.short_AP[i] if paradigm is short_adj else self.long_AP[i]

      adj_form = self.swap(
         trunk=self.trunk[i],
         length_inconstant=length_inconstant,
         AP=current_AP,
         target_AP=self.short_AP[i]
      )

      for label, ending in zip(paradigm._fields, paradigm):

         if label in self.replacements:
            result = [
               expose_replacement(w_form, yat, latin) 
               for w_form in self.replacements[label]
            ]
            yield nice_name(label), uniq(result)

         else:
            ready_forms: List[str] = []
            for variation in ending: # e.g. -om, -ome, -omu
               if 'ʟ' in adj_form:
                  adj_variants = [adj_form.replace('ʟ', 'ʌ'), adj_form.replace('ʟ', 'л')]
               else:
                  adj_variants = [adj_form]
               for adj_variant in adj_variants:
                  if self._adj_form_is_possible(adj_variant + variation.morpheme):
                     ready_forms += self.process_one_form(
                        current_AP=current_AP,
                        stem=adj_variant,
                        morphChain=[variation],
                        iterative=False
                     )

            if label in self.amendments:
               ready_forms += [
                  expose_replacement(w_form, yat, latin)
                  for w_form in self.amendments[label]
               ]
            result = [self._expose(w_form, yat, latin) for w_form in ready_forms]
            yield nice_name(label), uniq(result)

   def multiforms(
      self,
      *,
      variant:Optional[int]=None,
      yat:str="e",
      latin:bool=False
   ) -> Iterator[LabeledMultiform]:
      """decline"""
      endings = self.gram.other[0]
      MPs: List[AdjParadigm]
      if endings == "all":
         MPs = [short_adj, long_adj]
      elif endings == "ski":
         MPs = [long_adj]
      elif endings == "ov":
         MPs = [mixed_adj]

      for i, AP in enumerate(self.gram.AP):
         # variant = None means all variants
         if not(variant is not None and variant != i):
            length_inconstant = False

            if endings == "all":
               if self.short_AP[i][-1] != self.long_AP[i][-1]:
                  length_inconstant = True
            for paradigm in MPs:
               yield from self._paradigm_to_forms(
                  paradigm,
                  i, 
                  length_inconstant,
                  yat,
                  latin
               )
