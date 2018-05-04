from lookup import random_lookup

if __name__ == '__main__':
   for table in random_lookup():
      print("-"*20)
      for form in table:
         print(form)
      print("-"*20)
