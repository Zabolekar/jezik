from ....lookup.data.multidict import Entry, Multidict


def test_accepts_unhashable_entries_and_removes_duplicates():
   """Entries contain replacement lists, so they deliberately are unhashable."""
   entry = Entry(
      ("caption", ""), "key", "", "N\\f", "a.",
      (("sg gen", ["форме"]),), (), None
   )
   other_entry = Entry(
      ("other", ""), "other", "", "N\\f", "a.",
      (("sg gen", ["друге форме"]),), (), None
   )
   values = Multidict[str, Entry]()

   values["word"] = entry
   values["word"] = entry
   values["word"] = other_entry

   assert values["word"] == [entry, other_entry]
