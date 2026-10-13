from ....lookup.noun import Noun
from ....lookup.noun.paradigms import male_gen_pl_marked


def test_noun_rejects_impossible_single_vowel_marked_genitive_plural():
   assert not Noun._noun_form_is_possible("а", male_gen_pl_marked[0], "c.")
   assert Noun._noun_form_is_possible("а", male_gen_pl_marked[0], "a.")
   assert Noun._noun_form_is_possible("аба", male_gen_pl_marked[0], "c.")


def test_noun_with_only_amendments_returns_the_prescribed_forms():
   noun = Noun("тест", "те̍ст", "N", "0/", (), (("custom_form", ["те̍ст"]),))

   assert list(noun.multiforms()) == [("custom form", ["те̏ст"])]


def test_neuter_e_stem_uses_the_soft_stem_marker():
   noun = Noun("море", "мо̍ре", "N\\n", "a./", (), ())

   assert noun.trunk == ["мо̍рʲ"]
