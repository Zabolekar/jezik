from typing import Iterator, Optional
from ..pos import PartOfSpeech
from ..utils import garde, expose
from ..paradigm_helpers import uniq, nice_name, accentize
from ..table import LabeledMultiform

class Adverb(PartOfSpeech): #TODO majority of these can probably be moved to POS?
   def __init__(self, key: str, accented_keys: str, kind: str, info: str) -> None:
      super().__init__(key, accented_keys, kind, info, (), ())

   @staticmethod
   def _expose(form: str, yat:str="e", latin:bool=False) -> str:
      return expose(form, yat, latin)

   def multiforms(
      self,
      *,
      variant: Optional[int] = None,
      yat:str="e",
      latin:bool=False
   ) -> Iterator[LabeledMultiform]:
      accented_adverbs = [
         garde(accentize(self.key))
         for i in range(len(self.accented_keys))
         ]
      yield nice_name(""), uniq(expose(form, yat, latin) for form in accented_adverbs)
