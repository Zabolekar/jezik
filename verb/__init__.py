from typing import Any, Dict, List
from ..table import Table
from ..utils import insert, garde, expose, last_vowel_index
from ..paradigm_helpers import GramInfo
from .paradigms import MP_to_verb_stems

# There are 2 major types of paradigms: o., a., a: and the rest

infinitive_dict: Dict[str, str] = {
   'alpha': 'ити', 'beta': 'ати', 'gamma': 'нути',
   'delta': 'ати', 'epsilon': 'овати', 'zeta': 'ивати',
   'eta': 'ети', 'theta': 'ети', 'iota': 'ати',
   'kappa': 'ти', 'lambda': 'ти', 'mu': 'ати'
}

class Verb:
   def __init__(self, key: str, value: Dict[str, Any]) -> None:
      self.key = key
      self.value = value
      i, t = self.value['i'].split(';'), self.value['t']
      self.info = GramInfo(i, t)
      self.is_reflexive = 'Refl' in self.info.other
      self.trunk = self._trunk()

   def _expose(self, form: str) -> str:
      form = expose(form)
      if self.is_reflexive:
         form += ' се'
      return form

   def _trunk(self) -> List[str]:
      result: List[str] = []
      for number, AP in enumerate(self.info.AP):
         accented_verb = garde(self.info.accents[number].accentize(self.key)) # TODO: add loop
         N = len(infinitive_dict[self.info.MP])
         if AP in ['o.', 'a.', 'a:']:
            result.append(accented_verb[:-N])
         else:
            if self.info.MP in ['kappa', 'lambda']:
               trunk = accented_verb[:-N]
            else:
               trunk = accented_verb[:-N-1]
            lvi = last_vowel_index(trunk)
            if lvi is None:
               result.append(trunk)
            else:
               result.append(insert(trunk, {lvi + 1: '·'}))
      return result
               
   def _append_morpheme(self, number, verb_form, ending_part):
      # TODO: sveto: please understand and document
      if self.info.AP[number] in ending_part.accent:
         if self.info.AP[number] in ['o.', 'a.', 'a:']:
            verb_form = verb_form.replace('\u030d', '') # straight
         morpheme = ending_part.morpheme.replace('·', '\u030d') # to straight
      else:
         morpheme = ending_part.morpheme
      return verb_form + morpheme

   def conjugate(self) -> Table:
      if self.info.MP in infinitive_dict: # TODO: what if not?
         for number, AP in enumerate(self.info.AP):
            for label, endings in MP_to_verb_stems[self.info.MP].labeled_endings:
               verb_forms: List[str] = []
               for ending in endings:
                  verb_form = self.trunk[number]
                  verb_form = self._append_morpheme(number, verb_form, ending.theme)
                  verb_form = self._append_morpheme(number, verb_form, ending.ending)
                  if self.info.AP not in ['o.', 'a.', 'a:']:
                     if '\u030d' not in verb_form: # straight
                        verb_form = verb_form.replace('·', '\u030d', 1) # to straight
                  verb_forms.append(self._expose(verb_form))
               yield label, iter(verb_forms) # TODO: why does it need to be iter?
