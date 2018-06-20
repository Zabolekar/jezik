from typing import Dict, Iterator, Any
from .paradigms import GramInfo, MP_to_verb_stems
from .utils import insert, garde, expose, last_vowel_index, first_vowel_index
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
      accented_verb = garde(self.info.accents.accentize(self.key))
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
            #raise ValueError(f"{trunk} does not contain any vowels")
            pass
         else:
            to_insert = lvi + 1
            return insert(trunk, {to_insert: '·'})

   def conjugate(self) -> Iterator[str]:
      if self.info.MP in infinitive_dict: # TODO: what if not?
         for stem in MP_to_verb_stems[self.info.MP]:
            for ending in stem: # type: ignore
               verb_form = self.trunk
               for ending_part in ending:
                  if self.info.AP in ending_part.accent:
                     if self.info.AP in ['o.', 'a.', 'a:']:
                        verb_form = verb_form.replace('\u030d', '') # straight
                     current_morph = ending_part.morpheme.replace('·', '\u030d') # to straight
                  else:
                     current_morph = ending_part.morpheme
                  verb_form += current_morph
               if self.info.AP not in ['o.', 'a.', 'a:']:
                  if '\u030d' not in verb_form: # straight
                     verb_form = verb_form.replace('·', '\u030d', 1) # to straight
               yield self._expose(verb_form)
