from typing import Iterator
import random
import os
import yaml
from verb import Verb

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '\\a_sr_ru.yaml', encoding="utf-8") as f:
   data = yaml.load(f)
   letter_a = data['letter_a'][0]

def part_of_speech(key: str) -> type:
   value = letter_a[key]
   if 'i' in value:
      return Verb
   return type(None) # TODO other parts of speech

def lookup(raw_word: str) -> Iterator[Iterator[str]]:
   # TODO: lookup by partial keys in a dict? Really?
   # We ought to rethink the way we store data
   with_se = raw_word[-3:] == " се"
   if with_se:
      raw_word = raw_word[:-3]

   for key in letter_a.keys():
      key_without_disambiguator = key.split()[0]
      if raw_word == key_without_disambiguator:
         if part_of_speech(key) is Verb:
            verb = Verb(key, letter_a[key])
            if with_se and not verb.is_reflexive:
               continue
            yield verb.conjugate()
         elif with_se: # for skipping meaningless queries like "адвокат се"
            continue
         else:
            yield iter(["Ово није глагол 😞"]) # TODO

def random_word() -> Iterator[Iterator[str]]:
   while True:
      raw_word = random.choice(list(letter_a.keys()))
      if 'i' in letter_a[raw_word]:
         yield from lookup(raw_word)
         break
