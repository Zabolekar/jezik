from typing import Any, Dict, List, Iterator, Optional
import re
from ..table import LabeledMultiform
from ..pos import PartOfSpeech
from ..utils import insert, garde, expose, last_vowel_index
from ..paradigm_helpers import GramInfo, nice_name, oa
from .paradigms import AdjParadigm, short_adj, long_adj, mixed_adj

class Adjective(PartOfSpeech):
   def __init__(self, key: str, value: Dict[str, Any], yat:str="ekav") -> None:
      super().__init__(key, value, yat)
      # Adjective-only: zipping the APs to 2 lists. But is it really necessary?
      self.short_AP, self.long_AP = list(zip(*[AP.split(',') for AP in self.info.AP]))

      self.trunk = self._trunk() #both but not separable

   # different
   def _expose(self, form: str, yat:str="ekav") -> str:
      return expose(form, yat)

   # different for Verb and Adjective
   def _trunk(self) -> List[str]:
      result = []

      for number, item in enumerate(self.info.AP):
         accented_adj = garde(self.info.accents[number].accentize(self.key))
         if 'ov' in self.info.other:
            trunk = accented_adj # ok
         elif 'all' in self.info.other:
            if 'ъ\u030d' in accented_adj:
               trunk = accented_adj[:-2] + accented_adj[-1]
            else:
               trunk = accented_adj
         elif 'ski' in self.info.other:
            trunk = re.sub('\u0304\u030d$', '\u0304', accented_adj)[:-2]
         if not 'a' in self.info.AP[number]:
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

   # Adjective-only. Verb should have its own one 
   def _paradigm_to_forms(self, paradigm: AdjParadigm, i: int, length_inconstant: bool, yat:str="ekav") -> Iterator[LabeledMultiform]:
      """
      Current subparadigm: short or long AP (they behave differently)
      i: index of the variation (by variation we mean things like зу̑бнӣ зу́бнӣ)
      """
      current_AP = self.short_AP[i] if paradigm is short_adj else self.long_AP[i]

      for label, ending in zip(paradigm._fields, paradigm): # TODO: verbs do it completely differently, unify
         ready_forms = []
         
         adj_form = self._swap(self.trunk[i], length_inconstant, current_AP, self.long_AP[i])

         for variation in ending: # e.g. -om, -ome, -omu
            new_adj_form = adj_form
            
            new_adj_form = new_adj_form

            if current_AP in variation.accent: # if the ending should be accented
               new_adj_form = new_adj_form.replace('\u030d', '') # delete all already put accents from the stem
               if current_AP not in oa: # and, further, if the stem has no firmly accented place,
                   # then we delete all the accentable places from the stem.
                   # if we do not do this, we get wrong (double) accents in result!
                   # TODO: when extending this to verbs, do not forget the 'o' paradigm
                  new_adj_form = new_adj_form.replace('·', '')
               # -- and finally we put the accent on the ending:
               current_morpheme = variation.morpheme.replace('·', '\u030d')
               
            else:
               current_morpheme = variation.morpheme.replace('·', '')
            
            # special case: if we are in the short AP
            
            if current_AP == self.short_AP[i]:
               if current_AP.endswith('?') and not 'ø' in current_morpheme:
                  trunk_lvi = last_vowel_index(new_adj_form)
                  last_macron = new_adj_form.rfind('\u0304')
                  new_adj_form = new_adj_form[:last_macron] + new_adj_form[last_macron+1:]
                  # we delete macron on the last vowel from words with inconstant length
                  # TODO: BIG QUESTION: why do we check and do this twice? just for security?
                  
            new_adj_form += current_morpheme # add the ending to the stem

            # finally, if the word is not accented, we put the accent on the stem
            
            if 'a' not in current_AP: # why this? why not always? TODO: test on an 'a'-adj
               if '\u030d' not in adj_form:
                  new_adj_form = new_adj_form.replace('·', '\u030d', 1) 
            if self._adj_form_is_possible(new_adj_form):
               ready_forms.append(new_adj_form)
            
         yield nice_name(label), [self._expose(w_form, yat) for w_form in ready_forms]

   def multiforms(self, *, variant: Optional[int] = None, yat:str="ekav") -> Iterator[LabeledMultiform]:
      """decline"""
      endings = self.info.other[0]
      MPs: List[AdjParadigm]
      if endings == "all":
         MPs = [short_adj, long_adj]
      elif endings == "ski":
         MPs = [long_adj]
      elif endings == "ov":
         MPs = [mixed_adj]

      for i, AP in enumerate(self.info.accents):
         # variant = None means all variants
         if variant is not None and variant != i:
            continue
         length_inconstancy = False
         print(self.short_AP)
         print(self.long_AP)
         if endings == "all":
            if self.short_AP[i][-1] != self.long_AP[i][-1]:
               length_inconstancy = True
         for paradigm in MPs:
            yield from self._paradigm_to_forms(paradigm, i, length_inconstancy, yat)
