from typing import Dict, Iterator, NamedTuple, Tuple, List
import re
from ..paradigm_helpers import AccentedTuple

class VerbEnding(NamedTuple):
   theme: AccentedTuple
   ending: AccentedTuple

LabeledEnding = Tuple[str, List[VerbEnding]]

_r = re.compile("([a-z]+|[A-Z]|\d)")
def nice_name(name: str) -> str:
   return " ".join(_r.findall(name)) # TODO

class Present(NamedTuple):
   prs1sg: List[VerbEnding]
   prs2sg: List[VerbEnding]
   prs3sg: List[VerbEnding]
   prs1pl: List[VerbEnding]
   prs2pl: List[VerbEnding]
   prs3pl: List[VerbEnding]
   imv2sg: List[VerbEnding]
   imv1pl: List[VerbEnding]
   imv2pl: List[VerbEnding]

   @property
   def labeled_endings(self) -> Iterator[LabeledEnding]:
      yield from zip(map(nice_name, self._fields),
                     super().__iter__())

class Past(NamedTuple):
   pfMsg: List[VerbEnding]
   pfFsg: List[VerbEnding]
   pfNsg: List[VerbEnding]
   pfMpl: List[VerbEnding]
   pfFpl: List[VerbEnding]
   pfnNpl: List[VerbEnding]
   aor1sg: List[VerbEnding]
   aor2sg: List[VerbEnding]
   aor3sg: List[VerbEnding]
   aor1pl: List[VerbEnding]
   aor2pl: List[VerbEnding]
   aor3pl: List[VerbEnding]
   infinitive: List[VerbEnding]
   ipf1sg: List[VerbEnding]
   ipf2sg: List[VerbEnding]
   ipf3sg: List[VerbEnding]
   ipf1pl: List[VerbEnding]
   ipf2pl: List[VerbEnding]
   ipf3pl: List[VerbEnding]

   @property
   def labeled_endings(self) -> Iterator[LabeledEnding]:
      yield from zip(map(nice_name, self._fields),
                     super().__iter__())

"""class Presents(NamedTuple):
   i: Present
   e: Present
   a: Present
   je: Present
   ie: Present
   uje: Present

class Pasts(NamedTuple):
   i: Past
   a: Past
   ie: Past
   ova: Past
   u: Past # TODO: add "zero" after finishing the book!
"""

class Stems(NamedTuple):
   present: Present
   past: Past

   @property
   def labeled_endings(self) -> Iterator[LabeledEnding]:
      yield from self.present.labeled_endings
      yield from self.past.labeled_endings

i_theme_past = AccentedTuple('и·', 'p.p:r.r:s0')
a_theme_past = AccentedTuple('а·~', ' k:l.m.n.p:t.x.y0z0')
ie_theme_past = AccentedTuple('е·', 'k.q:s.')
#zero_theme_past = AccentedTuple('', '')
#nu_theme_past = AccentedTuple('ну', '') # TODO: finish the book first!
ova_theme_past = AccentedTuple('ова·', 'm.')
iva_theme_past = AccentedTuple('и\u0304ва·', 'k’')

i_theme_ipf = AccentedTuple('ȷа\u0304·', 'r.r:s0')
ie_theme_ipf = AccentedTuple('ȷа\u0304·', 'q:s.')
a_theme_ipf = AccentedTuple('а\u0304·', 'm.n.y0z0')
ova_theme_ipf = AccentedTuple('о·ва\u0304', 'm.')
iva_theme_ipf = AccentedTuple('и\u0304·ва\u0304', 'k’')

ending_null = AccentedTuple('', '')
ending_x = AccentedTuple('х', '')
ending_she = AccentedTuple('ше', '')
ending_smo = AccentedTuple('смо', '')
ending_ste = AccentedTuple('сте', '')
ending_xu = AccentedTuple('ху', '')
ending_ti = AccentedTuple('ти', '')

i_past = Past(
   [VerbEnding(i_theme_past, AccentedTuple('ʌ', ''))],
   [VerbEnding(i_theme_past, AccentedTuple('ла', ''))],
   [VerbEnding(i_theme_past, AccentedTuple('ло', ''))],
   [VerbEnding(i_theme_past, AccentedTuple('ли', ''))],
   [VerbEnding(i_theme_past, AccentedTuple('ле', ''))],
   [VerbEnding(i_theme_past, AccentedTuple('ла', ''))],
   [VerbEnding(i_theme_past, ending_x)],
   [VerbEnding(AccentedTuple('и·', 's0'), AccentedTuple('0·~', 'o.p.p:r.r:'))],
   [VerbEnding(AccentedTuple('и·', 's0'), AccentedTuple('0·~', 'o.p.p:r.r:'))],
   [VerbEnding(i_theme_past, ending_smo)],
   [VerbEnding(i_theme_past, ending_ste)],
   [VerbEnding(i_theme_past, ending_she)],
   [VerbEnding(i_theme_past, ending_ti)],
   [VerbEnding(i_theme_ipf, ending_x)],
   [VerbEnding(i_theme_ipf, ending_she)],
   [VerbEnding(i_theme_ipf, ending_she)],
   [VerbEnding(i_theme_ipf, ending_smo)],
   [VerbEnding(i_theme_ipf, ending_ste)],
   [VerbEnding(i_theme_ipf, ending_xu)]
)

