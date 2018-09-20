from typing import Any, Dict, List, Iterator, Optional
from ..pos import PartOfSpeech
from ..utils import insert, garde, expose, last_vowel_index, first_vowel_index
from ..paradigm_helpers import AccentedTuple, GramInfo, nice_name, oa
from ..table import LabeledMultiform
from .paradigms import c_m

class Noun(PartOfSpeech):
   def __init__(self, key: str, value: Dict[str, Any], yat:str="ekav") -> None:
      super().__init__(key, value, yat)

      self.trunk = self._trunk()
      #print(self.info.MP)
      x = self.info.MP[0].split(',')
      self.anim = [x.split(',')[1] for x in self.info.MP]
      self.suff = [x.split(',')[0] for x in self.info.MP]

   def _expose(self, form: str, yat:str="ekav") -> str:
      return expose(form, yat)

   def _trunk(self) -> List[str]:
      result = []

      for i, AP in enumerate(self.info.AP):
         #print("AP: ", AP)
         accented_noun = garde(self.info.accents[i].accentize(self.key))

         if 'm' in self.info.other[i] and not 'o' in self.info.other[i]:
            trunk_ = self.key
            accented_trunk_ = accented_noun
         else:
            trunk_ = self.key[:-1]
            accented_trunk_ = accented_noun[:-1]

         if 'c' in AP:
            if not self.key.endswith('а'):
               trunk = accented_trunk_.replace('\u030d', '·')
               #print(trunk_, '->', trunk)
            else:
               fvi = first_vowel_index(trunk_)
               if fvi is None:
                  trunk = trunk_
                  #print('no vowel found: ', trunk)
               else:
                  trunk = insert(trunk_, {fvi: '·'})
                  #print(trunk_, ' : ', trunk)
         elif 'b' in AP:
            lvi = last_vowel_index(trunk_)
            if lvi is None:
               trunk = trunk_
            else:
               trunk = insert(trunk_, {lvi: '·'})
         elif 'a' in AP:
            trunk = accented_trunk_
         else:
            raise NotImplementedError
         #print(trunk)
         result.append(trunk)     
      
      return result

   def _paradigm_to_forms(self, paradigm, i, length_inconstancy, yat:str="ekav"):
      for label, ending in c_m(self.suff[i], self.anim[i]).labeled_endings:
         ready_forms: List[str] = []
         for variation in ending:
            noun_form = self.trunk[i]
            for w in variation:
               noun_form = self._append_morpheme(i, noun_form, w)
            if self.info.AP[i] not in oa:
               if '\u030d' not in noun_form: # straight
                  noun_form = noun_form.replace('·', '\u030d', 1) # to straight
            ready_forms.append(noun_form)
         yield nice_name(label), [self._expose(w_form, yat) for w_form in ready_forms]

   def multiforms(self, *, variant: Optional[int] = None, yat:str="ekav") -> Iterator[LabeledMultiform]:
      """conjugate"""
      for i, AP in enumerate(self.info.AP):
         yield from self._paradigm_to_forms(self.info.other[i], i, False, yat)