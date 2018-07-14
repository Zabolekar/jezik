from typing import Iterable, Iterator, List, Tuple
from pprint import pprint

Form = str
Multiform = List[Form]
LabeledMultiform = Tuple[str, Multiform]

class Table:
   def __init__(self, caption: str, data: Iterable[LabeledMultiform]) -> None:
      self.caption = caption
      self._data = list(data)

   def __getitem__(self, query: str) -> "Table": # TODO: you know what to do when we switch to 3.7
      result = []
      v = query.split()
      for form_name, forms in self._data:
         w = form_name.split()
         if all(s in w for s in v):
            result.append((form_name, forms))
      return Table(f"{self.caption} [{query}]", result)

   def __repr__(self) -> str:
      result = self.caption + "\n"
      for form_name, forms in self._data:
         result += f"{form_name:20}{', '.join(forms)}\n"
      return result

   def __iter__(self) -> Iterator[LabeledMultiform]:
      return iter(self._data)
