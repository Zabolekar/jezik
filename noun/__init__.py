from typing import Any, Dict, List, Iterator, Optional
from ..pos import PartOfSpeech
from ..utils import insert, garde, expose, last_vowel_index, first_vowel_index
from ..paradigm_helpers import AccentedTuple, OrderedSet, nice_name, oa, accentize
from ..table import LabeledMultiform
from .paradigms import c_m

class Noun(PartOfSpeech):
   def __init__(self, key: str, value: Dict[str, Any], yat:str="ekav") -> None:
      super().__init__(key, value, yat)

      self.trunk = self._trunk()
      #x = self.info.MP[0].split(',')
      self.anim = [x.split(',')[1] for x in self.info.MP]
      self.suff = [x.split(',')[0] for x in self.info.MP]

   def _expose(self, form: str, yat:str="ekav") -> str:
      return expose(form, yat)

   def _trunk(self) -> List[str]:
      result = []

      for i, AP in enumerate(self.info.AP):

         accented_noun = garde(accentize(self.key, self.info.accents[i].r, self.info.accents[i].v))

         if 'm' in self.info.other and not 'o' in self.info.other:
            trunk_ = accented_noun.replace('\u030d', '')
            # self.key is useless here; accented_noun has not only stress place,
            # it has also all the lengths in the stem which surely are of importance
            accented_trunk_ = accented_noun
         else:
            trunk_ = accented_noun.replace('\u030d', '')[:-1]
            accented_trunk_ = accented_noun[:-1]

         if 'c' in AP or 'd' in AP:
            if not self.key.endswith('а'):
               trunk = accented_trunk_.replace('\u030d', '·')
            else:
               fvi = first_vowel_index(trunk_)
               if fvi is None:
                  trunk = trunk_
               else:
                  trunk = insert(trunk_, {fvi: '·'})
         elif 'b' in AP:
            lvi = last_vowel_index(trunk_)
            if lvi is None:
               trunk = trunk_
            else:
               trunk = insert(trunk_, {lvi+1: '·'})
         elif 'a' in AP:
            trunk = accented_trunk_
         else:
            raise NotImplementedError
         trunk = trunk.replace('·\u0304', '\u0304·')
         trunk = trunk.replace('\u030d\u0304', '\u0304\u030d')
         result.append(trunk)
      return result

   def _noun_form_is_possible(self, noun_form: str, variation, paradigm):
      return not(first_vowel_index(noun_form) == last_vowel_index(noun_form)
                 and ('c' in paradigm or 'd' in paradigm)
                 and variation == [AccentedTuple('<а·\u0304', 'b.b:')])

   def _paradigm_to_forms(self, i, length_inconstancy, yat:str="ekav"):
      for label, ending in c_m(self.suff[i], self.anim[i]).labeled_endings:
         ready_forms: List[str] = [] # TODO: better name
         for variation in ending:
            noun_form = self.trunk[i]
            if self._noun_form_is_possible(noun_form, variation, self.info.AP[i]):
               for w in variation:
                  noun_form = self._append_morpheme(i, noun_form, w)
               if self.info.AP[i] not in oa: 
                  if '\u030d' not in noun_form: # straight
                     noun_form = noun_form.replace('·', '\u030d', 1) # to straight
               ready_forms.append(noun_form)
         yield nice_name(label), list(OrderedSet([self._expose(w_form, yat) for w_form in ready_forms]))

   def multiforms(self, *, variant: Optional[int] = None, yat:str="ekav") -> Iterator[LabeledMultiform]:
      """decline"""
      for i, AP in enumerate(self.info.AP):
         if not (variant is not None and variant != i):
            yield from self._paradigm_to_forms(i, False, yat)