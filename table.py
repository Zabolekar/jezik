from typing import Iterator

GenericTable = Iterator # TODO: it's not a simple iterator

Form = str
Multiform = Iterator[Form]
Table = GenericTable[Multiform]
Multitable = Iterator[Table]