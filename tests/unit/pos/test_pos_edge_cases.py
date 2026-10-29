from ...entries import make_entry
from ....lookup.utils import characters as c
from ....lookup.paradigm_helpers import AccentedTuple
from ....lookup.pos import PartOfSpeech, _swap


def _pos(kind="N"):
   return PartOfSpeech("тест", make_entry("те̍ст", kind, "a./alpha"))


def test_swap_toggles_only_the_last_vowel_length():
   assert _swap("ра") == "ра" + c.macron
   assert _swap("ра" + c.macron) == "ра"
   assert _swap("р") == "р"
   assert PartOfSpeech.swap("ра", False, "a.", "b.") == "ра"


def test_accentize_preserves_old_paradigm_accents_and_adds_new_ones():
   assert PartOfSpeech.accentize("a.", "те·ст") == "те" + c.straight + "ст"
   assert PartOfSpeech.accentize("o.", "те" + c.straight + "·ст") == "те" + c.straight + "ст"


def test_connectendum_handles_syllabic_r_and_special_verb_markers():
   verb = _pos("V\\Tr\\Ipf\\extra")

   consonant_ending = verb._connectendum("a.", "бр", AccentedTuple("т", ""))
   vowel_ending = verb._connectendum("a.", "бр" + c.macron, AccentedTuple("а", ""))
   marker_ending = verb._connectendum("e", "те̍ст", AccentedTuple(">>ʘ·а", "e"))

   assert consonant_ending == [["бр" + c.ring, "т"]]
   assert vowel_ending == [["бр", "а"]]
   assert marker_ending == [["тест", "·а"]]


def test_process_one_form_produces_soft_and_hard_stem_variants():
   forms = _pos().process_one_form("a.", "путʲ", [AccentedTuple("œ", "")])

   assert forms == ["пу̍тʲœ", "пу̍тœ"]


def test_process_one_form_accents_a_yer_when_there_are_no_vowels():
   forms = _pos().process_one_form("a.", "съ", [AccentedTuple("ø", "")])

   assert forms == ["съ" + c.straight + "ø"]


def test_part_of_speech_takes_everything_from_the_entry():
   word = PartOfSpeech("тест\\ми", make_entry(
      "те̍ст", "N\\m", "a.;b./x",
      replacements=(("pl gen", ["а, б"]),),
      amendments=(("sg nom", ["в"]),)
   ))

   assert word.key == "тест"
   assert word.kind == "N\\m"
   assert word.gram.AP == ["a.", "b."]
   assert word.accented_keys == ["те̍ст", "те̍ст"] # copied for each accent paradigm
   assert word.replacements == {"pl gen": ["а, б"]}
   assert word.amendments == {"sg nom": ["в"]}
   assert word.label("m")
