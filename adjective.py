from typing import Dict, Iterator, Any
from .paradigms import GramInfo
from .utils import insert, garde, prettify, last_vowel_index, first_vowel_index

class Adjective:
   def __init__(self, key: str, value: Dict[str, Any]) -> None:
      self.key = key
      self.value = value
      i, t = self.value['i'], self.value['t']
      self.info = GramInfo(i, t)
      self.trunk = self._trunk()
      
   def _trunk(self):
      accented_adj = garde(self.info.accents.accentize(self.key))
      
      if self.info.MP == 'ov':
         trunk = accented_adj
      elif self.info.MP == 'ski':
         trunk = accented_adj[]
      elif self.info.MP == 'all':
         if 'ə' in self.info.other:
            pass
            trunk = accented_adj[:-2] + accented_adj[-1]
            trunk = trunk.replace('стн', 'сн')
         else:
            pass
            #trunk = accented_adj[:-N-1]
         to_insert = last_vowel_index(trunk) + 1
         return insert(trunk, {to_insert: '·'})