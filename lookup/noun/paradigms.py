from typing import Dict, NamedTuple, List, Iterator
from ..paradigm_helpers import (
   AccentedTuple, nice_name, MorphemeChain, LabeledEnding
)
from ..charutils import c
from ..utils import last_vowel_index

class NounStem(NamedTuple):
   sg_nom: List[MorphemeChain]
   sg_acc: List[MorphemeChain]
   sg_gen: List[MorphemeChain]
   sg_dat: List[MorphemeChain]
   sg_ins: List[MorphemeChain]
   sg_loc: List[MorphemeChain]
   sg_voc: List[MorphemeChain]
   pl_nom: List[MorphemeChain]
   pl_acc: List[MorphemeChain]
   pl_gen: List[MorphemeChain]
   pl_dat: List[MorphemeChain]
   pl_ins: List[MorphemeChain]
   pl_loc: List[MorphemeChain]
   pl_voc: List[MorphemeChain]

   @property
   def labeled_endings(self) -> Iterator[LabeledEnding]:
      yield from zip(map(nice_name, self._fields), iter(self))

m_anim_dict: Dict[str, Dict[str, List[MorphemeChain]]] = {
   'sg_acc': {
      'in': [[AccentedTuple('ø·', 'b.b:b?e:f.q.')]],
      'an': [[AccentedTuple('а·', 'b.b:b?e:f.q.')]]
   },
   'sg_loc': {
      'an': [[AccentedTuple('у·', 'b.b:b?e:f.q.')]],
      'in': [[AccentedTuple('у·', 'b.b:b?c:c?d:e:f.q.')], [AccentedTuple('у·', 'b.b:b?e:f.q.')]]
   }
}

male_gen_pl_marked = [
   [AccentedTuple(f'<а·{c.macron}', 'b.b:b?')],
   [AccentedTuple(f'<а·{c.macron}', 'b.b:b?e:')]
]

female_gen_pl_i = [AccentedTuple(f'и·{c.macron}', 'b.b:c.c:g.g:')]

def m_plural(suff:str = '_') -> List[List[MorphemeChain]]:
   ov = AccentedTuple('>œ·в', 'b.b:b?c?d:e:f.')

   suffixed_plurals = [
       [[AccentedTuple('ʹи·', '')]],
       [[AccentedTuple('е·', '')]],
       [[AccentedTuple(f'<а·{c.macron}', 'b.b:b?c:c?b0d:')], male_gen_pl_marked[0]],
       [[AccentedTuple('ʹи·ма', 'c:c?b0')], [AccentedTuple('ʹи·ма', '')]],
       [[AccentedTuple('ʹи·ма', 'c:c?b0')], [AccentedTuple('ʹи·ма', '')]],
       [[AccentedTuple('ʹи·ма', 'c:c?b0')], [AccentedTuple('ʹи·ма', '')]],
       [[AccentedTuple('ʹи0·', 'b.b:b?c:c?b0q.')]]
   ]

   free_plurals = [
       [[AccentedTuple('ʹи·', 'b.b:b?e:q.')]],
       [[AccentedTuple('е·', 'b.b:b?e:q.')]],
       [[AccentedTuple(f'<а·{c.macron}', 'b.b:b?c:c?b0d:e:')], male_gen_pl_marked[1]],
       [[AccentedTuple('ʹи·ма', 'b.b:b?c:c?b0e:q.')], [AccentedTuple('ʹи·ма', 'b.b:b?e:q.')]],
       [[AccentedTuple('ʹи·ма', 'b.b:b?c:c?b0e:q.')], [AccentedTuple('ʹи·ма', 'b.b:b?e:q.')]],
       [[AccentedTuple('ʹи·ма', 'b.b:b?c:c?b0e:q.')], [AccentedTuple('ʹи·ма', 'b.b:b?e:q.')]],
       [[AccentedTuple('ʹи0·', 'b.b:b?c:c?b0q.')]]
   ]
   if suff == '+':
      return [[[ov] + a for a in plural] for plural in suffixed_plurals]
   elif suff == '_':
      return free_plurals
   elif suff == '±':
      return [
         [[ov] + a for a in suffixed_plurals[i]] + free_plurals[i]
         for i in range(7)
      ]
   else:
      raise NotImplementedError("Unknown paradigm")


def m_instr(stem: str) -> List[List[AccentedTuple]]:
   lvi = last_vowel_index(stem)

   em = [AccentedTuple('е·м', 'b.b:b?e:f.q.')]
   om = [AccentedTuple('о·м', 'b.b:b?e:f.q.')]

   if lvi is None:
      result = [om]
   elif stem.endswith('ʲ') or stem.endswith('тељ') and not stem.endswith('ирʲ'): # пријатељ, сир
      result = [em, om] # плашт, дажд, пут, нос, курс, појас, цар
   elif stem.endswith('ъц'): # отац, палац
      result = [em]
   elif stem[-1] in 'чџшжјљњ':
      if stem[lvi] == 'е':
         result = [om, em] # лавеж, кеј, Беч
      else:
         result = [em] # кључ
   elif stem[-1] in 'њљћђ': # коњ
      result = [em]
   else:
      result = [om]
   return result

