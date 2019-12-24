from os import path
from re import search as rsearch
import yaml
from ..charutils import all_vowels, plain_accents
from .multidict import Entry, FancyLookup
from ..utils import deaccentize, cyr2lat

data = FancyLookup()

dir_path = path.dirname(path.realpath(__file__))
file_path = path.join(dir_path, "data.yml")

posdict = {"N": "именица", "V": "глагол", "A": "придев", "B": "прилог"}

with open(file_path, encoding="utf-8") as f:
   raw_data = yaml.safe_load(f)
for full_key in raw_data.keys():
   if rsearch(f"[^{all_vowels}ъ][{plain_accents}]", full_key):
      raise ValueError(full_key) # TODO WHY doesn't it work??
   # full_key is with disambiguator, key is without
   first_space = full_key.find(" ")
   if first_space != -1:
      accented_keys_with_extra_key : str = full_key[:first_space]
      disambiguator = full_key[first_space+1:] + ":"
   else:
      accented_keys_with_extra_key : str = full_key
      disambiguator = ""
   if '\\' in accented_keys_with_extra_key:
      accented_keys, extra_key = accented_keys_with_extra_key.split("\\", 1)
   else:
      accented_keys = accented_keys_with_extra_key
      extra_key = ''
   unaccented_keys = deaccentize(accented_keys).split(',')
   assert len(set(unaccented_keys)) == 1, unaccented_keys
   try:
      comment = "(" + raw_data[full_key]["c"] + ")"
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

   caption = f"{disambiguator} {current_pos} {comment}"
   new_entry = Entry(
      caption,
      accented_keys,
      extra_key,
      raw_entry["t"],
      raw_entry["i"],
      tuple(replacements.items()),
      tuple(amendments.items())
   )
   data[unaccented_keys[0]] = new_entry
