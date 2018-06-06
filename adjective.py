from typing import Dict, Iterator, Any
from .paradigms import GramInfo, short_adj, long_adj
from .utils import insert, garde, expose, last_vowel_index, first_vowel_index

class Adjective:
   def __init__(self, key: str, value: Dict[str, Any]) -> None:
      self.key = key
      self.value = value
      i, t = self.value['i'], self.value['t']
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
            trunk = accented_adj[:-1]
      elif 'ski' in self.info.other:
         trunk = accented_adj[:-3] if accented_adj.endswith('\u030d') else accented_adj[:-2] # ok
      if not 'a' in self.info.AP:
         to_insert = last_vowel_index(trunk) + 1
         trunk = insert(trunk, {to_insert: '·'})
            
      return trunk
      
   def decline(self) -> Iterator[str]:
      adj_MPs_dict = {'all': [short_adj, long_adj], 'ski': [long_adj]}# think how to add ov
      which_AP = {'short_adj': self.short_AP, 'long_adj': self.long_AP}
      MPs = adj_MPs_dict[self.info.other[0]]
      for paradigm in MPs:
         for ending in paradigm:
            adj_form = self.trunk
            if which_AP[str(paradigm)] in ending.accent:
               if 'a' in which_AP[str(paradigm)]:
                  adj_form = adj_form.replace('\u030d', '') # straight
               current_morph = ending.morpheme.replace('·', '\u030d') # to straight
            else: 
               current_morph = ending.morpheme
            adj_form += current_morph
            if not a in which_AP[str(paradigm)]:
               if '\u030d' not in adj_form: # straight
                  adj_form = adj_form.replace('·', '\u030d', 1) # to straight
            yield self._expose(adj_form)