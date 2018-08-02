from typing import Any, Dict, List, Iterator, Optional
from ..table import LabeledMultiform
from ..utils import insert, garde, expose, last_vowel_index
from ..paradigm_helpers import AccentedTuple, GramInfo
from .paradigms import MP_to_verb_stems, VerbEnding

# There are 2 major types of paradigms: o., a., a: and the rest
oa = ['o.', 'a.', 'a:']

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
      result = []
      
      for i, AP in enumerate(self.info.AP):
         accented_verb = garde(self.info.accents[i].accentize(self.key)) # TODO: add loop
         N = len(infinitive_dict[self.info.MP])
         if AP in oa:
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
   
   # Verb-only
   def _verb_form_is_possible(self, label, aspect):
      if label.startswith('ipf'):
         return not 'Pf' in aspect
      else:
         return True
      
   def _append_morpheme(self, i: int, verb_form: str, ending_part: AccentedTuple) -> str:
      # TODO: sveto: please understand and document
      if self.info.AP[i] in ending_part.accent:
         if self.info.AP[i] in oa:
            verb_form = verb_form.replace('\u030d', '') # straight
         morpheme = ending_part.morpheme.replace('·', '\u030d') # to straight
      else:
         morpheme = ending_part.morpheme
      return verb_form + morpheme
   
   def _reduce_doublets(self, endings_: List[VerbEnding], AP: str) -> List[VerbEnding]:
      # the following code is for verbs only (is it?).
      # but only because it is not needed in adjectives.
      # it deletes endings identical in future
      endings: List[Any] = []
      if len(endings_) > 1:
         for ending_ in endings_:
            addendum = True
            supr_ = (ending_.theme.morpheme+ending_.ending.morpheme).replace('·', '')
            for ending in endings:
               supr = (ending.theme.morpheme+ending.ending.morpheme).replace('·', '')
               accents_ = ''.join([ending.theme.accent+ending.ending.accent])
               if AP not in accents_ and supr_ == supr:
                  addendum = False
            if addendum:   
               endings.append(ending_)
      else:
         endings = endings_
         
      return endings

   def multiforms(self, *, variant: Optional[int] = None) -> Iterator[LabeledMultiform]:
      """conjugate"""
      if self.info.MP in infinitive_dict:
         for i, AP in enumerate(self.info.AP):
            if variant is not None and variant != i:
               continue
            for label, endings_ in MP_to_verb_stems[self.info.MP].labeled_endings:
               if self._verb_form_is_possible(label, self.info.other):
                  verb_forms: List[str] = []               
                  endings = self._reduce_doublets(endings_, AP)
                  
                  for ending in endings:
                     verb_form = self.trunk[i]
                     verb_form = self._append_morpheme(i, verb_form, ending.theme)
                     verb_form = self._append_morpheme(i, verb_form, ending.ending)
                     if self.info.AP not in oa:
                        if '\u030d' not in verb_form: # straight
                           verb_form = verb_form.replace('·', '\u030d', 1) # to straight
                           
                     verb_forms.append(self._expose(verb_form))
                  yield label, verb_forms
      
      else:
         raise NotImplementedError('Type {self.info.MP} ({}) does not exist or is not ready yet')