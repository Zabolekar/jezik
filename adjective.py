from typing import Any, Dict, List
from .table import Table
from .paradigms import GramInfo, AdjParadigm, short_adj, long_adj
from .utils import insert, garde, expose, last_vowel_index

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

   def _paradigm_table(self, paradigm: AdjParadigm) -> Table:
      # current subparadigm: short or long AP (they behave differently)
      if paradigm is short_adj:
         current_AP = self.short_AP
      elif paradigm is long_adj:
         current_AP = self.long_AP

      for label, ending in zip(paradigm._fields, paradigm):
         adj_forms = []
         for variant in ending:
            adj_form = self.trunk
            if current_AP in variant.accent: # please add loop, so it would be "ending[i].accent" or so, since adj ending is actually a list of endings
               if 'a' in current_AP:
                  adj_form = adj_form.replace('\u030d', '') # straight
               current_morpheme = variant.morpheme.replace('·', '\u030d') # to straight
            else:
               current_morpheme = variant.morpheme
            adj_form += current_morpheme
            if not 'a' in current_AP:
               if '\u030d' not in adj_form: # straight
                  adj_form = adj_form.replace('·', '\u030d', 1) # to straight
            adj_forms.append(adj_form)
         yield label, (self._expose(adj_form) for adj_form in adj_forms)

   def decline(self) -> Table:
      endings = self.info.other[0]
      MPs: List[AdjParadigm]
      if endings == "all":
         MPs = [short_adj, long_adj]
      elif endings == "ski":
         MPs = [long_adj]
      # else: TODO think how to add ov
      for paradigm in MPs:
         yield from self._paradigm_table(paradigm)
      # TODO: this ONLY works because "Table" is currently an Iterator
      # you CAN'T just expect to yield from two tables and obtain another table
      # pay special attention to this part when rewriting Table
