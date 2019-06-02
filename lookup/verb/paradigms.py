from typing import Dict, Iterator, NamedTuple, Tuple, List
from ..paradigm_helpers import (AccentedTuple, nice_name,
                                MorphemeChain, LabeledEnding)
from ..charutils import cmacron

class Present(NamedTuple):
   prs_1_sg: List[MorphemeChain]
   prs_2_sg: List[MorphemeChain]
   prs_3_sg: List[MorphemeChain]
   prs_1_pl: List[MorphemeChain]
   prs_2_pl: List[MorphemeChain]
   prs_3_pl: List[MorphemeChain]
   imv_2_sg: List[MorphemeChain]
   imv_1_pl: List[MorphemeChain]
   imv_2_pl: List[MorphemeChain]

   @property
   def labeled_endings(self) -> Iterator[LabeledEnding]:
      yield from zip(map(nice_name, self._fields),
                     super().__iter__())

class Past(NamedTuple):
   pf_m_sg: List[MorphemeChain]
   pf_f_sg: List[MorphemeChain]
   pf_n_sg: List[MorphemeChain]
   pf_m_pl: List[MorphemeChain]
   pf_f_pl: List[MorphemeChain]
   pf_n_pl: List[MorphemeChain]
   aor_1_sg: List[MorphemeChain]
   aor_2_sg: List[MorphemeChain]
   aor_3_sg: List[MorphemeChain]
   aor_1_pl: List[MorphemeChain]
   aor_2_pl: List[MorphemeChain]
   aor_3_pl: List[MorphemeChain]
   infinitive: List[MorphemeChain]
   ipf_1_sg: List[MorphemeChain]
   ipf_2_sg: List[MorphemeChain]
   ipf_3_sg: List[MorphemeChain]
   ipf_1_pl: List[MorphemeChain]
   ipf_2_pl: List[MorphemeChain]
   ipf_3_pl: List[MorphemeChain]

   @property
   def labeled_endings(self) -> Iterator[LabeledEnding]:
      yield from zip(map(nice_name, self._fields),
                     super().__iter__())


class Stems(NamedTuple):
   present: Present
   past: Past

   @property
   def labeled_endings(self) -> Iterator[LabeledEnding]:
      yield from self.present.labeled_endings
      yield from self.past.labeled_endings

i_theme_past = AccentedTuple('и·', 'p.p:r.r:s0')
a_theme_past = AccentedTuple('а·~', ' k:l.m.n.p:t.x.y0z0')
ie_theme_past = AccentedTuple('ѣ·', 'k.q:s.')
#zero_theme_past = AccentedTuple('', '')
#nu_theme_past = AccentedTuple('ну', '') # TODO: finish the book first!
ova_theme_past = AccentedTuple('ова·', 'm.')
iva_theme_past = AccentedTuple(f'и{cmacron}ва·', 'k’')

i_theme_ipf = AccentedTuple(f'ȷа{cmacron}·', 'r.r:s0')
ie_theme_ipf = AccentedTuple(f'ȷа{cmacron}·', 'q:s.')
ie2_theme_ipf = AccentedTuple(f'ꙓ·ја{cmacron}', 's.')
a_theme_ipf = AccentedTuple(f'а{cmacron}·', 'm.n.y0z0')
ova_theme_ipf = AccentedTuple(f'о·ва{cmacron}', 'm.')
iva_theme_ipf = AccentedTuple(f'и{cmacron}·ва{cmacron}', 'k’')

ending_null = AccentedTuple('', '')
ending_x = AccentedTuple('х', '')
ending_she = AccentedTuple('ше', '')
ending_smo = AccentedTuple('смо', '')
ending_ste = AccentedTuple('сте', '')
ending_xu = AccentedTuple('ху', '')
ending_ti = AccentedTuple('ти', '')

