import pytest # type: ignore
from ...lookup.utils import (
   ungarde, garde, deyerify, expose_replacement, insert, assimilate, make_recessive, deaccentize,
   strip_suffix
)
from ...lookup.charutils import c, notation_marks

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

def test_deyerify():
   assert [deyerify(i) for i in [
   "небъце", "тежъко", "кљунорожъци", "властъни"]] == [
   "непце", "тешко", "кљунорошци", "власни"]

def test_insert():
   word = "аустроугарски\u0304"
   assert [insert(word, {x: '!', 7: '\u030f'}) for x in range(0, len(word))] == [
   "!аустроу\u030fгарски\u0304",
   "а!устроу\u030fгарски\u0304",
   "ау!строу\u030fгарски\u0304",
   "аус!троу\u030fгарски\u0304",
   "ауст!роу\u030fгарски\u0304",
   "аустр!оу\u030fгарски\u0304",
   "аустро!у\u030fгарски\u0304",
   "аустроу\u030fгарски\u0304",
   "аустроу\u030fг!арски\u0304",
   "аустроу\u030fга!рски\u0304",
   "аустроу\u030fгар!ски\u0304",
   "аустроу\u030fгарс!ки\u0304",
   "аустроу\u030fгарск!и\u0304",
   "аустроу\u030fгарски!\u0304"
   ]

def test_assimilate():
   assert [assimilate(word, "je") for word in [
       "цꙓ̄лѣ\u030dти", "бѣлѣ\u030dжӣм", "ви\u030dдѣʌ"]] == [
   "цйје̄ље\u030dти", "биље\u030dжӣм", "ви\u030dдио"]
   assert [assimilate(word, "e") for word in [
       "цꙓ̄лѣ\u030dти", "бѣлѣ\u030dжӣм", "ви\u030dдѣʌ"]] == [
   "це̄ле\u030dти", "беле\u030dжӣм", "ви\u030dдео"]

def test_expose_replacement_preserves_long_yat_before_traditional_accent():
   form = "звꙓ´ри_"

   assert expose_replacement(form, "e") == "зве́рӣ"
   assert expose_replacement(form, "je") == "звйје́рӣ"
   assert expose_replacement(form, "ije") == "звијѐрӣ"

def test_strip_suffix():
   s = "abcdefghi"
   assert strip_suffix(s, ["fghi"]) == ("abcde", True)
   assert strip_suffix(s, ["gggg"]) == (s, False)
   assert strip_suffix(s, [""]) == (s, True)
   assert strip_suffix(s, ["ggghi", "gghi", "ghi", "hi", "i"]) == ("abcdef", True)
   assert strip_suffix(s, []) == (s, False)


def test_make_recessive_puts_the_accent_on_the_first_vowel():
   assert make_recessive(f"вода0{c.straight}") == f"во{c.straight}да"


def test_make_recessive_turns_tilde_into_macron():
   assert make_recessive(f"мо0{c.straight}~ре") == f"мо{c.straight}{c.macron}ре"


def test_make_recessive_leaves_forms_without_the_zero_marker_alone():
   assert make_recessive("вода") == "вода"


def test_make_recessive_rejects_forms_without_vowels():
   with pytest.raises(ValueError):
      make_recessive(f"р0{c.straight}")


def test_deyerify_lengthens_vowel_before_sonorant_and_lost_yer():
   assert deyerify(f"ва{c.straight}рък") == f"ва{c.straight}{c.macron}рк"


def test_deyerify_moves_accent_stranded_on_a_consonant_to_the_vowel():
   assert deyerify(f"авио{c.macron}н{c.straight}") == f"авио{c.straight}{c.macron}н"


def test_deaccentize_removes_every_mark_of_the_plain_text_notation():
   assert deaccentize("а`б´в¨г^д_е°ж!з") == "абвгдежз"
   assert all(deaccentize(f"а{mark}") == "а" for mark in notation_marks)
