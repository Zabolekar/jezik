from typing import Iterator, Optional
from ..pos import PartOfSpeech, Replacement
from ..utils import garde
from ..paradigm_helpers import uniq, nice_name, accentize
from ..table import LabeledMultiform

class Adverb(PartOfSpeech):
   def __init__(
      self,
      key:str,
      accented_keys:str,
      kind:str,
      info:str,
      replacements:tuple[Replacement, ...]=(),
      amendments:tuple[Replacement, ...]=()
   ) -> None:
      super().__init__(key, accented_keys, kind, info, replacements, amendments)

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
