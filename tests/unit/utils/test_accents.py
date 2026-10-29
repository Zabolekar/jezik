import pytest # type: ignore
from ....lookup.utils import characters as c
from ....lookup.utils.accents import ungarde, garde, make_recessive

def test_ungarde():
   assert [ungarde(i) for i in [
   "do\u030dbar", "da\u0304\u030dn", "noga\u030d",
   "lju\u0304\u030ddi", "lju\u0304di\u0304\u030d",
   "до\u030dбар", "да\u0304\u030dн", "нога\u030d",
   "љу\u0304\u030dди", "љу\u0304ди\u0304\u030d",
   "асимили\u0304\u030dра\u0304м", "адвокати\u0304ра\u030dо",
   "хал!о\u0304\u030d", "зафр\u0325к!а\u030dнт",
   "ср\u0325\u030dпскохр\u0325ва\u0304\u030dтски\u0304",
   "хр\u0325ва\u0304\u030dтскоср!\u0325\u030dпски\u0304", "к"]] == [
   "do\u030fbar", "da\u0311n", "no\u0300ga",
   "lju\u0311di", "ljúdi\u0304",
   "до\u030fбар", "да\u0311н", "но\u0300га",
   "љу\u0311ди", "љу́ди\u0304",
   "асими\u0300ли\u0304ра\u0304м", "адвокати́рао",
   "хало\u0311", "зафр\u0325ка\u030fнт",
   "ср\u0325\u030fпскохр\u0325\u0300ва\u0304тски\u0304",
   "хр\u0325\u0300ва\u0304тскоср\u0325\u030fпски\u0304", "к"]


def test_ungarde_additional_bang():
   assert ungarde("пла̄во̍с!ӣва̍") == ungarde("пла̄во̍сӣва̍") == "пла́воси́ва"


def test_garde():
   assert [garde(i) for i in [
   "do\u030fbar", "dȃn", "no\u0300ga",
   "lju\u0311di", "ljúdi\u0304",
   "до\u030fбар", "да̑н", "но\u0300га",
   "љу\u0311ди", "љу́ди\u0304",
   "асими\u0300ли\u0304ра\u0304м", "адвокати\u0301рао",
   "хало\u0311", "зафр\u0325ка\u030fнт",
   "ср\u0325\u030fпскохр\u0325\u0300ва\u0304тски\u0304",
   "хр\u0325\u0300ва\u0304тскоср\u0325\u030fпски\u0304", "к"]] == [
   "do\u030dbar", "da\u0304\u030dn", "noga\u030d",
   "lju\u0304\u030ddi", "lju\u0304di\u0304\u030d",
   "до\u030dбар", "да\u0304\u030dн", "нога\u030d",
   "љу\u0304\u030dди", "љу\u0304ди\u0304\u030d",
   "асимили\u0304\u030dра\u0304м", "адвокати\u0304ра\u030dо",
   "хал!о\u0304\u030d", "зафр\u0325к!а\u030dнт",
   "ср\u0325\u030dпскохр\u0325ва\u0304\u030dтски\u0304",
   "хр\u0325ва\u0304\u030dтскоср!\u0325\u030dпски\u0304", "к"]


def test_make_recessive_puts_the_accent_on_the_first_vowel():
   assert make_recessive(f"вода0{c.straight}") == f"во{c.straight}да"


def test_make_recessive_turns_tilde_into_macron():
   assert make_recessive(f"мо0{c.straight}~ре") == f"мо{c.straight}{c.macron}ре"


def test_make_recessive_leaves_forms_without_the_zero_marker_alone():
   assert make_recessive("вода") == "вода"


def test_make_recessive_rejects_forms_without_vowels():
   with pytest.raises(ValueError):
      make_recessive(f"р0{c.straight}")
