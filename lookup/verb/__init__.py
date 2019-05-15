from typing import Dict, List, Iterator, Optional, Tuple
from ..pos import PartOfSpeech, Replacement
from ..utils import insert, garde, expose, last_vowel_index, expose_replacement
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
   def __init__(
      self, 
      key: str, 
      kind: str, 
      info: str,
      replacements: Tuple[Replacement, ...],
      yat:str="ekav") -> None:
      super().__init__(key, kind, info, replacements, yat)
      #Verb-only
      self.is_reflexive = 'Refl' in self.gram.other
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
      
      for i, AP in enumerate(self.gram.AP):
         accented_verb = garde(accentize(self.key, self.gram.accents[i].r, self.gram.accents[i].v))
         N = len(infinitive_dict[self.gram.MP[i]])
         if AP in oa:
            result.append(accented_verb[:-N])
         else:
            if self.gram.MP[i] in ['kappa', 'lambda']:
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
   def _verb_form_is_possible(self, label: str, aspect: List[str]) -> bool:
      if label.startswith('ipf'):
         return not 'Pf' in aspect
      else:
         return True

   def process_one_form(self, i: int, verb_trunk: str, ending_variation: List[AccentedTuple]) -> List[str]:
      verb_form = [verb_trunk]
      current_AP = self.gram.AP[i]
      for w in ending_variation:
         verb_form = self._append_morpheme(current_AP, verb_form, w)
         for x in verb_form:
            x = self.accentize(current_AP, x)
      return verb_form

   def _paradigm_to_forms(self, i: int, length_inconstancy: bool, yat:str="ekav") -> Iterator[LabeledMultiform]:
      # TODO: length_inconstancy currently not used
      # however, but Svetozar says he will use it later
      # e.g. гри̏сти, гри́зе̄м
      for label, ending in MP_to_verb_stems[self.gram.MP[i]].labeled_endings:

         if label in self.replacements:
            yield nice_name(label), \
               list(
                  OrderedSet(
                     [expose_replacement(w_form, yat) for w_form in self.replacements[label]]
                     )
                  )

         else:
            if self._verb_form_is_possible(label, self.gram.other):
               ready_forms: List[str] = [] 
               for variation in ending:
                  ready_forms += self.process_one_form(i, self.trunk[i], variation)
               yield nice_name(label), \
                  list(
                     OrderedSet(
                        [self._expose(w_form, yat) for w_form in ready_forms]
                        )
                     )


   def multiforms(self, *, variant: Optional[int] = None, yat:str="ekav") -> Iterator[LabeledMultiform]:
      """conjugate"""
      for i, AP in enumerate(self.gram.AP):
         if self.gram.MP[i] in infinitive_dict:         
            if not (variant is not None and variant != i):
               yield from self._paradigm_to_forms(i, False, yat)
  
         else:
            raise NotImplementedError(f'Type {self.gram.MP[i]} ({self.key}) does not exist or is not ready yet')