from typing import Dict, Generic, List, TypeVar
import random

KT = TypeVar("KT")
VT = TypeVar("VT")

class Multidict(Generic[KT, VT]):
   """
   A key can correspond to zero or more values.
   There are no KeyErrors: no values are not an error, just a special case.
   """
   def __init__(self) -> None:
      self._data: Dict[KT, List[VT]] = {}

   def __getitem__(self, key: KT) -> List[VT]:
      try:
         return self._data[key]
      except KeyError:
         return []

   def __setitem__(self, key: KT, value: VT) -> None:
      if key in self._data:
         self._data[key].append(value)
      else:
         self._data[key] = [value]

   def random_key(self) -> KT:
      return random.choice(list(self._data.keys()))
