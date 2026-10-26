from typing import Iterator, Optional
from ..pos import PartOfSpeech
from ..utils import garde
from ..paradigm_helpers import uniq, nice_name, accentize
from ..table import LabeledMultiform

class Adverb(PartOfSpeech):
   def multiforms(
      self,
      *,
      variant:Optional[int] = None,
      yat:str="e",
      latin:bool=False
   ) -> Iterator[LabeledMultiform]:
      accented_adverbs = [
         garde(accentize(key))
         for i, key in enumerate(self.accented_keys)
         if variant is None or variant == i
      ]
      yield nice_name(""), uniq(self._expose(form, yat, latin) for form in accented_adverbs)
