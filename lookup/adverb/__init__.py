from typing import Iterator, Optional
from ..pos import PartOfSpeech
from ..utils.text_utils import accentize
from ..utils.accents import garde
from ..generic_utils import uniq
from ..paradigm_helpers import nice_name
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
