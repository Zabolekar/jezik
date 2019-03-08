from typing import Dict, List, Iterator, Optional
from copy import deepcopy
import re
from ..table import LabeledMultiform
from ..pos import PartOfSpeech
from ..utils import insert, garde, expose, last_vowel_index
from ..paradigm_helpers import AccentedTuple, nice_name, oa, accentize
from .paradigms import AdjParadigm, short_adj, long_adj, mixed_adj

class Adjective(PartOfSpeech):
   def __init__(self, key: str, kind: str, info: str, yat:str="ekav") -> None:
      super().__init__(key, kind, info, yat)
      # TODO: Adjective-only: zipping the APs to 2 lists. But is it really necessary?
      self.short_AP, self.long_AP = list(zip(*[AP.split(',') for AP in self.gram.AP]))

      self.trunk = self._trunk() #both but not separable

   # different
   def _expose(self, form: str, yat:str="ekav") -> str:
      return expose(form, yat)

   # different for Verb and Adjective
   def _trunk(self) -> List[str]:
      result = []

      for number, item in enumerate(self.gram.AP):
         accented_adj = garde(accentize(self.key, self.gram.accents[number].r, self.gram.accents[number].v))
         if 'ov' in self.gram.other:
            trunk = accented_adj
         elif 'all' in self.gram.other:
            if 'ъ\u030d' in accented_adj:
               trunk = accented_adj[:-2] + accented_adj[-1]
            else:
               trunk = accented_adj
         elif 'ski' in self.gram.other:
            trunk = re.sub('\u0304\u030d$', '\u0304', accented_adj)[:-2]
         if not 'a' in self.gram.AP[number]:
            lvi = last_vowel_index(trunk)
            if lvi is None:
               #raise ValueError(f"{trunk} does not contain any vowels")
               pass
            else:
               if lvi > -1:
                  to_insert = lvi + 1
                  trunk = insert(trunk, {to_insert: '·'})
         result.append(trunk)
      return result

   # Adjective-specific. Verb has its own one
   def _adj_form_is_possible(self, adj_form: str) -> bool:
      return re.search('[њљћђшжчџјṕ]œ.ме$', adj_form) is None

   def process_one_form(self, current_AP: str, adj_variant: str, ending_variation: AccentedTuple) -> str:
      result = self._append_morpheme(current_AP, [adj_variant], ending_variation)[0] # no iterability in adjectives
      #result = self.accentize(current_AP, result) # TODO: why not? can we unify it somehow in future?
      return result

   # Adjective-only. Verb should have its own one 
   def _paradigm_to_forms(self, paradigm: AdjParadigm, i: int, length_inconstant: bool, yat:str="ekav") -> Iterator[LabeledMultiform]:
      """
      Current subparadigm: short or long AP (they behave differently)
      i: index of the variation (by variation we mean things like зу̑бнӣ зу́бнӣ)
      """
      current_AP = self.short_AP[i] if paradigm is short_adj else self.long_AP[i]
      adj_form = self.swap(self.trunk[i], length_inconstant, current_AP, self.long_AP[i])

      for label, ending in zip(paradigm._fields, paradigm):
         ready_forms = []
         for variation in ending: # e.g. -om, -ome, -omu
            new_adj_form = self.process_one_form(current_AP, adj_form, variation)
            if self._adj_form_is_possible(new_adj_form):
               ready_forms.append(new_adj_form)
            
         yield nice_name(label), [self._expose(w_form, yat) for w_form in ready_forms]

   def multiforms(self, *, variant: Optional[int] = None, yat:str="ekav") -> Iterator[LabeledMultiform]:
      """decline"""
      endings = self.gram.other[0]
      MPs: List[AdjParadigm]
      if endings == "all":
         MPs = [short_adj, long_adj]
      elif endings == "ski":
         MPs = [long_adj]
      elif endings == "ov":
         MPs = [mixed_adj]

      for i, AP in enumerate(self.gram.accents):
         # variant = None means all variants
         if not(variant is not None and variant != i):
            length_inconstancy = False
            
            if endings == "all":
               if self.short_AP[i][-1] != self.long_AP[i][-1]:
                  length_inconstancy = True
            for paradigm in MPs:
               yield from self._paradigm_to_forms(paradigm, i, length_inconstancy, yat)