i_past = Past(
   [[i_theme_past, AccentedTuple('ʌ', '')]],
   [[i_theme_past, AccentedTuple('ла', '')]],
   [[i_theme_past, AccentedTuple('ло', '')]],
   [[i_theme_past, AccentedTuple('ли', '')]],
   [[i_theme_past, AccentedTuple('ле', '')]],
   [[i_theme_past, AccentedTuple('ла', '')]],
   [[i_theme_past, ending_x]],
   [[AccentedTuple('и·', 's0'), AccentedTuple('0·~', 'o.p.p:r.r:')]],
   [[AccentedTuple('и·', 's0'), AccentedTuple('0·~', 'o.p.p:r.r:')]],
   [[i_theme_past, ending_smo]],
   [[i_theme_past, ending_ste]],
   [[i_theme_past, ending_she]],
   [[i_theme_past, ending_ti]],
   [[i_theme_ipf, ending_x]],
   [[i_theme_ipf, ending_she]],
   [[i_theme_ipf, ending_she]],
   [[i_theme_ipf, ending_smo]],
   [[i_theme_ipf, ending_ste]],
   [[i_theme_ipf, ending_xu]]
)

a_past = Past(
   [[a_theme_past, AccentedTuple('ʌ0·', 'm.x.')]],
   [[a_theme_past, AccentedTuple('ла0·', 'm.x.')]],
   [[a_theme_past, AccentedTuple('ло0·', 'm.x.')]],
   [[a_theme_past, AccentedTuple('ли0·', 'm.x.')]],
   [[a_theme_past, AccentedTuple('ле0·', 'm.x.')]],
   [[a_theme_past, AccentedTuple('ла0·', 'm.x.')]],
   [[a_theme_past, ending_x]],
   [[AccentedTuple('а·', 'l.p:x.y0'), AccentedTuple('0·~', 'o.k:m.n.t.x.')]],
   [[AccentedTuple('а·', 'l.p:x.y0'), AccentedTuple('0·~', 'o.k:m.n.t.x.')]],
   [[a_theme_past, ending_smo]],
   [[a_theme_past, ending_ste]],
   [[a_theme_past, ending_she]],
   [[a_theme_past, ending_ti]],
   [[a_theme_ipf, ending_x]],
   [[a_theme_ipf, ending_she]],
   [[a_theme_ipf, ending_she]],
   [[a_theme_ipf, ending_smo]],
   [[a_theme_ipf, ending_smo]],
   [[a_theme_ipf, ending_xu]]
)

ie_past = Past(
   [[ie_theme_past, AccentedTuple('ʌ', '')]],
   [[ie_theme_past, AccentedTuple('ла', '')]],
   [[ie_theme_past, AccentedTuple('ло', '')]],
   [[ie_theme_past, AccentedTuple('ли', '')]],
   [[ie_theme_past, AccentedTuple('ле', '')]],
   [[ie_theme_past, AccentedTuple('ла', '')]],
   [[ie_theme_past, ending_x]],
   [[ie_theme_past, ending_null]],
   [[ie_theme_past, ending_null]],
   [[ie_theme_past, ending_smo]],
   [[ie_theme_past, ending_ste]],
   [[ie_theme_past, ending_she]],
   [[ie_theme_past, ending_ti]],
   [[ie_theme_ipf, ending_x]],
   [[ie_theme_ipf, ending_she]],
   [[ie_theme_ipf, ending_she]],
   [[ie_theme_ipf, ending_smo]],
   [[ie_theme_ipf, ending_ste]],
   [[ie_theme_ipf, ending_xu]]
)

ie2_past = Past(
   [[ie_theme_past, AccentedTuple('ʌ', '')]],
   [[ie_theme_past, AccentedTuple('ла', '')]],
   [[ie_theme_past, AccentedTuple('ло', '')]],
   [[ie_theme_past, AccentedTuple('ли', '')]],
   [[ie_theme_past, AccentedTuple('ле', '')]],
   [[ie_theme_past, AccentedTuple('ла', '')]],
   [[ie_theme_past, ending_x]],
   [[ie_theme_past, ending_null]],
   [[ie_theme_past, ending_null]],
   [[ie_theme_past, ending_smo]],
   [[ie_theme_past, ending_ste]],
   [[ie_theme_past, ending_she]],
   [[ie_theme_past, ending_ti]],
   [[ie2_theme_ipf, ending_x]],
   [[ie2_theme_ipf, ending_she]],
   [[ie2_theme_ipf, ending_she]],
   [[ie2_theme_ipf, ending_smo]],
   [[ie2_theme_ipf, ending_ste]],
   [[ie2_theme_ipf, ending_xu]]
)

