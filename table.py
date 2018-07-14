from typing import Iterator, Tuple

Form = str
Multiform = Iterator[Form]
LabeledMultiform = Tuple[str, Multiform]

class Table:
   def __init__(self, caption, data):
      self.caption = caption
      self._data = data

   def __iter__(self):
      return self._data