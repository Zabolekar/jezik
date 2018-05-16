from typing import Any, Dict, Tuple
import os
import yaml
from .multidict import Multidict

Entry = Tuple[str, Dict[str, Any]]

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = dir_path + "/a_sr_ru.yaml"

data = Multidict[str, Entry]()

with open(file_path, encoding="utf-8") as f:
   raw_data = yaml.load(f)
   for full_key in raw_data.keys():
      # full_key is with disambiguator, key is without
      key = full_key.split()[0]
      pair = full_key, raw_data[full_key]
      data[key] = pair