ova_past = Past(
   [[AccentedTuple('ова~', ''), AccentedTuple('ʌ0·', 'm.')]],
   [[AccentedTuple('ова~', ''), AccentedTuple('ла0·', 'm.')]],
   [[AccentedTuple('ова~', ''), AccentedTuple('ло0·', 'm.')]],
   [[AccentedTuple('ова~', ''), AccentedTuple('ли0·', 'm.')]],
   [[AccentedTuple('ова~', ''), AccentedTuple('ле0·', 'm.')]],
   [[AccentedTuple('ова~', ''), AccentedTuple('ла0·', 'm.')]],
   [[ova_theme_past, ending_x]],
   [[AccentedTuple('ова', ''), AccentedTuple('0·~', 'o.m.')]],
   [[AccentedTuple('ова', ''), AccentedTuple('0·~', 'o.m.')]],
   [[ova_theme_past, ending_smo]],
   [[ova_theme_past, ending_ste]],
   [[ova_theme_past, ending_she]],
   [[ova_theme_past, ending_ti]],
   [[ova_theme_ipf, ending_x]],
   [[ova_theme_ipf, ending_she]],
   [[ova_theme_ipf, ending_she]],
   [[ova_theme_ipf, ending_smo]],
   [[ova_theme_ipf, ending_ste]],
   [[ova_theme_ipf, ending_xu]]
)

iva_past = Past(
   [[iva_theme_past, AccentedTuple('ʌ', '')]],
   [[iva_theme_past, AccentedTuple('ла', '')]],
   [[iva_theme_past, AccentedTuple('ло', '')]],
   [[iva_theme_past, AccentedTuple('ли', '')]],
   [[iva_theme_past, AccentedTuple('ле', '')]],
   [[iva_theme_past, AccentedTuple('ла', '')]],
   [[iva_theme_past, ending_x]],
   [[iva_theme_past, AccentedTuple('·', 'k’')]],
   [[iva_theme_past, AccentedTuple('·', 'k’')]],
   [[iva_theme_past, ending_smo]],
   [[iva_theme_past, ending_ste]],
   [[iva_theme_past, ending_she]],
   [[iva_theme_past, ending_ti]],
   [[iva_theme_ipf, ending_x]],
   [[iva_theme_ipf, ending_she]],
   [[iva_theme_ipf, ending_she]],
   [[iva_theme_ipf, ending_smo]],
   [[iva_theme_ipf, ending_ste]],
   [[iva_theme_ipf, ending_xu]]
)

#("e", Present),   — todo later
#("ne", Present) — todo after finishing the book

i_theme_prs = AccentedTuple(f'и·{cmacron}', 'q:r.r:s0s.x.')
je_theme_prs = AccentedTuple(f'ȷе·{cmacron}', 'z0')
a_theme_prs = AccentedTuple(f'а·{cmacron}', 'm.n.y0')
uje_theme_prs = AccentedTuple(f'у·је{cmacron}', 'k’m.')
ie_theme_prs = AccentedTuple(f'ꙓ·{cmacron}', 's.')

i_theme_imv = AccentedTuple('ӥ·', 'k.p.p:q:r.r:s0s.x.')
je_theme_imv = AccentedTuple('ȷӥ·', 'l.m.p:t.z0')
a_theme_imv = AccentedTuple(f'а·{cmacron}ј', 'm.n.y0')
uje_theme_imv = AccentedTuple(f'у·{cmacron}ј', 'k’m.')
ie_theme_imv = AccentedTuple(f'ꙓ·{cmacron}ј', 's.')

ending_mo = AccentedTuple('мо', '')
ending_te = AccentedTuple('те', '')
ending_m = AccentedTuple('м', '')
ending_sh = AccentedTuple('ш', '')

