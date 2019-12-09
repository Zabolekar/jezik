from os import path
import yaml
from .multidict import Entry, FancyLookup

data = FancyLookup()

dir_path = path.dirname(path.realpath(__file__))
file_path = path.join(dir_path, "data.yml")

posdict = {"N": "именица", "V": "глагол", "A": "придев", "B": "прилог"}

with open(file_path, encoding="utf-8") as f:
   raw_data = yaml.safe_load(f)
   for full_key in raw_data.keys():
      # full_key is with disambiguator, key is without
      first_space = full_key.find(" ")
      if first_space != -1:
         key = full_key[:first_space]
         disambiguator = full_key[first_space+1:] + ":"
      else:
         key = full_key
         disambiguator = ""
      try:
         comment = raw_data[full_key]["c"]
      except KeyError:
         comment = ""
      try:
         replacements = {x: y.split(", ") for x, y in raw_data[full_key]["except"].items()}
      except KeyError:
         replacements = {}
      try:
         amendments = {x: y.split(", ") for x, y in raw_data[full_key]["add"].items() }
      except KeyError:
         amendments = {}

      raw_entry = raw_data[full_key]
      current_pos = posdict[raw_entry["t"][0]]

      if disambiguator and comment:
         caption = f"{disambiguator} {current_pos} ({comment})"
      else:
         caption = f"{disambiguator} {current_pos} {comment}"

      data[key] = Entry(
         caption,
         raw_entry["t"],
         raw_entry["i"],
         tuple(replacements.items()),
         tuple(amendments.items())
      )
