from typing import Any
from ..paradigm_helpers import GramInfo, adj_AP_to_inner_AP, infinitive_dict

ADJECTIVE_KINDS = ("all", "ov", "ski")

def validate_entry(full_key:str, raw_entry:Any, accented_keys:str) -> None:
   """
   Checks that a raw data.yml entry is well-formed, so that mistakes are
   reported when the data is loaded and not when the word is looked up.
   Raises ValueError with the offending key.
   """
   def fail(message:str) -> None:
      raise ValueError(f"{full_key}: {message}")

   if not isinstance(raw_entry, dict):
      fail("entry must be a mapping")
   for field in ("t", "i"):
      if not isinstance(raw_entry.get(field), str) or not raw_entry[field]:
         fail(f"missing or empty field '{field}'")
   for field in ("except", "add"):
      section = raw_entry.get(field, {})
      if not isinstance(section, dict) or not all(
         isinstance(k, str) and isinstance(v, str) for k, v in section.items()
      ):
         fail(f"'{field}' must map labels to strings")

   keys = accented_keys.split(",")
   if not all(keys):
      fail("empty accented key")

   kind = raw_entry["t"]
   gram = GramInfo(kind, raw_entry["i"].split(";"))
   if len(keys) > 1 and len(keys) != len(gram.AP):
      fail(f"{len(keys)} accented keys but {len(gram.AP)} accent paradigms")

   if gram.POS == "A":
      if not gram.other or gram.other[0] not in ADJECTIVE_KINDS:
         fail(f"adjective type must be one of {ADJECTIVE_KINDS}")
      for AP in gram.AP:
         if AP not in adj_AP_to_inner_AP:
            fail(f"unknown adjective accent paradigm '{AP}'")
   elif gram.POS == "V":
      for MP in gram.MP:
         if MP not in infinitive_dict:
            fail(f"unknown verb paradigm '{MP}'")
