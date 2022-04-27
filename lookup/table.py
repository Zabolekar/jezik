from __future__ import annotations
from typing import Iterable, Iterator, List, Tuple, Union
from .paradigm_helpers import TableCaption

Form = str
Multiform = List[Form]
LabeledMultiform = Tuple[str, Multiform]

class Table:
   def __init__(self, pos:str, caption:TableCaption, data:Iterable[LabeledMultiform]) -> None:
      self.caption = caption
      self.pos = pos
      self._data = list(data)

   def __getitem__(self, query:str) -> Table:
      result = []
      query_grammemes = query.split()
      for form_name, forms in self._data:
         target_grammemes = form_name.split()
         if all(s in target_grammemes for s in query_grammemes):
            result.append((form_name, forms))
      return Table(
         f"partial {self.pos}",
         TableCaption(
            self.caption.caption,
            self.caption.par,
            self.caption.subpar,
            f"{self.caption.caption} [{query}]"
         ),
         result
      )

   @property
   def multiform(self) -> List[str]: # TODO: document in README, rethink
      if len(self._data) != 1:
         raise AttributeError(
            "A 'Table' object has an attribute 'multiform' if and only if it has exactly one cell"
         )
      return self._data[0][1]

   def __repr__(self) -> str:
      result = self.caption.full_caption + "\n"
      name_widths = (len(form_name) for form_name, _ in self._data)
      column_width = max(name_widths, default=0) + 5
      if self._data:
         for form_name, forms in self._data:
            result += f"{form_name:{column_width}}{', '.join(forms)}\n"
      else:
         result += "Form not found\n"
      return result

   def __iter__(self) -> Iterator[LabeledMultiform]:
      return iter(self._data)

   def __len__(self) -> int:
      return len(self._data)

class Multitable:
   def __init__(self, input_word:str, tables:Iterator[Table]) -> None:
      self._tables = list(tables)
      self.input = input_word

   def __repr__(self) -> str:
      if self._tables:
         return "\n".join(str(table) for table in self._tables)
      return "Word not found"

   def __getitem__(self, query:Union[int, str]) -> Union[Multitable, Table]:
      if isinstance(query, int):
         return self._tables[query]
      else:
         n_tables = len(self._tables)
         if n_tables == 0:
            raise ValueError("You can't index an empty multitable")
         elif n_tables == 1:
            return self[0][query]
         else:
            print("There's more than one table, consider using explicit indexing!", end="\n\n")
            return Multitable(self.input, (table[query] for table in self._tables))

   def __len__(self) -> int:
      return len(self._tables)

   def __bool__(self) -> bool:
      return bool(self._tables)
