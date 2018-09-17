from typing import Any, Dict, List, Iterator, Optional
from ..pos import PartOfSpeech
from ..utils import insert, garde, expose, last_vowel_index
from ..paradigm_helpers import AccentedTuple, GramInfo, nice_name, oa
from .paradigms import MP_to_verb_stems
from ..table import LabeledMultiform

infinitive_dict: Dict[str, str] = {
   'alpha': 'ити', 'beta': 'ати', 'gamma': 'нути',
   'delta': 'ати', 'epsilon': 'овати', 'zeta': 'ивати',
   'eta': 'ети', 'theta': 'ети', 'iota': 'ати',
   'kappa': 'ти', 'lambda': 'ти', 'mu': 'ати'
}

class Verb(PartOfSpeech):
   def __init__(self, key: str, value: Dict[str, Any]) -> None:
      super().__init__(key, value)
      #Verb-only
      self.is_reflexive = 'Refl' in self.info.other

      self.trunk = self._trunk() #both but not separable

   # Verb-specific
   def _expose(self, form: str) -> str:
      form = expose(form)
      if self.is_reflexive:
         form += ' се'
      return form

   # Verb-specific
   def _trunk(self) -> List[str]:
      result = []
      
      for i, AP in enumerate(self.info.AP):
         accented_verb = garde(self.info.accents[i].accentize(self.key))
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

   def _paradigm_to_forms(self, paradigm, i, length_inconstancy):
         for label, endings_ in MP_to_verb_stems[self.info.MP[i]].labeled_endings:
            if self._verb_form_is_possible(label, self.info.other):
               ready_forms: List[str] = []               
               ending = self._reduce_doublets(endings_, self.info.AP[i])
                  
               for variation in ending:
                  verb_form = self.trunk[i]
                  for w in variation:
                     verb_form = self._append_morpheme(i, verb_form, w)
                  if self.info.AP not in oa:
                     if '\u030d' not in verb_form: # straight
                        verb_form = verb_form.replace('·', '\u030d', 1) # to straight
                           
                  ready_forms.append(verb_form)
               yield nice_name(label), [self._expose(w_form) for w_form in ready_forms]


   def multiforms(self, *, variant: Optional[int] = None) -> Iterator[LabeledMultiform]:
      """conjugate"""
      for i, AP in enumerate(self.info.AP):
         if self.info.MP[i] in infinitive_dict:         
            if variant is not None and variant != i:
               continue

            yield from self._paradigm_to_forms(self.info.MP[i], i, False)
  
         else:
            raise NotImplementedError(f'Type {self.info.MP[i]} ({self.key}) does not exist or is not ready yet')