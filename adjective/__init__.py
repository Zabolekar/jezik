from typing import Any, Dict, List, Iterator, Optional
import re
from ..table import LabeledMultiform
from ..utils import insert, garde, expose, last_vowel_index
from ..paradigm_helpers import GramInfo, nice_name
from .paradigms import AdjParadigm, short_adj, long_adj, mixed_adj

class Adjective:
   def __init__(self, key: str, value: Dict[str, Any]) -> None:
      self.key = key
      self.value = value
      i, t = self.value['i'].split(';'), self.value['t'] # NB i is a list
      self.info = GramInfo(i, t) 
      self.short_AP: List[str] = []
      self.long_AP: List[str] = []
      for AP in self.info.AP:  # TODO: please rewrite and reorder this somehow
         short, long = AP.split(',')
         self.short_AP.append(short)
         self.long_AP.append(long)
      self.trunk = self._trunk()

   def _expose(self, form: str) -> str:
      return expose(form)

   def _trunk(self) -> List[str]:
      result = []

      for number, item in enumerate(self.info.AP):
         accented_adj = garde(self.info.accents[number].accentize(self.key))
         if 'ov' in self.info.other:
            trunk = accented_adj # ok
         elif 'all' in self.info.other:
            if 'ъ\u030d' in accented_adj:
               trunk = accented_adj[:-2] + accented_adj[-1]
            else:
               trunk = accented_adj
         elif 'ski' in self.info.other:
            trunk = re.sub('\u0304\u030d$', '\u0304', accented_adj)[:-2]
         if not 'a' in self.info.AP[number]:
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

   def _adj_form_is_possible(self, adj_form: str) -> bool:
      return re.search('[њљћђшжчџјṕ]œ.ме$', adj_form) is None
      
   def _paradigm_to_forms(self, paradigm: AdjParadigm, i: int, length_inconstant: bool) -> Iterator[LabeledMultiform]:
      """
      Current subparadigm: short or long AP (they behave differently)
      i: index of the variant (by variant we mean things like зу̑бнӣ зу́бнӣ)
      """ 
      if paradigm is short_adj:
         current_AP = self.short_AP[i]
      elif paradigm is long_adj:
         current_AP = self.long_AP[i]
      elif paradigm is mixed_adj:
         current_AP = self.long_AP[i]

      for label, ending in zip(paradigm._fields, paradigm): # TODO: verbs do it completely differently, unify
         adj_forms = []
         
         # at first we process words like boos ~ bosa
         # (this code will be very useful while processing nouns,
         # so it should better be put into Utils):
         
         if length_inconstant and current_AP == self.long_AP[i]:
            trunk_lvi = last_vowel_index(self.trunk[i])
            last_macron = self.trunk[i].rfind('\u0304')
            if trunk_lvi: # if the word has vowels:
               if current_AP.endswith(':') and trunk_lvi+1 != last_macron and trunk_lvi+2 != last_macron:
               # if we need to insert macron, we do it
                  adj_form = insert(self.trunk[i], {trunk_lvi+2: '\u0304'})
               elif current_AP.endswith('.') and trunk_lvi+1 != last_macron and last_macron != -1:
               # and vice versa, we delete macron from the last vowel in case it is there
                  adj_form = self.trunk[i][:last_macron] + self.trunk[i][last_macron+1:] 
               else: # TODO: when does this actually happen? maybe we should raise an error?
                  adj_form = self.trunk[i]
                  print('word got vowels, but length switch not possible!')
         
         # this part is about words where length is the same in most forms:
                  
         else:
            adj_form = self.trunk[i]
            
         # the rest is valid for any adjective:
         
         for variant in ending: # e.g. -om, -ome, -omu
            new_adj_form = adj_form
            
            if current_AP in variant.accent: # if the ending should be accented
               new_adj_form = new_adj_form.replace('\u030d', '') # delete all already put accents from the stem
               if 'a' not in current_AP: # and, further, if the stem has no firmly accented place,
                   # then we delete all the accentable places from the stem.
                   # if we do not do this, we get wrong (double) accents in result!
                   # TODO: when extending this to verbs, do not forget the 'o' paradigm
                  new_adj_form = new_adj_form.replace('·', '')
               # -- and finally we put the accent on the ending:
               current_morpheme = variant.morpheme.replace('·', '\u030d')
               
            else:
               current_morpheme = variant.morpheme.replace('·', '')
            
            # special case: if we are in the short AP
            
            if current_AP == self.short_AP[i]:
               if current_AP.endswith('?') and not 'ø' in current_morpheme:
                  trunk_lvi = last_vowel_index(new_adj_form)
                  last_macron = new_adj_form.rfind('\u0304')
                  new_adj_form = new_adj_form[:last_macron] + new_adj_form[last_macron+1:]
                  # we delete macron on the last vowel from words with inconstant length
                  # TODO: BIG QUESTION: why do we check and do this twice? just for security?
                  
            new_adj_form += current_morpheme # add the ending to the stem

            # finally, if the word is not accented, we put the accent on the stem
            
            if 'a' not in current_AP: # why this? why not always? TODO: test on an 'a'-adj
               if '\u030d' not in adj_form:
                  new_adj_form = new_adj_form.replace('·', '\u030d', 1) 
            if self._adj_form_is_possible(new_adj_form):
               adj_forms.append(new_adj_form)
            
         yield nice_name(label), [self._expose(adjform) for adjform in adj_forms]

   def multiforms(self, *, variant: Optional[int] = None) -> Iterator[LabeledMultiform]:
      """decline"""
      endings = self.info.other[0]
      MPs: List[AdjParadigm]
      if endings == "all":
         MPs = [short_adj, long_adj]
      elif endings == "ski":
         MPs = [long_adj]
      elif endings == "ov":
         MPs = [mixed_adj]

      for i, AP in enumerate(self.info.accents):
         # variant = None means all variants
         if variant is not None and variant != i:
            continue
         length_inconstancy = False
         if endings == "all" and self.short_AP[i][-1] != self.long_AP[i][-1]:
            length_inconstancy = True
         for paradigm in MPs:
            yield from self._paradigm_to_forms(paradigm, i, length_inconstancy)
