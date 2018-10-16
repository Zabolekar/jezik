from typing import Tuple, NamedTuple, List, Union, Iterator
from ..paradigm_helpers import AccentedTuple, nice_name

LabeledEnding = Tuple[str, List[List[AccentedTuple]]]

class NounStem(NamedTuple):
   sg_nom: List[List[AccentedTuple]]
   sg_acc: List[List[AccentedTuple]]
   sg_gen: List[List[AccentedTuple]]
   sg_dat: List[List[AccentedTuple]]
   sg_ins: List[List[AccentedTuple]]
   sg_loc: List[List[AccentedTuple]]
   sg_voc: List[List[AccentedTuple]]
   pl_nom: List[List[AccentedTuple]]
   pl_acc: List[List[AccentedTuple]]
   pl_gen: List[List[AccentedTuple]]
   pl_dat: List[List[AccentedTuple]]
   pl_ins: List[List[AccentedTuple]]
   pl_loc: List[List[AccentedTuple]]
   pl_voc: List[List[AccentedTuple]]

   @property
   def labeled_endings(self) -> Iterator[LabeledEnding]:
      yield from zip(map(nice_name, self._fields),
                     super().__iter__())

anim_dict = {'sg_acc': {'in': [AccentedTuple('ø·', 'b.b:e:q.')],
                       'an': [AccentedTuple('а·', 'b.b:e:q.')]},
            'sg_loc': {'an': [AccentedTuple('у·', 'b.b:e:q.')],
                       'in': [AccentedTuple('у·', 'b.b:c:d:e:q.')]}
            }

vocative_dict = {'u': [AccentedTuple('у0·', 'b.b:c:d:e:q.')],
          'ue': [AccentedTuple('у0·', 'b.b:c:d:e:q.'), AccentedTuple('ʺе0·', 'b.b:c:d:e:q.')],
          'e': [AccentedTuple('ʺе0·', 'b.b:c:d:e:q.')]}

def m_plural(suff='_'):
   ov = AccentedTuple('>œ·в', 'b.b:d:e:')
   plurals = [
       [[AccentedTuple('ʹи·', 'b.b:e:q.')]],
       [[AccentedTuple('е·', 'b.b:e:q.')]],
       [[AccentedTuple('<а·\u0304', 'b.b:c:d:e:')], [AccentedTuple('<а·\u0304', 'b.b:e:')]],
       [[AccentedTuple('ʹи·ма', 'b.b:c:e:q.')], [AccentedTuple('ʹи·ма', 'b.b:e:q.')]],
       [[AccentedTuple('ʹи·ма', 'b.b:c:e:q.')], [AccentedTuple('ʹи·ма', 'b.b:e:q.')]],
       [[AccentedTuple('ʹи·ма', 'b.b:c:e:q.')], [AccentedTuple('ʹи·ма', 'b.b:e:q.')]],
       [[AccentedTuple('ʹи0·', 'b.b:c:e:q.')]]
             ]
   if suff == '+':
      return [[[ov] + a for a in plural] for plural in plurals]
   elif suff == '_':
      return plurals
   elif suff == '±':
      return [[[ov] + a for a in plural] + [a for a in plural] for plural in plurals]
   else:
      raise NotImplementedError("Unknown paradigm")
   


def c_m(suff, anim, vocative):
   m_singular_ = [
         [[AccentedTuple('ø·', 'b.b:e:q.')]],
   [anim_dict['sg_acc'][anim]],
   [[AccentedTuple('а·', 'b.b:e:q.')]],
   [[AccentedTuple('у·', 'b.b:e:q.')]],
   [[AccentedTuple('œ·м', 'b.b:e:q.')]],
   [anim_dict['sg_loc'][anim]],
   [vocative_dict[vocative]],
   ]

   m_plural_ = m_plural(suff)
   declension = m_singular_ + m_plural_
   return NounStem(*declension)
