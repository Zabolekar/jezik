from typing import Dict, Iterator, Any
from paradigms import GramInfo, MP_to_stems
from notation_utils import accentize, insert, garde, prettify
from utils import last_vowel_index, first_vowel_index
from auxiliary_data import infinitive_dict

# There are 2 major types of paradigms: 'a' and the rest

class Verb:
   # TODO: get rid of Any
   def __init__(self, key: str, value: Dict[str, Any]) -> None:
      self.key = key
      self.value = value
      i, t = self.value['i'], self.value['t']
      self.info = GramInfo(i, t)
      self.is_reflexive = 'Refl' in self.info.other
      self.trunk = self._trunk()

   def _expose(self, form: str) -> str:
      if '0̍' in form: # 0 means accent on the firstmost syllable
         form = (form
                 .replace('0', '')
                 .replace('\u030d', '') # straight accent
                 .replace('~', '\u0304'))
         to_insert = first_vowel_index(form) + 1
         form = insert(form, {to_insert: '\u030d'}) # straight accent
      form = prettify(form
                      .replace('\u030d\u0304', '\u0304\u030d') #straight, macron
                      .replace('~', '')
                      .replace('0', '')
                      .replace('·', ''))
      if self.is_reflexive:
         form += ' се'
      return form

   def _trunk(self):
      accented_verb = garde(accentize(self.key, self.info.accents))
      N = len(infinitive_dict[self.info.MP])
      if self.info.AP == 'a':
         return accented_verb[:-N]
      else:
         if self.info.MP in ['kappa', 'lambda']:
            trunk = accented_verb[:-N]
         else:
            trunk = accented_verb[:-N-1]
         to_insert = last_vowel_index(trunk) + 1
         return insert(trunk, {to_insert: '·'})

   def conjugate(self) -> Iterator[str]:
      if self.info.MP in infinitive_dict: # TODO: what if not?
         for stem in MP_to_stems[self.info.MP]:
            for ending in stem: # type: ignore
               verb_form = self.trunk
               for ending_part in ending:
                  if self.info.AP in ending_part.accent:
                     if self.info.AP == 'a':
                        verb_form = verb_form.replace('\u030d', '') # straight
                     current_morph = ending_part.morpheme.replace('·', '\u030d') # to straight
                  else:
                     current_morph = ending_part.morpheme
                  verb_form += current_morph
               if self.info.AP != 'a':
                  if '\u030d' not in verb_form: # straight
                     verb_form = verb_form.replace('·', '\u030d', 1) # to straight
               yield self._expose(verb_form)
