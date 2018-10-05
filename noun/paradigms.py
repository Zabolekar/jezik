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

anim_dict = {'sg_acc': {'in': [AccentedTuple('ø·', 'b:')],
                       'an': [AccentedTuple('а·', 'b:')]},
            'sg_loc': {'an': [AccentedTuple('у·', 'b:')],
                       'in': [AccentedTuple('у·', 'b:c:')]}
            }

def m_plural(suff='_'):
   ov = AccentedTuple('>œ·в', 'b:')
   plurals = [
       [[AccentedTuple('ʹи·', 'b:')]],
       [[AccentedTuple('е·', 'b:')]],
       [[AccentedTuple('<а·\u0304', 'b:c:')], [AccentedTuple('<а·\u0304', 'b:')]],
       [[AccentedTuple('ʹи·ма', 'b:c:')], [AccentedTuple('ʹи·ма', 'b:')]],
       [[AccentedTuple('ʹи·ма', 'b:c:')], [AccentedTuple('ʹи·ма', 'b:')]],
       [[AccentedTuple('ʹи·ма', 'b:c:')], [AccentedTuple('ʹи·ма', 'b:')]],
       [[AccentedTuple('ʹи·', 'b:')]]
             ]
   if suff == '+':
      return [[[ov] + a for a in plural] for plural in plurals]
   elif suff == '_':
      return plurals
   elif suff == '±':
      return [[[ov] + a for a in plural] + [a for a in plural] for plural in plurals]
   else:
      raise UnknownParadigmError
   


def c_m(suff, anim):
   m_singular_ = [[[AccentedTuple('ø', 'b:')]],
   [anim_dict['sg_acc'][anim]],
   [[AccentedTuple('а·', 'b:')]],
   [[AccentedTuple('у·', 'b:')]],
   [[AccentedTuple('œ·м', 'b:')]],
   [anim_dict['sg_loc'][anim]],
   [[AccentedTuple('ʺе·', 'b:')]]]

   m_plural_ = m_plural(suff)

   declension = m_singular_ + m_plural_
   print('len_of_Declension: ', len(declension))
   return NounStem(*declension)