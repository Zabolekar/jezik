import pytest # type: ignore

from ....lookup.noun import Noun
from ....lookup.noun.paradigms import f_declension_a


def test_feminine_plural_accusative_uses_cyrillic_ie():
   ending = f_declension_a[8][0][0].morpheme

   assert ending == "е·"
   assert "e" not in ending


@pytest.mark.parametrize(("first_mode", "expected_first", "expected_second"), [
   ("i", ["ма̀глӣ"], ["ма́гла̄"]),
   ("j", ["ма́гла̄", "ма̀глӣ"], ["ма́гла̄"]),
])
def test_feminine_genitive_plural_overrides_do_not_leak_between_variants(
   first_mode, expected_first, expected_second
):
   noun = Noun(
      "магла", "ма`гла,ма´гла", "N\\f", f"b./{first_mode};b$", (), ()
   )

   forms = list(noun.multiforms())

   assert dict(forms[:14])["pl gen"] == expected_first
   assert dict(forms[14:])["pl gen"] == expected_second
