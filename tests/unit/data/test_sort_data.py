from io import StringIO

import pytest # type: ignore
import yaml

from ....lookup.adverb import Adverb
from ....lookup.data.sort_data import print_entry, to_direct, to_reverse


@pytest.mark.parametrize("info", [
   "0", "001", "yes", "null", "2026-10-13", "note: value", "note # value",
])
def test_print_entry_preserves_string_metadata(info):
   entry = {"t": "B", "i": info}
   output = StringIO()

   print_entry("у¨залу_д", entry, file=output)

   assert yaml.safe_load(output.getvalue()) == {"у¨залу_д": entry}


def test_print_entry_preserves_nested_forms_and_field_order():
   entry = {
      "add": {"pl gen": "ну´ла_, ну^ла_"},
      "v": "нула",
      "except": {"sg gen": "0"},
      "i": "a.",
      "c": "напомена: знак # остаје",
      "t": "N\\f",
   }
   output = StringIO()

   print_entry("ну¨ла I", entry, file=output)
   restored = yaml.safe_load(output.getvalue())

   assert restored == {"ну¨ла I": entry}
   assert list(restored["ну¨ла I"]) == ["t", "i", "c", "v", "add", "except"]


@pytest.mark.parametrize(("sorter", "expected_keys"), [
   (to_direct, ["а¨бонос", "а¨ван", "у¨залу_д"]),
   (to_reverse, ["у¨залу_д", "а¨ван", "а¨бонос"]),
])
def test_sorting_preserves_dictionary_data_and_usable_metadata(tmp_path, sorter, expected_keys):
   entries = {
      "у¨залу_д": {"t": "B", "i": "0"},
      "а¨ван": {"t": "N\\m", "i": "a."},
      "а¨бонос": {
         "t": "N\\m", "i": "a.",
         "except": {"sg gen": "а¨боноса"},
         "add": {"pl gen": "а¨боноса_, а`боноса_"},
      },
   }
   input_path = tmp_path / "input.yml"
   output_path = tmp_path / "output.yml"
   input_path.write_text(yaml.safe_dump(entries, allow_unicode=True), encoding="utf-8")

   sorter(input_path, output_path)
   output = output_path.read_text(encoding="utf-8")
   restored = yaml.safe_load(output)

   assert output.startswith("%YAML 1.1\n---\n")
   assert restored == entries
   assert list(restored) == expected_keys
   adverb_entry = restored["у¨залу_д"]
   adverb = Adverb("узалуд", "у¨залу_д", adverb_entry["t"], adverb_entry["i"])
   assert list(adverb.multiforms()) == [("", ["у̏залӯд"])]
