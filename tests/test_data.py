import pytest # type: ignore
from ..lookup import lookup, data


@pytest.mark.slow
def test_data():
   """
   Iterate over entries in the database.
   Ensure that their lookup doesn't raise an exception.
   """
   for outer_key, yat_mode in data._outer_to_inner._data:
      try:
         multitable = lookup(outer_key, input_yat=yat_mode)
         if any(not table.pos for table in multitable):
            raise ValueError("invalid part of speech")
      except Exception as e:
         print(outer_key, yat_mode)
         raise

def test_rings():
   """ Ensure that rings are placed below r's. """
   for outer_key, yat_mode in data._outer_to_inner._data:
      for inner_key, wrd in data[outer_key, 'ekav']:
         if '@' in wrd.info:
            accent_info = wrd.info.split('\\')[1]
            r_info = int(accent_info.split('@')[0])
            if inner_key[r_info-1] not in ['р', 'Р']:
               raise ValueError(inner_key + ': ' + str(r_info))


         