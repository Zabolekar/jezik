import pytest
from ..lookup import lookup, data

import pytest

quick = pytest.mark.skipif(
      pytest.config.option.quick,
      reason="data validation only runs without --quick option")

@quick
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

