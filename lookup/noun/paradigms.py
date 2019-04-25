from typing import Dict, NamedTuple, List, Iterator
from ..paradigm_helpers import (AccentedTuple, nice_name,
                                MorphemeChain, LabeledEnding)
from ..charutils import cmacron
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
      yield from zip(map(nice_name, self._fields),
                     super().__iter__())

anim_dict: Dict[str, Dict[str, List[MorphemeChain]]] = {'sg_acc': {'in': [[AccentedTuple('ø·', 'b.b:e:q.')]],
                       'an': [[AccentedTuple('а·', 'b.b:e:q.')]]},
            'sg_loc': {'an': [[AccentedTuple('у·', 'b.b:e:q.')]],
                       'in': [[AccentedTuple('у·', 'b.b:c:c?d:e:q.')], [AccentedTuple('у·', 'b.b:e:q.')]]}
            }


def m_plural(suff:str = '_') -> List[List[MorphemeChain]]:
   ov = AccentedTuple('>œ·в', 'b.b:c?d:e:')

   suffixed_plurals = [
       [[AccentedTuple('ʹи·', '')]],
       [[AccentedTuple('е·', '')]],
       [[AccentedTuple(f'<а·{cmacron}', 'b.b:c:c?b0d:')], [AccentedTuple(f'<а·{cmacron}', 'b.b:')]],
       [[AccentedTuple('ʹи·ма', 'c:c?b0')], [AccentedTuple('ʹи·ма', '')]],
       [[AccentedTuple('ʹи·ма', 'c:c?b0')], [AccentedTuple('ʹи·ма', '')]],
       [[AccentedTuple('ʹи·ма', 'c:c?b0')], [AccentedTuple('ʹи·ма', '')]],
       [[AccentedTuple('ʹи0·', 'b.b:c:c?b0q.')]]
            ]

   free_plurals = [
       [[AccentedTuple('ʹи·', 'b.b:e:q.')]],
       [[AccentedTuple('е·', 'b.b:e:q.')]],
       [[AccentedTuple(f'<а·{cmacron}', 'b.b:c:c?b0d:e:')], [AccentedTuple(f'<а·{cmacron}', 'b.b:e:')]],
       [[AccentedTuple('ʹи·ма', 'b.b:c:c?b0e:q.')], [AccentedTuple('ʹи·ма', 'b.b:e:q.')]],
       [[AccentedTuple('ʹи·ма', 'b.b:c:c?b0e:q.')], [AccentedTuple('ʹи·ма', 'b.b:e:q.')]],
       [[AccentedTuple('ʹи·ма', 'b.b:c:c?b0e:q.')], [AccentedTuple('ʹи·ма', 'b.b:e:q.')]],
       [[AccentedTuple('ʹи0·', 'b.b:c:c?b0q.')]]
             ]
   if suff == '+':
      return [[[ov] + a for a in plural] for plural in suffixed_plurals]
   elif suff == '_':
      return free_plurals
   elif suff == '±':
      return [[[ov] + a for a in suffixed_plurals[i]] + [a for a in free_plurals[i]] for i in range(7)]
   else:
      raise NotImplementedError("Unknown paradigm")
   

def m_instr(stem: str) -> List[List[AccentedTuple]]:
   lvi = last_vowel_index(stem)
   em = [AccentedTuple('е·м', 'b.b:e:q.')]
   om = [AccentedTuple('о·м', 'b.b:e:q.')]

   if stem.endswith('ʲ') \
      or stem.endswith('тељ'): # пријатељ
      return [em, om] # плашт, дажд, пут, нос, курс, појас, цар 
   elif stem.endswith('ъц'): # отац, палац
      return [em]
   elif stem[-1] in 'чџшжј':
      if stem[lvi] == 'е':
         return [om, em] # лавеж, кеј, Беч
      else:
         return [em] # кључ
   elif stem[-1] in 'њљћђ': # коњ
      return [em]
   else:
      return [om]

def m_voc(stem: str, anim: str) -> List[List[AccentedTuple]]:
   u = [AccentedTuple('у0·', 'b.b:c:c?b0d:e:q.')]
   e = [AccentedTuple('ʺе0·', 'b.b:c:c?b0d:e:q.')]

   if stem.endswith('рʲ'): # цар
      return [u, e]
   if stem[-1] in 'јљњђћчшжџ': # гај
      return [u]
   elif stem.endswith('ък') \
      and stem[-3] in 'тдчсшзж': # редак
      return [u]
   elif stem.endswith(f'е·{cmacron}з'): # Кинез
      return [u]
   elif stem[-1] in 'кгх' \
       and stem[-2] != 'ъ' \
       and anim == 'in': # ковчег, лек, смех, прах
      return [u, e]
   else:
      return [e]


def c_m(stem: str, suff: str, anim: str) -> NounStem:
   m_singular_ = [
         [[AccentedTuple('ø·', 'b.b:e:q.')]],
   anim_dict['sg_acc'][anim],
   [[AccentedTuple('а·', 'b.b:e:q.')]],
   [[AccentedTuple('у·', 'b.b:e:q.')]],
   m_instr(stem),
   anim_dict['sg_loc'][anim],
   m_voc(stem, anim)
   ]

   m_plural_ = m_plural(suff)
   declension = m_singular_ + m_plural_
   return NounStem(*declension)
