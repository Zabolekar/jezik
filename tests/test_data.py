from typing import List
import pytest # type: ignore
from ..lookup import lookup, data
from ..lookup.charutils import four_accents, cmacron
from ..lookup.table import LabeledMultiform

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
            for labeled_multiform in table:
               for form in labeled_multiform[1]:
                  if any(form.startswith(x) for x in four_accents + cmacron):
                     bad_multiforms.append(labeled_multiform)
   if bad_multiforms:
      print(bad_multiforms)
      raise ValueError("impossible accentuation")

def test_paradigms():
   """Ensure that accent paradigms are desribed well"""
   for outer_key, _ in data._outer_to_inner:
      for inner_key, word in data[outer_key, 'e']:
         paradigms = [x.split("\\")[1] for x in word.info.split(";")]
         for paradigm in paradigms:
            assert isinstance(paradigm, str), paradigm + " " + inner_key
            if len(paradigm) == 2:
               assert paradigm[0].isalpha() and paradigm[1] in (".:!ʹʺ’?0"), paradigm + " " + inner_key
            elif len(paradigm) in [4, 5]:
               assert paradigm[-3] == ",", paradigm + " " + inner_key
            elif len(paradigm) == 1:
               assert paradigm == '0', paradigm + " " + inner_key
            elif len(paradigm):
               raise ValueError("bad paradigm len: " + paradigm + " " + inner_key)
