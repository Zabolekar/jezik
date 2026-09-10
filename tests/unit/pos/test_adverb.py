from ....lookup.adverb import Adverb


def test_exposes_each_accented_key():
   adverb = Adverb("узалуд", "у¨залу_д,у´залу_д", "B", "0", (), ())

   _, forms = next(adverb.multiforms())

   assert forms == ["у̏залӯд", "у́залӯд"]
