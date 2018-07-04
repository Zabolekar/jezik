from typing import Any, Dict
from .table import Table
from .paradigms import GramInfo, MP_to_verb_stems
from .utils import insert, garde, expose, last_vowel_index
from .auxiliary_data import infinitive_dict

# There are 2 major types of paradigms: o., a., a: and the rest

class Verb:
   def __init__(self, key: str, value: Dict[str, Any]) -> None:
      self.key = key
      self.value = value
      i, t = self.value['i'], self.value['t']
      self.info = GramInfo(i, t)
      self.is_reflexive = 'Refl' in self.info.other
      self.trunk = self._trunk()

   def _expose(self, form: str) -> str:
      form = expose(form)
      if self.is_reflexive:
         form += ' се'
      return form

   def _trunk(self) -> str:
      accented_verb = garde(self.info.accents[0].accentize(self.key)) # TODO: add loop
      N = len(infinitive_dict[self.info.MP])
      if self.info.AP in ['o.', 'a.', 'a:']:
         return accented_verb[:-N]
      else:
         if self.info.MP in ['kappa', 'lambda']:
            trunk = accented_verb[:-N]
         else:
            trunk = accented_verb[:-N-1]
         lvi = last_vowel_index(trunk)
         if lvi is None:
            return trunk
         else:
            return insert(trunk, {lvi + 1: '·'})

   def _append_morpheme(self, verb_form, ending_part):
      # TODO: sveto: please understand and document
      if self.info.AP in ending_part.accent:
         if self.info.AP in ['o.', 'a.', 'a:']:
            verb_form = verb_form.replace('\u030d', '') # straight
         morpheme = ending_part.morpheme.replace('·', '\u030d') # to straight
      else:
         morpheme = ending_part.morpheme
      return verb_form + morpheme

   def conjugate(self) -> Table:
      if self.info.MP in infinitive_dict: # TODO: what if not?
         for label, ending in MP_to_verb_stems[self.info.MP].labeled_endings:
            verb_form = self.trunk
            verb_form = self._append_morpheme(verb_form, ending.theme)
            verb_form = self._append_morpheme(verb_form, ending.ending)
            if self.info.AP not in ['o.', 'a.', 'a:']:
               if '\u030d' not in verb_form: # straight
                  verb_form = verb_form.replace('·', '\u030d', 1) # to straight
            yield label, iter([self._expose(verb_form)]) # TODO: multiforms