a_past = Past(
   [VerbEnding(a_theme_past, AccentedTuple('ʌ0·', 'm.'))],
   [VerbEnding(a_theme_past, AccentedTuple('ла0·', 'm.'))],
   [VerbEnding(a_theme_past, AccentedTuple('ло0·', 'm.'))],
   [VerbEnding(a_theme_past, AccentedTuple('ли0·', 'm.'))],
   [VerbEnding(a_theme_past, AccentedTuple('ле0·', 'm.'))],
   [VerbEnding(a_theme_past, AccentedTuple('ла0·', 'm.'))],
   [VerbEnding(a_theme_past, ending_x)],
   [VerbEnding(AccentedTuple('а·', 'l.p:x.y0'), AccentedTuple('0·~', 'o.k:m.n.t.'))],
   [VerbEnding(AccentedTuple('а·', 'l.p:x.y0'), AccentedTuple('0·~', 'o.k:m.n.t.'))],
   [VerbEnding(a_theme_past, ending_smo)],
   [VerbEnding(a_theme_past, ending_ste)],
   [VerbEnding(a_theme_past, ending_she)],
   [VerbEnding(a_theme_past, ending_ti)],
   [VerbEnding(a_theme_ipf, ending_x)],
   [VerbEnding(a_theme_ipf, ending_she)],
   [VerbEnding(a_theme_ipf, ending_she)],
   [VerbEnding(a_theme_ipf, ending_smo)],
   [VerbEnding(a_theme_ipf, ending_smo)],
   [VerbEnding(a_theme_ipf, ending_xu)]
)

ie_past = Past(
   [VerbEnding(ie_theme_past, AccentedTuple('ʌ', ''))],
   [VerbEnding(ie_theme_past, AccentedTuple('ла', ''))],
   [VerbEnding(ie_theme_past, AccentedTuple('ло', ''))],
   [VerbEnding(ie_theme_past, AccentedTuple('ли', ''))],
   [VerbEnding(ie_theme_past, AccentedTuple('ле', ''))],
   [VerbEnding(ie_theme_past, AccentedTuple('ла', ''))],
   [VerbEnding(ie_theme_past, ending_x)],
   [VerbEnding(ie_theme_past, ending_null)],
   [VerbEnding(ie_theme_past, ending_null)],
   [VerbEnding(ie_theme_past, ending_smo)],
   [VerbEnding(ie_theme_past, ending_ste)],
   [VerbEnding(ie_theme_past, ending_she)],
   [VerbEnding(ie_theme_past, ending_ti)],
   [VerbEnding(ie_theme_ipf, ending_x)],
   [VerbEnding(ie_theme_ipf, ending_she)],
   [VerbEnding(ie_theme_ipf, ending_she)],
   [VerbEnding(ie_theme_ipf, ending_smo)],
   [VerbEnding(ie_theme_ipf, ending_ste)],
   [VerbEnding(ie_theme_ipf, ending_xu)]
)

