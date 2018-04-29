import re

def last_vowel_index(trunk: str) -> int:
   *__, last_vowel = re.finditer('[АаЕеИиОоУуAaEeIiOoUu\u0325]', trunk)
   index, _ = last_vowel.span()
   return index

def first_vowel_index(trunk: str) -> int:
    return re.search('[АаЕеИиОоУуAaEeIiOoUu\u0325]', trunk).span()[0]
