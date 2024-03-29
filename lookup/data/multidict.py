from typing import Dict, Generic, List, NamedTuple, Iterator, Tuple, TypeVar
import random
from ..utils import cyr2lat, deaccentize, expose, garde
from ..paradigm_helpers import accentize, uniq
from ..charutils import all_vowels, c

Replacement = Tuple[str, List[str]]

KT = TypeVar("KT")
VT = TypeVar("VT")

class Multidict(Generic[KT, VT]):
   """
   A key can correspond to zero or more values.
   There are no KeyErrors: no values are not an error, just a special case.
   Values are unique. Then why do we use a List and not a Set, you may ask?
   Because we need consistent order for testing.
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
         self._data[key] = list(set(self._data[key]))
         self._data[key].sort()
      else:
         self._data[key] = [value]

   def __iter__(self):
      return iter(self._data)

   def __len__(self):
      return len(self._data)

# This Multidict was good enough for some time, but it didn't allow us to
# look a word up using more than one notation. Furthermore, the only supported
# notation was the one we use to store words in the data.yml (see NOTATION.md),
# which is impractical because it doesn't correspond to any orthography in use.

# A word is _defined_ by its inner representation AKA inner key. It can have
# multiple outer representations AKA outer keys (i.e. ways it can be written in
# some real-world orthography), usually two (Latin and Cyrillic) but sometimes
# more due to e.g. yat reflexes. Outer representations of different words can
# coincide (e.g. свет can be an outer representation of both свет and свꙓт).

class Entry(NamedTuple):
   caption: Tuple[str, str]
   accented_keys: str
   extra_key: str
   type: str
   info: str
   replacements: Tuple[Replacement, ...]
   amendments: Tuple[Replacement, ...]


def inner_to_outer(accented_keys:str, extra_key:str) -> Iterator[Tuple[str, str]]:
   """
   Converts a word in our inner notation to its possible outer notations.
   E.g. зъʌ yields зао, zao; свꙓтъʌ yields светао, свијетао, svijetao etc.)
   """
   keys = accented_keys.split(',')
   big_tmp_list : List[str] = []
   for k in keys:
      tmp = k + 'ø' if not k[-1] in all_vowels + '_' else k
      if 'ʟ' in tmp:
         tmp_list = [tmp.replace('ʟ', 'л'), tmp.replace('ʟ', 'ʌ')]
      elif 'Ъ' in tmp:
         tmp_list = [tmp.replace('Ъ', ''), tmp.replace('Ъ', 'ъ')]
      else:
         tmp_list = [tmp]
      big_tmp_list += tmp_list
   unique_keys = uniq(big_tmp_list)

   for input_yat in ["e", "je", "ije"]:
      if extra_key:
         extra_token = deaccentize(
            expose(
               form=garde(accentize(extra_key)),
               yat=input_yat
            ).lower()
         )
         yield extra_token, input_yat
         yield cyr2lat(extra_token), input_yat
      for item in unique_keys:
         if (accented_token := garde(accentize(item))) == item:
            raise ValueError(f"accented token {accented_token} shouldn't be equal to {item}")
         exposed_token = expose(accented_token, yat=input_yat)
         deaccentized_token = deaccentize(exposed_token).lower()
         yield deaccentized_token, input_yat
         yield cyr2lat(deaccentized_token), input_yat


class FancyLookup:

   def __init__(self) -> None:
      self._inner_to_entries = Multidict[str, Entry]()
      self._outer_to_inner = Multidict[Tuple[str, str], str]()
      # in this Tuple[str, str] the first str is the outer key and the second is the yat mode

   def __getitem__(self, key_with_mode: Tuple[str, str]) -> Iterator[Tuple[str, Entry]]:
      outer_key, input_yat = key_with_mode
      inner_keys = self._outer_to_inner[(outer_key.lower(), input_yat)]
      for key in inner_keys:
         for entry in self._inner_to_entries[key]:
            yield key, entry

   def __setitem__(self, inner_key: str, value: Entry) -> None:
      self._inner_to_entries[inner_key] = value

      for outer_key, input_yat in inner_to_outer(value.accented_keys, value.extra_key):
         self._outer_to_inner[(outer_key, input_yat)] = inner_key

   def random_key(self) -> Tuple[str, str]:
      return random.choice(list(self._outer_to_inner))
