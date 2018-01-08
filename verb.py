from typing import Dict, Iterator, Any
from paradigms import GramInfo, MP_to_stems
from notation_utils import accentize, insert, garde, prettify
from utils import decipher, last_vowel_index, first_vowel_index

class Verb:
   # TODO: get rid of Any
   def __init__(self, key: str, value: Dict[str, Any]) -> None:
      self.key = key
      self.value = value
      i, t = self.value['i'], self.value['t']
      self.info = decipher(i, t) # type: GramInfo
      self.is_reflexive = 'Refl' in self.info.other

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
      
   def conjugate(self) -> Iterator[str]:
      accented_verb = garde(accentize(self.key, self.info.accents))
      infinitive_dict = {'alpha': 'ити', 'beta': 'ати', 'gamma': 'нути',
                         'delta': 'ати', 'epsilon': 'овати', 'zeta': 'ивати',
                         'eta': 'ети', 'theta': 'ети', 'iota': 'ати',
                         'kappa': 'ти', 'lambda': 'ти', 'mu': 'ати'}
      if self.info.MP in infinitive_dict:
         # There are 2 major types of paradigms: 'a' and the rest
         if self.info.AP == 'a':
            trunk = accented_verb[:-len(infinitive_dict[self.info.MP])]
            for stem in MP_to_stems[self.info.MP]:
               for ending in stem: # type: ignore
                  verb_form = trunk
                  for ending_part in ending:
                     if self.info.AP in ending_part.accent:
                        verb_form.replace('\u030d', '') # straight
                        current_morph = ending_part.morpheme.replace('·', '\u030d') # to straight
                     else:
                        current_morph = ending_part.morpheme
                     verb_form += current_morph
                  yield self.expose(verb_form)

         else:
            if self.info.MP == 'kappa' or self.info.MP == 'lambda':
               trunk = accented_verb[:-len(infinitive_dict[self.info.MP])]
            else:
               trunk = accented_verb[:-len(infinitive_dict[self.info.MP])-1]
            to_insert = last_vowel_index(trunk) + 1
            trunk = insert(trunk, {to_insert: '·'})
            for stem in MP_to_stems[self.info.MP]:
               for ending in stem: # type: ignore
                  verb_form = trunk
                  #accentedness = False
                  for ending_part in ending:
                     if self.info.AP in ending_part.accent:
                        current_morph = ending_part.morpheme.replace('·', '\u030d') # straight
                        #accentedness = True
                     else:
                        current_morph = ending_part.morpheme
                     verb_form += current_morph
                  if '\u030d' not in verb_form: # straight
                     verb_form = verb_form.replace('·', '\u030d', 1) # to straight
                  yield self.expose(verb_form)
