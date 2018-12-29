from typing import Any, Dict, List, Iterator, Optional
from ..pos import PartOfSpeech
from ..utils import insert, garde, expose, last_vowel_index
from ..paradigm_helpers import AccentedTuple, OrderedSet, nice_name, oa, accentize
from .paradigms import MP_to_verb_stems
from ..table import LabeledMultiform

infinitive_dict: Dict[str, str] = {
   'alpha': 'ити', 'beta': 'ати', 'gamma': 'нути',
   'delta': 'ати', 'epsilon': 'овати', 'zeta': 'ивати',
   'eta': 'ети', 'theta': 'ети', 'iota': 'ати',
   'kappa': 'ти', 'lambda': 'ти', 'mu': 'ати'
}

class Verb(PartOfSpeech):
   def __init__(self, key: str, value: Dict[str, Any], yat:str="ekav") -> None:
      super().__init__(key, value, yat)
      #Verb-only
      self.is_reflexive = 'Refl' in self.info.other

      self.trunk = self._trunk() #both but not separable

   # Verb-specific
   def _expose(self, form: str, yat:str="ekav") -> str:
      form = expose(form, yat)
      if self.is_reflexive:
         form += ' се'
      return form

   # Verb-specific
   def _trunk(self) -> List[str]:
      result = []
      
      for i, AP in enumerate(self.info.AP):
         accented_verb = garde(accentize(self.key, self.info.accents[i].r, self.info.accents[i].v))
         N = len(infinitive_dict[self.info.MP[i]])
         if AP in oa:
            result.append(accented_verb[:-N])
         else:
            if self.info.MP[i] in ['kappa', 'lambda']:
               trunk = accented_verb[:-N]
            else:
               trunk = accented_verb[:-N-1]
            lvi = last_vowel_index(trunk)
            if lvi is None:
               result.append(trunk)
            else:
               result.append(insert(trunk, {lvi + 1: '·'}))
      return result
   
   # Verb-only
   def _verb_form_is_possible(self, label, aspect):
      if label.startswith('ipf'):
         return not 'Pf' in aspect
      else:
         return True

   def process_one_form(self, i: str, verb_trunk: str, ending_variation: List[AccentedTuple]) -> List[str]:
      verb_form = [verb_trunk]
      for w in ending_variation:
         verb_form = self._append_morpheme(self.info.AP[i], verb_form, w)
         for x in verb_form:
            x = self.accentize(i, x)
      return verb_form

   def _paradigm_to_forms(self, i, length_inconstancy, yat:str="ekav"):
         for label, ending in MP_to_verb_stems[self.info.MP[i]].labeled_endings:
            if self._verb_form_is_possible(label, self.info.other):
               ready_forms: List[str] = []               
                  
               for variation in ending:
                  ready_forms += self.process_one_form(i, self.trunk[i], variation)
                           
               yield nice_name(label), list(OrderedSet([self._expose(w_form, yat) for w_form in ready_forms]))


   def multiforms(self, *, variant: Optional[int] = None, yat:str="ekav") -> Iterator[LabeledMultiform]:
      """conjugate"""
      for i, AP in enumerate(self.info.AP):
         if self.info.MP[i] in infinitive_dict:         
            if not (variant is not None and variant != i):
               yield from self._paradigm_to_forms(i, False, yat)
  
         else:
            raise NotImplementedError(f'Type {self.info.MP[i]} ({self.key}) does not exist or is not ready yet')