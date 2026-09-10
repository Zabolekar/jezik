from ....lookup.noun.paradigms import f_declension_a


def test_feminine_plural_accusative_uses_cyrillic_ie():
   ending = f_declension_a[8][0][0].morpheme

   assert ending == "е·"
   assert "e" not in ending
