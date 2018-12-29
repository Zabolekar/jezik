from typing import Dict, Tuple, NamedTuple, List, Iterator
from ..paradigm_helpers import AccentedTuple, nice_name

MorphemeChain = List[AccentedTuple] # the name sounds promising, but those "chains" are unlikely to be longer than two morphemes
LabeledEnding = Tuple[str, List[MorphemeChain]]

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

vocative_dict: Dict[str, MorphemeChain] = {'u': [AccentedTuple('у0·', 'b.b:c:c?d:e:q.')],
          'ue': [AccentedTuple('у0·', 'b.b:c:c?d:e:q.'), AccentedTuple('ʺе0·', 'b.b:c:c?d:e:q.')],
          'e': [AccentedTuple('ʺе0·', 'b.b:c:c?d:e:q.')]}

def m_plural(suff:str = '_') -> List[List[MorphemeChain]]:
   ov = AccentedTuple('>œ·в', 'b.b:c?d:e:')
   plurals = [
       [[AccentedTuple('ʹи·', 'b.b:e:q.')]],
       [[AccentedTuple('е·', 'b.b:e:q.')]],
       [[AccentedTuple('<а·\u0304', 'b.b:c:c?d:e:')], [AccentedTuple('<а·\u0304', 'b.b:e:')]],
       [[AccentedTuple('ʹи·ма', 'b.b:c:c?e:q.')], [AccentedTuple('ʹи·ма', 'b.b:e:q.')]],
       [[AccentedTuple('ʹи·ма', 'b.b:c:c?e:q.')], [AccentedTuple('ʹи·ма', 'b.b:e:q.')]],
       [[AccentedTuple('ʹи·ма', 'b.b:c:c?e:q.')], [AccentedTuple('ʹи·ма', 'b.b:e:q.')]],
       [[AccentedTuple('ʹи0·', 'b.b:c:c?e:q.')]]
             ]
   if suff == '+':
      return [[[ov] + a for a in plural] for plural in plurals]
   elif suff == '_':
      return plurals
   elif suff == '±':
      return [[[ov] + a for a in plural] + [a for a in plural] for plural in plurals]
   else:
      raise NotImplementedError("Unknown paradigm")
   


def c_m(suff: str, anim: str, vocative: str) -> NounStem:
   m_singular_ = [
         [[AccentedTuple('ø·', 'b.b:e:q.')]],
   anim_dict['sg_acc'][anim],
   [[AccentedTuple('а·', 'b.b:e:q.')]],
   [[AccentedTuple('у·', 'b.b:e:q.')]],
   [[AccentedTuple('œ·м', 'b.b:e:q.')]],
   anim_dict['sg_loc'][anim],
   [vocative_dict[vocative]],
   ]

   m_plural_ = m_plural(suff)
   declension = m_singular_ + m_plural_
   return NounStem(*declension)
