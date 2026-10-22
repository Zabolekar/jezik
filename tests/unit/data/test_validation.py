import pytest # type: ignore
from ....lookup.data.validation import validate_entry


def ok(**overrides):
   entry = {"t": "N\\m", "i": "a."}
   entry.update(overrides)
   return entry


def test_valid_entries_pass():
   validate_entry("а`б", ok(), "а`б")
   validate_entry("а`б", {"t": "A\\all", "i": "A."}, "а`б")
   validate_entry("а`б", {"t": "V\\Tr\\Pf", "i": "a./alpha"}, "а`б")


@pytest.mark.parametrize("entry, keys, message", [
   ("not a mapping", "а", "mapping"),
   ({"i": "a."}, "а", "'t'"),
   ({"t": "N\\m"}, "а", "'i'"),
   ({"t": "N\\m", "i": ""}, "а", "'i'"),
   (ok(**{"except": ["x"]}), "а", "except"),
   (ok(add={"pl gen": 5}), "а", "add"),
   (ok(), "а,", "empty accented key"),
   (ok(), "а,б", "accent paradigms"),
   ({"t": "A\\bogus", "i": "A."}, "а", "adjective type"),
   ({"t": "A", "i": "A."}, "а", "adjective type"),
   ({"t": "A\\all", "i": "zz"}, "а", "adjective accent"),
   ({"t": "V\\Pf", "i": "a./omega"}, "а", "verb paradigm"),
])
def test_invalid_entries_are_rejected_with_the_key(entry, keys, message):
   with pytest.raises(ValueError, match=message) as error:
      validate_entry("ключ", entry, keys)
   assert "ключ" in str(error.value) or message == "mapping"
