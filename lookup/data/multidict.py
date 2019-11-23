from typing import Dict, Generic, List, NamedTuple, Iterator, Tuple, TypeVar
import random
from ..utils import all_vowels, cyr2lat, deaccentize, expose, garde
from ..paradigm_helpers import accentize, i_to_accents

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
         self._data[key] = sorted(set(self._data[key]))
      else:
         self._data[key] = [value]

   def __iter__(self):
      return iter(self._data)

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
   caption: str
   type: str
   info: str
   replacements: Tuple[Replacement, ...]
   amendments: Tuple[Replacement, ...]


def inner_to_outer(s: str, accent: str) -> Iterator[Tuple[str, str]]:
   """
   Converts a word in our inner notation to its possible outer notations.
   E.g. зъʌ yields зао, zao; свꙓтъʌ yields светао, свијетао, svijetao etc.)
   """
   accent_dict = i_to_accents(accent)
   tmp = s + 'ø' if not s[-1] in all_vowels else s
   if 'ʟ' in tmp:
      tmp_list = [tmp.replace('ʟ', 'л'), tmp.replace('ʟ', 'ʌ')]
   elif 'Ъ' in tmp:
      tmp_list = [tmp.replace('Ъ', ''), tmp.replace('Ъ', 'ъ')]
   else:
      tmp_list = [tmp]


   for input_yat in ["e", "je", "ije"]:
      for item in tmp_list:
         accented_token = garde(accentize(item, accent_dict.r, accent_dict.v))
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
      if '\\' in value.info:
         first_substr = value.info.split(';')[0]
         first_accent = first_substr.split('\\')[1]
      else:
         first_accent = ""

      for outer_key, input_yat in inner_to_outer(inner_key, first_accent):
         outer_keys_ = outer_key.split('\\')
         for outer_key_ in outer_keys_:
            self._outer_to_inner[(outer_key_, input_yat)] = inner_key

   def random_key(self) -> Tuple[str, str]:
      return random.choice(list(self._outer_to_inner))
