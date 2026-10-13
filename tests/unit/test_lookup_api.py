import pytest # type: ignore

from ...lookup import lazy_lookup, lookup, part_of_speech, random_key
from ...lookup.adjective import Adjective
from ...lookup.adverb import Adverb
from ...lookup.data.multidict import Entry
from ...lookup.noun import Noun
from ...lookup.verb import Verb
from ...lookup import ACCENTS_NOT_FOUND_MESSAGE

@pytest.mark.parametrize(("kind", "expected"), [
   ("V\\Tr", Verb),
   ("A", Adjective),
   ("N\\m", Noun),
   ("B", Adverb),
   ("X", None),
])
def test_part_of_speech_recognizes_supported_kinds(kind, expected):
   assert part_of_speech(kind) is expected


def test_lookup_normalizes_jekavian_input_and_rejects_invalid_modes():
   assert lookup("свијет", input_yat="je")["sg nom"].multiform == ["свйје̑т"]
   assert not lookup("свет", input_yat="invalid")
   assert not lookup("свет", output_yat="invalid")


def test_lookup_requires_reflexive_marker_to_match_a_reflexive_verb():
   assert lookup("бој")[0].pos == "noun"
   assert lookup("бојати се")["infinitive"].multiform == ["бо̀јати се"]
   assert not lookup("адвокат се")


@pytest.mark.parametrize(("query", "expected"), [
   ("БОЈАТИ СЕ", ["бо̀јати се"]),
   ("БоЈаТи Се", ["бо̀јати се"]),
   ("BOJATI SE", ["bòjati se"]),
   ("BoJaTi Se", ["bòjati se"]),
])
def test_lookup_recognizes_reflexive_particle_regardless_of_case(query, expected):
   assert lookup(query)["infinitive"].multiform == expected


def test_lookup_rejects_uppercase_non_reflexive_word_with_reflexive_particle():
   assert not lookup("АДВОКАТ СЕ")


def test_lazy_lookup_exposes_a_helpful_table_for_an_unknown_part_of_speech(monkeypatch):
   entry = Entry(("непознато", ""), "те̍ст", "", "X", "a./", (), ())

   class FakeData:
      def __getitem__(self, _):
         return iter([("тест", entry)])

   monkeypatch.setitem(lazy_lookup.__globals__, "data", FakeData())

   table = list(lazy_lookup("тест", "e", "e"))[0]

   assert table.pos == ""
   assert list(table) == ACCENTS_NOT_FOUND_MESSAGE


def test_random_key_delegates_to_the_data_index(monkeypatch):
   class FakeData:
      def random_key(self):
         return "реч", "ije"

   monkeypatch.setitem(random_key.__globals__, "data", FakeData())

   assert random_key() == ("реч", "ije")
