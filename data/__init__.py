from typing import Any, Dict, Tuple
from os import path
import yaml
from .multidict import Multidict

Entry = Tuple[str, Dict[str, Any]]
data = Multidict[str, Entry]()

dir_path = path.dirname(path.realpath(__file__))
file_path = path.join(dir_path, "data.yml")

with open(file_path, encoding="utf-8") as f:
   raw_data = yaml.safe_load(f)
   for full_key in raw_data.keys():
      # full_key is with disambiguator, key is without
      key = full_key.split()[0]
      pair = full_key, raw_data[full_key]
      data[key] = pair
