from typing import Dict
from os import path
import yaml
from .multidict import FancyLookup

data = FancyLookup()

dir_path = path.dirname(path.realpath(__file__))
file_path = path.join(dir_path, "data.yml")

with open(file_path, encoding="utf-8") as f:
   raw_data = yaml.safe_load(f)
   for full_key in raw_data.keys():
      # full_key is with disambiguator, key is without
      first_space = full_key.find(" ")
      if first_space != -1:
         key = full_key[:first_space]
         disambiguator = full_key[first_space+1:]
      else:
         key = full_key
         disambiguator = ""
      try:
         comment = raw_data[full_key]["c"]
      except KeyError:
         comment = ""
      if disambiguator and comment:
         caption = f"{disambiguator} ({comment})"
      else:
         caption = disambiguator + comment
      pair = caption, raw_data[full_key]
      data[key] = pair
