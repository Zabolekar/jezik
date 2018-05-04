from typing import Any, Dict, Tuple, List
import random
import os
import yaml

Entry = Tuple[str, Dict[str, Any]]

class Data:
   def __init__(self, path: str) -> None:
      with open(path, encoding="utf-8") as f:
         raw_data = yaml.load(f)
         # ad-hoc multidict
         self._data: Dict[str, List[Entry]] = {}  
         for full_key in raw_data.keys():
            # full_key is with disambiguator, key is without
            key = full_key.split()[0]
            pair = full_key, raw_data[full_key]
            if key in self._data:
               self._data[key].append(pair)
            else:
               self._data[key] = [pair]

   def __getitem__(self, word: str) -> List[Entry]:
      try:
         return self._data[word]
      except KeyError:
         return []

   def random_key(self) -> str:
      return random.choice(list(self._data.keys()))

dir_path = os.path.dirname(os.path.realpath(__file__))
data = Data(dir_path + '\\a_sr_ru.yaml')
