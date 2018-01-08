from lookup import random_word

if __name__ == '__main__':
   for table in random_word():
      print("-"*20)
      for form in table:
         print(form)
      print("-"*20)