from typing import Any, Dict, Generic, List, Iterator, Tuple, TypeVar
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

# This Multidict was good enough for some time, but it didn't allow us to
# look a word up using more than one notation. Furthermore, the only supported
# notation was the one we use to store words in the data.yml (see NOTATION.md),
# which is impractical because it doesn't correspond to any orthography in use.

# A word is _defined_ by its inner representation AKA inner key. It can have
# multiple outer representations AKA outer keys (i.e. ways it can be written in
# some real-world orthography), usually two (Latin and Cyrillic) but sometimes
# more due to e.g. yat reflexes. Outer representations of different words can
# coincide (e.g. свет can be an outer representation of both свет and свꙓт).

Entry = Tuple[str, str, Dict[str, Any]] # inner key, caption, info

def inner_to_outer(s: str) -> Iterator[str]:
   """
   Converts a word in our inner notation to its possible outer notations.
   E.g. зъʌ yields зао, zao; свꙓтъʌ yields светао, свијетао, svijetao etc.)
   """
   # TODO this is too simple to work as intended, consider using utils.py
   # TODO: Latin
   tmp = s.replace("ъ", "а").replace("ʌ", "о")
   if "ꙓ" in tmp:
      yield tmp.replace("ꙓ", "е")
      yield tmp.replace("ꙓ", "ије")
   else:
      yield tmp

class FancyLookup:

   def __init__(self) -> None:
      self._inner_to_entries = Multidict[str, Entry]()
      self._outer_to_inner = Multidict[str, str]()

   def __getitem__(self, outer_key: str) -> List[Entry]:
      result = []
      inner_keys = self._outer_to_inner[outer_key]
      for key in inner_keys:
         result.extend(self._inner_to_entries[key])
      return result

   def __setitem__(self, inner_key: str, value: Entry) -> None:
      self._inner_to_entries[inner_key] = value

      for outer_key in inner_to_outer(inner_key):
         self._outer_to_inner[outer_key] = inner_key

   def random_key(self) -> str:
      return random.choice(list(self._outer_to_inner._data.keys()))
