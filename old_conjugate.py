# old conjugate without accents, currently not used

def conjugate(verb, AP, MP):
   """
   conjugate(raw_word, None, deciphered.MP)
   """
   prs_endings = {'и': [(('и_', ), ('м')), (('и_'), ('ш')), (('и_'), ('')),
                        (('и_'), ('мо')), (('и_'), ('те')), (('е_'), ('')),
                        'й', 'ймо', 'йте'],
                  'е': ['е_м', 'е_ш', 'е_', 'е_мо', 'е_те', 'у_',
                        'й', 'ймо', 'йте'],
                  'а': ['а_м', 'а_ш', 'а_', 'а_мо', 'а_те', 'ају_',
                        'а_ј', 'а_јмо', 'а_јте']
                 }
   inf_endings = ['ти', 'о', 'ла', 'ло', 'ли', 'ле', 'ла',
                  'х', '~', '~', 'смо', 'сте', 'ше']

   MP_dict = {'alpha':
               {'inf': verb[:-2],
                'prs': (verb[:-3], 'и'),
                'pp': (palatalize(verb[:-3], mode='и'), 'е_н')},
              'beta':
               {'inf': verb[:-2],
                'prs': (verb[:-3], 'а'),
                'pp': (verb[:-3], 'а_н')},
              'epsilon':
               {'inf': verb[:-2],
                'prs': (verb[:-5]+'уј', 'е'),
                'pp': (verb[:-3], 'а_н')},
              'delta':
               {'inf': verb[:-2],
                'prs': (palatalize(verb[:-3]), 'е'),
                'pp': (verb[:-3], 'а_н')}
             }

   for ending in inf_endings:
      print(prettify(MP_dict[MP]['inf'] + ending))
   #for ending in prs_endings[MP_dict[MP]['prs'][1]]:
   #   print (prettify(MP_dict[MP]['prs'][0] + ending))

   return None