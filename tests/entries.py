from ..lookup.data.multidict import Entry, Replacement

def make_entry(
   accented_keys:str,
   kind:str,
   info:str,
   replacements:tuple[Replacement, ...]=(),
   amendments:tuple[Replacement, ...]=()
) -> Entry:
   """Makes a data entry the way data/__init__.py does, for tests that build words by hand."""
   return Entry(
      ("", ""), accented_keys, "", kind, info, replacements, amendments
   )
