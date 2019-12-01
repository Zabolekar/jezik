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
   if len(bad_multiforms):
      print(bad_multiforms)
      raise ValueError("impossible accentuation")

def test_rings():
   """ Ensure that rings are placed below r's. """
   for outer_key, _ in data._outer_to_inner:
      for inner_key, word in data[outer_key, 'e']:
         if '@' in word.info:
            accent_info = word.info.split('\\')[1]
            r_info = accent_info.split('@')[0]
            # mostly there is only one index, but there are words like српскохрватски:
            r_indices = [int(s) for s in r_info.split(",")]
            for i in r_indices:
               if inner_key[i-1] not in ['р', 'Р']:
                  raise ValueError("Bad R: " + inner_key + ': ' + str(r_info))

@pytest.mark.xfail
def test_paradigms():
   """Ensure that accent paradigms are desribed well"""
   for outer_key, _ in data._outer_to_inner:
      for inner_key, word in data[outer_key, 'e']:
         paradigms = [x.split("\\")[2] for x in word.info.split(";")]
         for paradigm in paradigms:
            assert type(paradigm) is str, paradigm
            if len(paradigm) == 2:
               assert paradigm[0].isalpha() and not paradigm[1].isalpha(), paradigm
            elif len(paradigm) in [4, 5]:
               # TODO: find out why it has . instead of ,
               assert paradigm[-3] == ",", paradigm
            else:
               raise ValueError("bad paradigm len: " + paradigm)
