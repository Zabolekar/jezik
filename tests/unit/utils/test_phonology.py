from ....lookup.utils import characters as c
from ....lookup.utils.phonology import deyerify, assimilate

def test_deyerify():
   assert [deyerify(i) for i in [
   "небъце", "тежъко", "кљунорожъци", "властъни"]] == [
   "непце", "тешко", "кљунорошци", "власни"]


def test_assimilate():
   assert [assimilate(word, "je") for word in [
       "цꙓ̄лѣ\u030dти", "бѣлѣ\u030dжӣм", "ви\u030dдѣʌ"]] == [
   "цйје̄ље\u030dти", "биље\u030dжӣм", "ви\u030dдио"]
   assert [assimilate(word, "e") for word in [
       "цꙓ̄лѣ\u030dти", "бѣлѣ\u030dжӣм", "ви\u030dдѣʌ"]] == [
   "це̄ле\u030dти", "беле\u030dжӣм", "ви\u030dдео"]


def test_deyerify_lengthens_vowel_before_sonorant_and_lost_yer():
   assert deyerify(f"ва{c.straight}рък") == f"ва{c.straight}{c.macron}рк"


def test_deyerify_moves_accent_stranded_on_a_consonant_to_the_vowel():
   assert deyerify(f"авио{c.macron}н{c.straight}") == f"авио{c.straight}{c.macron}н"
