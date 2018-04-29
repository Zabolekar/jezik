import re
from paradigms import GramInfo, Accents

def last_vowel_index(trunk: str) -> int:
   *__, last_vowel = re.finditer('[АаЕеИиОоУуAaEeIiOoUu\u0325]', trunk)
   index, _ = last_vowel.span()
   return index

def first_vowel_index(trunk: str) -> int:
    return re.search('[АаЕеИиОоУуAaEeIiOoUu\u0325]', trunk).span()[0]

def decipher(infos, types: str) -> GramInfo:

   if infos:
      line_accents, AP, MP = infos.split('|')
      if '@' in infos:
         Rs, Vs = line_accents.split('@')
      else:
         Rs, Vs = None, line_accents
      accents = Accents(
          {int(i): '\u0325' for i in Rs[1:].split(',')} if Rs else {},
          {int(i[:-1]): i[-1] for i in Vs.split(',')} if line_accents else {}
      )
   else:
      raise ValueError("Can't decipher empty i")

   if types:
      POS, *other = types.split('|')
   else:
      raise ValueError("Can't decipher empty t")

   return GramInfo(accents, AP, MP, POS, other)
