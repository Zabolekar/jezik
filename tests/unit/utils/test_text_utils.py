from ....lookup.utils.charutils import notation_marks
from ....lookup.utils.text_utils import insert, deaccentize

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


def test_deaccentize_removes_every_mark_of_the_plain_text_notation():
   assert deaccentize("а`б´в¨г^д_е°ж!з") == "абвгдежз"
   assert all(deaccentize(f"а{mark}") == "а" for mark in notation_marks)
