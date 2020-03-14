from typing import List
import pytest # type: ignore
from ..lookup import lookup, data
from ..lookup.charutils import four_accents, cmacron
from ..lookup.paradigm_helpers import cut_AP
from ..lookup.table import LabeledMultiform

def str_find(word: str, substr: str) -> int:
   found = word.find(substr)
   if found == -1:
      return len(word)
   return found

first_form = {
   "adjective": "m sg nom", # short or long, we take the 0st one
   "noun": "sg nom",
   "verb": "infinitive",
   "adverb": ""
}


@pytest.mark.slow
def test_no_exceptions():
   """
   Iterate over entries in the database.
   Ensure that their lookup doesn't raise an exception.
   """
   bad_multiforms : List[LabeledMultiform] = []
   for outer_key, yat_mode in data._outer_to_inner:
      try:
         multitable = lookup(outer_key, input_yat=yat_mode)
         if any(not table.pos for table in multitable):
            raise ValueError("invalid part of speech")
      except Exception:
         print(outer_key, yat_mode)
         raise
      else:
         for table in multitable._tables:
            main_form = list(table[first_form[table.pos]])[0][1][0]
            first_acc_main = min(str_find(main_form, x) for x in four_accents)
            last_acc_main = max(main_form.rfind(x) for x in four_accents)
            compound = last_acc_main == first_acc_main > str_find(main_form, cmacron)
            for labeled_multiform in table:
               for form in labeled_multiform[1]:
                  if any(form.startswith(x) for x in four_accents + cmacron):
                     bad_multiforms.append(labeled_multiform)
                  if not compound: # eg not plāvosȋv
                     first_acc = min(str_find(form, x) for x in four_accents)
                     last_acc = max(form.rfind(x) for x in four_accents)
                     if last_acc == first_acc > str_find(form, cmacron): # eg ōvánā
                        bad_multiforms.append(labeled_multiform)
   if bad_multiforms:
      print(bad_multiforms)
      raise ValueError("impossible accentuation")


def test_paradigms():
   """Ensure that accent paradigms are desribed well"""
   for outer_key, _ in data._outer_to_inner:
      for inner_key, word in data[outer_key, 'e']:
         paradigms = [cut_AP(x) for x in word.info.split(";")]
         for paradigm in paradigms:
            assert isinstance(paradigm, str), paradigm + " " + inner_key
            if len(paradigm) in (2, 3):
               assert paradigm[0].isalpha() and paradigm[1] in (".:!ʹʺ’¿?0"), paradigm+" "+inner_key
            elif len(paradigm) == 1:
               assert paradigm == '0', paradigm + " " + inner_key
            elif len(paradigm) > 0:
               raise ValueError("bad paradigm len: " + paradigm + " " + inner_key)
