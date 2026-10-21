from ....lookup.adverb import Adverb


def test_exposes_each_accented_key():
   adverb = Adverb("узалуд", "у¨залу_д,у´залу_д", "B", "0", (), ())

   _, forms = next(adverb.multiforms())

   assert forms == ["у̏залӯд", "у́залӯд"]


def test_variant_selects_a_single_accented_key():
   adverb = Adverb("узалуд", "у¨залу_д,у´залу_д", "B", "0", (), ())
   _, both = next(adverb.multiforms())

   assert next(adverb.multiforms(variant=0))[1] == [both[0]]
   assert next(adverb.multiforms(variant=1))[1] == [both[1]]
