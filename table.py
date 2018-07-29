from typing import Iterable, Iterator, List, Tuple
from pprint import pprint

Form = str
Multiform = List[Form]
LabeledMultiform = Tuple[str, Multiform]

class Table:
   def __init__(self, pos: str, caption: str, data: Iterable[LabeledMultiform]) -> None:
      self.caption = caption
      self.pos = pos
      self._data = list(data)

   def __getitem__(self, query: str) -> "Table": # TODO: you know what to do when we switch to 3.7
      result = []
      v = query.split()
      for form_name, forms in self._data:
         w = form_name.split()
         if all(s in w for s in v):
            result.append((form_name, forms))
      return Table(f"partial {self.pos}", f"{self.caption} [{query}]", result)

   @property
   def multiform(self) -> List[str]: # TODO: document in README, rethink
      if len(self._data) != 1:
         raise AttributeError("A 'Table' object has an attribute 'multiform' if and only if it contains exactly one cell")
      return self._data[0][1]

   def __repr__(self) -> str:
      result = self.caption + "\n"
      max_name_width = max(len(form_name) for form_name, _ in self._data)
      for form_name, forms in self._data:
         result += f"{form_name:{max_name_width + 5}}{', '.join(forms)}\n"
      return result

   def __iter__(self) -> Iterator[LabeledMultiform]:
      return iter(self._data)
