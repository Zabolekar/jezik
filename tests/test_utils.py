from ..lookup.utils import ungarde, garde, deyerify, insert, prettify

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

def test_prettify():
   assert [prettify(word, "je") for word in [
       "цꙓ̄лѣ\u030dти", "бѣлѣ\u030dжӣм", "ви\u030dдѣʌ"]] == [
   "цйје̄ље\u030dти", "биље\u030dжӣм", "ви\u030dдио"]
   assert [prettify(word, "e") for word in [
       "цꙓ̄лѣ\u030dти", "бѣлѣ\u030dжӣм", "ви\u030dдѣʌ"]] == [
   "це̄ле\u030dти", "беле\u030dжӣм", "ви\u030dдео"]
