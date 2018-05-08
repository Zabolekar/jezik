from typing import Dict, Iterator, Any
from .paradigms import GramInfo, MP_to_stems
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
      N = len(infinitive_dict[self.info.MP])
      if self.info.AP == 'a':
         pass
         #return accented_adj[:-N]
      else:
         if self.info.MP = 'all' and 'ə' in self.info.other:
            pass
            #trunk = accented_adj[:-N]
         else:
            pass
            #trunk = accented_adj[:-N-1]
         to_insert = last_vowel_index(trunk) + 1
         return insert(trunk, {to_insert: '·'})