from typing import Iterator, List, Tuple

Form = str
Multiform = List[Form]
LabeledMultiform = Tuple[str, Multiform]

class Table:
   def __init__(self, caption: str, data: Iterator[LabeledMultiform]) -> None:
      self.caption = caption
      self._data = list(data)

   def __getitem__(self, name):
      for form_name, forms in self:
         if name == form_name:
            return forms

   def __repr__(self):
      return str(self._data)

   def __iter__(self):
      return iter(self._data)