i_present = Present(
   [[i_theme_prs, ending_m]],
   [[i_theme_prs, ending_sh]],
   [[i_theme_prs, ending_null]],
   [[AccentedTuple(f'и·{cmacron}', 'q:r.r:'), AccentedTuple('мо·', 'r.s0s.x.')],
   [i_theme_prs, ending_mo]],
   [[AccentedTuple(f'и·{cmacron}', 'q:r.r:'), AccentedTuple('те·', 'r.s0s.x.')],
   [i_theme_prs, ending_te]],
   [[AccentedTuple(f'е·{cmacron}', 'q:r.r:s0s.x.'), ending_null]],
   [[i_theme_imv, ending_null]],
   [[i_theme_imv, ending_mo]],
   [[i_theme_imv, ending_te]]
)

je_present = Present(
   [[je_theme_prs, ending_m]],
   [[je_theme_prs, ending_sh]],
   [[je_theme_prs, ending_null]],
   [[AccentedTuple(f'ȷе·{cmacron}', ''), AccentedTuple('мо·', 'z0')],
   [je_theme_prs, ending_mo]],
   [[AccentedTuple(f'ȷе·{cmacron}', ''), AccentedTuple('те·', 'z0')],
   [je_theme_prs, ending_te]],
   [[AccentedTuple(f'ȷу·{cmacron}', 'z0'), ending_null]],
   [[je_theme_imv, ending_null]],
   [[je_theme_imv, ending_mo]],
   [[je_theme_imv, ending_te]]
)

a_present = Present(
   [[a_theme_prs, ending_m]],
   [[a_theme_prs, ending_sh]],
   [[a_theme_prs, ending_null]],
   [[AccentedTuple(f'а·{cmacron}', 'x.'), AccentedTuple('мо·', 'n.y0')],
   [a_theme_prs, ending_mo]],
   [[AccentedTuple(f'а·{cmacron}', 'x.'), AccentedTuple('те·', 'n.y0')],
   [a_theme_prs, ending_te]],
   [[AccentedTuple(f'а·ју{cmacron}', 'k:l.n.x.y0'), ending_null]],
   [[a_theme_imv, ending_null]],
   [[a_theme_imv, ending_mo]],
   [[a_theme_imv, ending_te]]
)

uje_present = Present(
   [[uje_theme_prs, ending_m]],
   [[uje_theme_prs, ending_sh]],
   [[uje_theme_prs, ending_null]],
   [[uje_theme_prs, ending_mo]],
   [[uje_theme_prs, ending_te]],
   [[AccentedTuple(f'у·ју{cmacron}', 'k’m.'), ending_null]],
   [[uje_theme_imv, ending_null]],
   [[uje_theme_imv, ending_mo]],
   [[uje_theme_imv, ending_te]]
)

ie_present = Present(
   [[ie_theme_prs, ending_m]],
   [[ie_theme_prs, ending_sh]],
   [[ie_theme_prs, ending_null]],
   [[AccentedTuple(f'ꙓ{cmacron}', ''), AccentedTuple('мо·', 's.')],
   [ie_theme_prs, ending_mo]],
   [[AccentedTuple(f'ꙓ{cmacron}', ''), AccentedTuple('те·', 's.')],
   [ie_theme_prs, ending_te]],
   [[AccentedTuple(f'ѣ·ју{cmacron}', 's.'), ending_null]],
   [[ie_theme_imv, ending_null]],
   [[ie_theme_imv, ending_mo]],
   [[ie_theme_imv, ending_te]]
)

MP_to_verb_stems: Dict[str, Stems] = dict(
   alpha=Stems(i_present, i_past),
   beta=Stems(a_present, a_past),
   delta=Stems(je_present, a_past),
   epsilon=Stems(uje_present, ova_past),
   zeta=Stems(uje_present, iva_past),
   eta=Stems(i_present, ie_past),
   theta=Stems(ie_present, ie2_past),
   mu=Stems(i_present,a_past)
)