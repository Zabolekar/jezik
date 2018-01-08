import re
from paradigms import GramInfo, Accents

def last_vowel_index(trunk: str) -> int:
   *__, last_vowel = re.finditer('[АаЕеИиОоУуAaEeIiOoUu̥]', trunk)
   index, _ = last_vowel.span()
   return index

def first_vowel_index(trunk: str) -> int:
    return re.search('[АаЕеИиОоУуAaEeIiOoUu̥]', trunk).span()[0]

def decipher(infos, typ: str) -> GramInfo:

   if infos:
      line_accents, AP, MP = infos.split('|')
      Rs = line_accents.split('@')[0] if '@' in infos else None
      Vs = line_accents.split('@')[1] if '@' in infos else line_accents
      accents = Accents(
          {int(i): '\u0325' for i in Rs[1:].split(',')} if Rs else {},
          {int(i[:-1]): i[-1] for i in Vs.split(',')} if line_accents else {}
      )
   else:
      accents, AP, MP = Accents({}, {}), "", ""

   if typ:
      splitted_typ = typ.split('|')
      POS = splitted_typ[0]
      other = splitted_typ[1:]

   return GramInfo(accents, AP, MP, POS, other)