def m_voc(stem: str, anim: str) -> List[List[AccentedTuple]]:
   u = [AccentedTuple('у0·', 'b.b:b?c:c?b0d:e:f.q.')]
   e = [AccentedTuple('ʺе0·', 'b.b:b?c:c?b0d:e:f.q.')]

   if stem.endswith('рʲ'): # цар
      return [u, e]
   if stem[-1] in 'јљњђћчшжџ': # гај
      return [u]
   elif (
      stem.endswith('ък') and
      stem[-3] in 'тдчсшзж'
   ): # редак
      return [u]
   elif stem.endswith(f'е·{c.macron}з'): # Кинез
      return [u]
   elif (
      stem[-1] in 'кгх' and 
      stem[-2] != 'ъ' and
      anim == 'in'
   ): # ковчег, лек, смех, прах
      return [u, e]
   else:
      return [e]

def stem_male(stem: str, suff: str, anim: str) -> NounStem:
   m_singular_ = [
         [[AccentedTuple('ø·', 'b.b:b?e:f.q.')]],
   m_anim_dict['sg_acc'][anim],
   [[AccentedTuple('а·', 'b.b:b?e:f.q.')]],
   [[AccentedTuple('у·', 'b.b:b?e:f.q.')]],
   m_instr(stem),
   m_anim_dict['sg_loc'][anim],
   m_voc(stem, anim)
   ]

   m_plural_ = m_plural(suff)
   declension = m_singular_ + m_plural_
   return NounStem(*declension)


f_declension_a = [
   [[AccentedTuple('а·', 'b.b:c.c:g.g:')]],
   [[AccentedTuple('у·', 'b.b:g.g:')]],
   [[AccentedTuple(f'е·{c.macron}', 'b.b:c.c:g.g:')]],
   [[AccentedTuple('ʹи·', 'b.b:g.g:')]],
   [[AccentedTuple(f'о·{c.macron}м', 'b.b:c.c:g.g:')]],
   [[AccentedTuple('ʹи·', 'b.b:c.c:g.g:')]],
   [[AccentedTuple('о0·', 'b.b:')]], # TODO: add o/u/e-rule
   [[AccentedTuple('е·', 'b.b:')]],
   [[AccentedTuple('e·', 'b.b:')]],
   [[AccentedTuple(f'<а·{c.macron}', 'b.b:c.c:g.g:')]],
   [[AccentedTuple('а·ма', 'b.b:c.c:g.g:')], [AccentedTuple('>>а·ма', 'b.b:c.c:g.g:')]],
   [[AccentedTuple('а·ма', 'b.b:c.c:g.g:')], [AccentedTuple('>>а·ма', 'b.b:c.c:g.g:')]],
   [[AccentedTuple('а·ма', 'b.b:c.c:g.g:')], [AccentedTuple('>>а·ма', 'b.b:c.c:g.g:')]],
   [[AccentedTuple('е0·', 'b.b:')]]
]

f_declension_yer = [
   [[AccentedTuple('ø', '')]],
   [[AccentedTuple('ø', '')]],
   [[AccentedTuple('и', '')]],
   [[AccentedTuple('и', '')]],
   [[AccentedTuple('ĵу', '')], [AccentedTuple('и', '')]],
   [[AccentedTuple('и·', 'c:c?')]],
   [[AccentedTuple('и', '')]],
   [[AccentedTuple('и', '')]],
   [[AccentedTuple('и', '')]],
   [[AccentedTuple(f'и·{c.macron}', 'c:c?')]],
   [[AccentedTuple('и·ма', 'c:c?')]],
   [[AccentedTuple('и·ма', 'c:c?')]],
   [[AccentedTuple('и·ма', 'c:c?')]],
   [[AccentedTuple('и', '')]]
]

def stem_female(a:bool) -> NounStem:
   if a:
      return NounStem(*f_declension_a)
   else:
      return NounStem(*f_declension_yer)

def stem_neutral() -> NounStem:
   # TODO: it is 'selo' only, add 'ime'
   return NounStem(
      [[AccentedTuple('¦œ·', 'b.b:b0g.')]],
      [[AccentedTuple('¦œ·', 'b.b:b0g.')]],
      [[AccentedTuple('а·', 'b.b:b0g.')]],
      [[AccentedTuple('у·', 'b.b:b0g.')]],
      [[AccentedTuple('¦œ·м', 'b.b:b0g.')]],
      [[AccentedTuple('у·', 'b.b:b0g.')]],
      [[AccentedTuple('¦œ·', 'b.b:b0g.')]],
      [[AccentedTuple('а·', 'b.c.c:')]],
      [[AccentedTuple('а·', 'b.c.c:')]],
      [[AccentedTuple(f'<а·{c.macron}', 'b.b:b0c.c:g.')]],
      [[AccentedTuple('ʹи·ма', 'b.b:b0c.c:')]],
      [[AccentedTuple('ʹи·ма', 'b.b:b0c.c:')]],
      [[AccentedTuple('ʹи·ма', 'b.b:b0c.c:')]],
      [[AccentedTuple('а·', 'b.c.c:')]]
   )