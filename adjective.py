from typing import Any, Dict, List, Iterator
import re
from .table import Table
from .paradigms import GramInfo, AdjParadigm, short_adj, long_adj, mixed_adj
from .utils import insert, garde, expose, last_vowel_index

class Adjective:
   def __init__(self, key: str, value: Dict[str, Any]) -> None:
      self.key = key
      self.value = value
      i, t = self.value['i'].split(';'), self.value['t'] # NB i is a list
      self.info = GramInfo(i, t)
      self.short_AP: List[str] = []
      self.long_AP: List[str] = []
      for AP in self.info.AP:  # please rewrite and reorder this somehow
         bothAPs = AP.split(',')
         self.short_AP.append(bothAPs[0])
         self.long_AP.append(bothAPs[1])
      self.trunk = self._trunk()

   def _expose(self, form: str) -> str:
      return expose(form)

   def _trunk(self) -> List[str]:
      result = []
      for nmr, item in enumerate(self.info.AP):
         accented_adj = garde(self.info.accents[nmr].accentize(self.key))
         if 'ov' in self.info.other:
            trunk = accented_adj # ok
         elif 'all' in self.info.other:
            if 'ъ\u030d' in accented_adj:
               trunk = accented_adj[:-2] + accented_adj[-1]
            else:
               trunk = accented_adj
         elif 'ski' in self.info.other:
            trunk = re.sub('\u0304\u030d$', '\u0304', accented_adj)[:-2]
         if not 'a' in self.info.AP[nmr]:
            lvi = last_vowel_index(trunk)
            if lvi is None:
               #raise ValueError(f"{trunk} does not contain any vowels")
               pass
            else:
               if lvi > -1:
                  to_insert = lvi + 1
                  trunk = insert(trunk, {to_insert: '·'})
         result.append(trunk)
      return result

   def _paradigm_table(self, paradigm: AdjParadigm, nmbr: int, length_inconstancy: bool) -> Table:
      # current subparadigm: short or long AP (they behave differently)
      if paradigm is short_adj:
         current_AP = self.short_AP[nmbr]
      elif paradigm is long_adj:
         current_AP = self.long_AP[nmbr]
      elif paradigm is mixed_adj:
         current_AP = self.long_AP[nmbr]

      for label, ending in zip(paradigm._fields, paradigm):
         adj_forms = []
         if length_inconstancy and current_AP == self.long_AP[nmbr]:
            trunk_lvi = last_vowel_index(self.trunk[nmbr])
            last_macron = self.trunk[nmbr].rfind('\u0304')
            if trunk_lvi:
               if current_AP.endswith(':') and self.trunk[nmbr][trunk_lvi+1] == '·' and trunk_lvi+2 != last_macron:
                  adj_form = insert(self.trunk[nmbr], {trunk_lvi+2: '\u0304'})
               elif current_AP.endswith('.') and trunk_lvi+1 != last_macron and last_macron != -1:
                  adj_form = self.trunk[nmbr][:last_macron] + self.trunk[nmbr][last_macron+1:] # delete last macron
               else: 
                  adj_form = self.trunk[nmbr]
         else:
            adj_form = self.trunk[nmbr]
         for variant in ending:
            new_adj_form = adj_form
            if current_AP in variant.accent: # please add loop, so it would be "ending[i].accent" or so, since adj ending is actually a list of endings
               print(current_AP)
               new_adj_form = new_adj_form.replace('\u030d', '') # straight
               if 'a' not in current_AP:
                  new_adj_form = new_adj_form.replace('·', '')
               current_morpheme = variant.morpheme.replace('·', '\u030d') # to straight
            else:
               current_morpheme = variant.morpheme.replace('·', '')
            new_adj_form += current_morpheme
            if not 'a' in current_AP:
               if '\u030d' not in adj_form: # straight
                  new_adj_form = new_adj_form.replace('·', '\u030d', 1) # to straight
                  
            adj_forms.append(new_adj_form)
            print(adj_forms)
         yield label, (self._expose(adjform) for adjform in adj_forms)

   def decline(self) -> Table:
      endings = self.info.other[0]
      MPs: List[AdjParadigm]
      if endings == "all":
         MPs = [short_adj, long_adj]
      elif endings == "ski":
         MPs = [long_adj]
      elif endings == "ov":
         MPs = [mixed_adj]
      
      for nmbr, AP in enumerate(self.info.accents):
         length_inconstancy = False
         if endings == "all" and self.short_AP[nmbr][-1] != self.long_AP[nmbr][-1]:
            length_inconstancy = True
         for paradigm in MPs:
            yield from self._paradigm_table(paradigm, nmbr, length_inconstancy)
         # TODO: this ONLY works because "Table" is currently an Iterator
         # you CAN'T just expect to yield from two tables and obtain another table
         # pay special attention to this part when rewriting Table
