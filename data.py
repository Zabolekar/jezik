from typing import Iterator, Dict, Tuple, Any
import random
import os
import yaml

class Data:
   def __init__(self, path: str) -> None:
      with open(path, encoding="utf-8") as f:
         self._data = yaml.load(f)

   def all_entries(self, raw_word: str) -> Iterator[Tuple[str, Dict[str, Any]]]:
      # TODO: lookup by partial keys in a dict? Really?
      # We ought to rethink the way we store data
      for key in self._data.keys():
         key_without_disambiguator = key.split()[0]
         if raw_word == key_without_disambiguator:
            yield key, self._data[key]

   def random_key(self) -> str:
      return random.choice(list(self._data.keys()))

dir_path = os.path.dirname(os.path.realpath(__file__))
data = Data(dir_path + '\\a_sr_ru.yaml')