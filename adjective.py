from typing import Dict, Iterator, Any
from .table import Table
from .paradigms import GramInfo, short_adj, long_adj
from .utils import insert, garde, expose, last_vowel_index, first_vowel_index

class Adjective:
   def __init__(self, key: str, value: Dict[str, Any]) -> None:
      self.key = key
      self.value = value
      i, t = self.value['i'].split(';')[0], self.value['t'] # add loop for multiple i's; for now only the first one is shown
      self.info = GramInfo(i, t)
      self.short_AP, self.long_AP = self.info.AP.split(',')
      self.trunk = self._trunk()

   def _expose(self, form: str) -> str:
      return expose(form)

   def _trunk(self) -> str:
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
         lvi = last_vowel_index(trunk)
         if lvi is None:
            #raise ValueError(f"{trunk} does not contain any vowels")
            pass
         else:
            if lvi > -1:
               to_insert = lvi + 1
               trunk = insert(trunk, {to_insert: '·'})
      return trunk

   def decline(self) -> Table:
      adj_MPs_dict = {'all': [short_adj, long_adj], 'ski': [long_adj]} # TODO think how to add ov
      which_AP = {'ShortAdj': self.short_AP, 'LongAdj': self.long_AP}
      MPs = adj_MPs_dict[self.info.other[0]]
      for paradigm in MPs: # type: ignore
         for label, ending in zip(paradigm._fields, paradigm):
            adj_forms = []
            current_AP = which_AP[type(paradigm).__name__] # current subparadigm: short or long AP (they behave differently)
            for variant in ending:
               adj_form = self.trunk
               if current_AP in variant.accent: # please add loop, so it would be "ending[i].accent" or so, since adj ending is actually a list of endings
                  if 'a' in current_AP:
                     adj_form = adj_form.replace('\u030d', '') # straight
                  current_morph = variant.morpheme.replace('·', '\u030d') # to straight
               else: 
                  current_morph = variant.morpheme
               adj_form += current_morph
               if not 'a' in current_AP:
                  if '\u030d' not in adj_form: # straight
                     adj_form = adj_form.replace('·', '\u030d', 1) # to straight
               adj_forms.append(adj_form)
            yield label, (self._expose(adjform) for adjform in adj_forms)
