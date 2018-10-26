from ..lookup import lookup, data

def test_data():
   """
   Iterate over entries in the database.
   Ensure that their lookup doesn't raise an exception.
   """
   for outer_key, yat_mode in data._outer_to_inner._data:
      try:
         lookup(outer_key, input_yat=yat_mode)
      except Exception as e:
         print(outer_key, yat_mode)
         raise

