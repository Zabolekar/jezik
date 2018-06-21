from typing import Iterator, Tuple

GenericTable = Iterator # TODO: it's not a simple iterator

Form = str
Multiform = Iterator[Form]
LabeledMultiform = Tuple[str, Multiform]
Table = GenericTable[LabeledMultiform]