ova_past = Past(
   [VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ʌ0·', 'm.'))],
   [VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ла0·', 'm.'))],
   [VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ло0·', 'm.'))],
   [VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ли0·', 'm.'))],
   [VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ле0·', 'm.'))],
   [VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ла0·', 'm.'))],
   [VerbEnding(ova_theme_past, ending_x)],
   [VerbEnding(AccentedTuple('ова', ''), AccentedTuple('0·~', 'o.m.'))],
   [VerbEnding(AccentedTuple('ова', ''), AccentedTuple('0·~', 'o.m.'))],
   [VerbEnding(ova_theme_past, ending_smo)],
   [VerbEnding(ova_theme_past, ending_ste)],
   [VerbEnding(ova_theme_past, ending_she)],
   [VerbEnding(ova_theme_past, ending_ti)],
   [VerbEnding(ova_theme_ipf, ending_x)],
   [VerbEnding(ova_theme_ipf, ending_she)],
   [VerbEnding(ova_theme_ipf, ending_she)],
   [VerbEnding(ova_theme_ipf, ending_smo)],
   [VerbEnding(ova_theme_ipf, ending_ste)],
   [VerbEnding(ova_theme_ipf, ending_xu)]
)

iva_past = Past(
   [VerbEnding(iva_theme_past, AccentedTuple('ʌ', ''))],
   [VerbEnding(iva_theme_past, AccentedTuple('ла', ''))],
   [VerbEnding(iva_theme_past, AccentedTuple('ло', ''))],
   [VerbEnding(iva_theme_past, AccentedTuple('ли', ''))],
   [VerbEnding(iva_theme_past, AccentedTuple('ле', ''))],
   [VerbEnding(iva_theme_past, AccentedTuple('ла', ''))],
   [VerbEnding(iva_theme_past, ending_x)],
   [VerbEnding(iva_theme_past, AccentedTuple('·', 'k’'))],
   [VerbEnding(iva_theme_past, AccentedTuple('·', 'k’'))],
   [VerbEnding(iva_theme_past, ending_smo)],
   [VerbEnding(iva_theme_past, ending_ste)],
   [VerbEnding(iva_theme_past, ending_she)],
   [VerbEnding(iva_theme_past, ending_ti)],
   [VerbEnding(iva_theme_ipf, ending_x)],
   [VerbEnding(iva_theme_ipf, ending_she)],
   [VerbEnding(iva_theme_ipf, ending_she)],
   [VerbEnding(iva_theme_ipf, ending_smo)],
   [VerbEnding(iva_theme_ipf, ending_ste)],
   [VerbEnding(iva_theme_ipf, ending_xu)]
)

#("e", Present),   — todo later
#("ie", Present), — todo later
#("ne", Present) — todo after finishing the book

i_theme_prs = AccentedTuple('и·\u0304', 'r.r:s0')
je_theme_prs = AccentedTuple('\u0237е·\u0304', 'z0')
a_theme_prs = AccentedTuple('а·\u0304', 'm.n.y0')
uje_theme_prs = AccentedTuple('у·је\u0304', 'k’m.')

i_theme_imv = AccentedTuple('ӥ·', 'p.p:r.r:s0')
je_theme_imv = AccentedTuple('\u0237ӥ·', 'l.m.p:t.z0')
a_theme_imv = AccentedTuple('а·\u0304ј', 'm.n.y0')
uje_theme_imv = AccentedTuple('у·\u0304ј', 'k’m.')

ending_mo = AccentedTuple('мо', '')
ending_te = AccentedTuple('те', '')
ending_m = AccentedTuple('м', '')
ending_sh = AccentedTuple('ш', '')

i_present = Present(
   [VerbEnding(i_theme_prs, ending_m)],
   [VerbEnding(i_theme_prs, ending_sh)],
   [VerbEnding(i_theme_prs, ending_null)],
   [VerbEnding(AccentedTuple('и·\u0304', 'r.r:'), AccentedTuple('мо', 's0'))],
   [VerbEnding(AccentedTuple('и·\u0304', 'r.r:'), AccentedTuple('те', 's0'))],
   [VerbEnding(AccentedTuple('е·\u0304', 'r.r:s0'), ending_null)],
   [VerbEnding(i_theme_imv, ending_null)],
   [VerbEnding(i_theme_imv, ending_mo)],
   [VerbEnding(i_theme_imv, ending_te)]
)

je_present = Present(
   [VerbEnding(je_theme_prs, ending_m)],
   [VerbEnding(je_theme_prs, ending_sh)],
   [VerbEnding(je_theme_prs, ending_null)],
   [VerbEnding(AccentedTuple('\u0237е·\u0304', ''), AccentedTuple('мо', 'z0'))],
   [VerbEnding(AccentedTuple('\u0237е·\u0304', ''), AccentedTuple('те', 'z0'))],
   [VerbEnding(AccentedTuple('\u0237у·\u0304', 'z0'), ending_null)],
   [VerbEnding(je_theme_imv, ending_null)],
   [VerbEnding(je_theme_imv, ending_mo)],
   [VerbEnding(je_theme_imv, ending_te)]
)

a_present = Present(
   [VerbEnding(a_theme_prs, ending_m)],
   [VerbEnding(a_theme_prs, ending_sh)],
   [VerbEnding(a_theme_prs, ending_null)],
   [VerbEnding(AccentedTuple('а·\u0304', 'n.x.'), AccentedTuple('мо', 'y0'))],
   [VerbEnding(AccentedTuple('а·\u0304', 'n.x.'), AccentedTuple('те', 'y0'))],
   [VerbEnding(AccentedTuple('а·ју\u0304', 'k:l.n.x.y0'), ending_null)],
   [VerbEnding(a_theme_imv, ending_null)],
   [VerbEnding(a_theme_imv, ending_mo)],
   [VerbEnding(a_theme_imv, ending_te)]
)

uje_present = Present(
   [VerbEnding(uje_theme_prs, ending_m)],
   [VerbEnding(uje_theme_prs, ending_sh)],
   [VerbEnding(uje_theme_prs, ending_null)],
   [VerbEnding(uje_theme_prs, ending_mo)],
   [VerbEnding(uje_theme_prs, ending_te)],
   [VerbEnding(AccentedTuple('у·ју\u0304', 'k’m.'), ending_null)],
   [VerbEnding(uje_theme_imv, ending_null)],
   [VerbEnding(uje_theme_imv, ending_mo)],
   [VerbEnding(uje_theme_imv, ending_te)]
)

MP_to_verb_stems: Dict[str, Stems] = dict(
   alpha=Stems(i_present, i_past),
   beta=Stems(a_present, a_past),
   delta=Stems(je_present, a_past),
   epsilon=Stems(uje_present, ova_past),
   zeta=Stems(uje_present, iva_past),
   eta=Stems(i_present, ie_past),
)
