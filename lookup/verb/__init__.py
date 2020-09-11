from typing import Dict, List, Iterator, Optional, Tuple
from ..pos import PartOfSpeech, Replacement
from ..utils import insert, garde, expose, last_vowel_index, expose_replacement
from ..paradigm_helpers import AccentedTuple, OrderedSet, nice_name, oa, accentize
from .paradigms import MP_to_verb_stems
from ..table import LabeledMultiform

infinitive_dict: Dict[str, str] = {
   'alpha': 'ити', 'beta': 'ати', 'gamma': 'нути',
   'delta': 'ати', 'epsilon': 'овати', 'zeta': 'ивати',
   'eta': 'ѣти', 'theta': 'ети', 'iota': 'ати',
   'kappa': 'ти', 'kappa2': 'ти', 'kappa3': 'ти', 'lambda': 'ти', 'mu': 'ати'
}

class Verb(PartOfSpeech):
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
      #Verb-only
      self.is_reflexive = self.label('Refl')
      self.trunk = self._trunk()
      self.trunk2 = self._trunk2()

   # Verb-only
   @staticmethod
   def _verb_form_is_possible(label:str, aspect:List[str]) -> bool:
      if label.startswith('ipf'):
         return not 'Pf' in aspect
      return True

   # Verb-specific
   def _expose(self, form:str, yat:str="e", latin:bool=False) -> str:
      form = expose(form, yat, latin)
      if self.is_reflexive:
         if latin:
            form += ' se'
         else:
            form += ' се'
      return form

   # Verb-specific
   def _trunk(self) -> List[str]:
      result = []
      keys = self.accented_keys
      for i, AP in enumerate(self.gram.AP):
         accented_verb = garde(accentize(keys[i]))
         N = len(infinitive_dict[self.gram.MP[i]])
         if AP in oa:
            result.append(accented_verb[:-N])
         else:
            if self.gram.MP[i] in ['lambda']:
               trunk = accented_verb[:-N]
            elif self.gram.MP[i] == 'zeta':
               trunk = accented_verb[:-N-2]
            else:
               trunk = accented_verb[:-N-1]

            lvi = last_vowel_index(trunk)
            if lvi is None:
               result.append(trunk)
            else:
               result.append(insert(trunk, {lvi + 1: '·'}))
      return result

   def _trunk2(self) -> List[str]:
      result = []
      splitted_kind = self.kind.split("\\")
      for i, AP in enumerate(self.gram.AP):
         if self.gram.MP[i].startswith('kappa') and len(splitted_kind) > 3:
            frm = splitted_kind[3]
            lvi_ = last_vowel_index(frm)
            if lvi_ is not None:
               frm = insert(frm, {lvi_ + 1: '·'})
            result.append(frm)
         else:
            result.append(self.trunk[i])

      return result

   def _current_trunk(
      self,
      i:int,
      label:str
   ) -> str:
      if self.gram.MP[i] == 'kappa':
         formlist = ['prs', 'imv', 'pf', 'ipf']
      elif self.gram.MP[i] == 'kappa2':
         formlist = ['prs', 'imv', 'ipf']
      else:
         formlist = []
      if any(label.startswith(x) for x in formlist):
         return self.trunk2[i]
      return self.trunk[i]


   def _paradigm_to_forms(
      self,
      i:int,
      length_inconstancy:bool,
      yat:str="e",
      latin:bool=False
   ) -> Iterator[LabeledMultiform]:
      # TODO: length_inconstancy currently not used
      # however, Svetozar says he will use it later
      # e.g. гри̏сти, гри́зе̄м
      for label, ending in MP_to_verb_stems[self.gram.MP[i]].labeled_endings:

         if label in self.replacements:
            result = [
               expose_replacement(w_form, yat, latin)
               for w_form in self.replacements[label]
            ]
            yield nice_name(label), list(OrderedSet(result))

         else:
            if self._verb_form_is_possible(label, self.gram.other):
               ready_forms: List[str] = []
               for variation in ending:
                  ready_forms += self.process_one_form(
                     self.gram.AP[i], self._current_trunk(i, label), variation)

               if label in self.amendments:
                  ready_forms += [
                     expose_replacement(w_form, yat, latin)
                     for w_form in self.amendments[label]
                  ]
               result = [
                  self._expose(w_form, yat, latin)
                  for w_form in ready_forms
               ]
               yield nice_name(label), list(OrderedSet(result))


   def multiforms(
      self,
      *,
      variant:Optional[int]=None,
      yat:str="e",
      latin:bool=False
   ) -> Iterator[LabeledMultiform]:
      """conjugate"""
      for i, AP in enumerate(self.gram.AP):
         if self.gram.MP[i] in infinitive_dict:
            if not (variant is not None and variant != i):
               yield from self._paradigm_to_forms(i, False, yat, latin)

         else:
            raise NotImplementedError(
               f'Type {self.gram.MP[i]} ({self.key}) does not exist or is not ready yet'
            )
