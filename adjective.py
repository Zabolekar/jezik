from typing import Dict, Iterator, Any
from .paradigms import GramInfo, short_adj, long_adj
from .utils import insert, garde, expose, last_vowel_index, first_vowel_index

class Adjective:
   def __init__(self, key: str, value: Dict[str, Any]) -> None:
      self.key = key
      self.value = value
      i, t = self.value['i'].split(';')[0], self.value['t'] # add loop for multiple i's; for now only the first one is shown
      self.info = GramInfo(i, t)
      print('self.info', str(self.info))
      print('self.info.AP: ', self.info.AP)
      self.short_AP, self.long_AP = self.info.AP.split(',')
      self.trunk = self._trunk()
    
   def _expose(self, form: str) -> str:
      return expose(form)
    
   def _trunk(self):
      accented_adj = garde(self.info.accents.accentize(self.key))
      # 
      if 'ov' in self.info.other:
         trunk = accented_adj # ok   
      elif 'all' in self.info.other:
         if 'ъ\u030d' in accented_adj:
            trunk = accented_adj[:-2] + accented_adj[-1]
         else:
            trunk = accented_adj
      elif 'ski' in self.info.other:
         trunk = accented_adj[:-3] if accented_adj.endswith('\u030d') else accented_adj[:-2] # ok
      if not 'a' in self.info.AP:
         to_insert = last_vowel_index(trunk) + 1
         trunk = insert(trunk, {to_insert: '·'})
            
      return trunk
      
   def decline(self) -> Iterator[str]:
      adj_MPs_dict = {'all': [short_adj, long_adj], 'ski': [long_adj]}# think how to add ov
      which_AP = {'ShortAdj': self.short_AP, 'LongAdj': self.long_AP}
      MPs = adj_MPs_dict[self.info.other[0]]
      for paradigm in MPs:
         for ending in paradigm:
            adj_form = self.trunk
            current_AP = which_AP[type(paradigm).__name__] # current subparadigm: short or long AP (they behave differently)
            if current_AP in ending[0].accent: # please add loop, so it would be "ending[i].accent" or so, since adj ending is actually a list of endings
               if 'a' in current_AP:
                  adj_form = adj_form.replace('\u030d', '') # straight
               current_morph = ending[0].morpheme.replace('·', '\u030d') # to straight
            else: 
               current_morph = ending[0].morpheme
            adj_form += current_morph
            if not 'a' in current_AP:
               if '\u030d' not in adj_form: # straight
                  adj_form = adj_form.replace('·', '\u030d', 1) # to straight
            yield self._expose(adj_form)