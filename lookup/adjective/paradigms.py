from typing import NamedTuple, List, Union
from ..paradigm_helpers import AccentedTuple
from ..charutils import cmacron

# TODO: why is this organized so differently from nouns and verbs? unify and/or document

class ShortAdj(NamedTuple):
   m_sg_nom_short: List[AccentedTuple] # len 1
   f_sg_nom_short: List[AccentedTuple] # 1
   n_sg_nom_short: List[AccentedTuple] # 1
   m_pl_nom_short: List[AccentedTuple] # 1
   f_pl_nom_short: List[AccentedTuple] # 1
   n_pl_nom_short: List[AccentedTuple] # 1
   m_pl_acc_short: List[AccentedTuple] # 1
   f_pl_acc_short: List[AccentedTuple] # 1; = f_pl_nom
   n_pl_acc_short: List[AccentedTuple] # 1; = n_pl_nom
   m_sg_gen_short: List[AccentedTuple] # 1
   m_sg_dat_short: List[AccentedTuple] # 1
   m_sg_loc_short: List[AccentedTuple] # 1
   f_sg_acc_short: List[AccentedTuple] # 1
   n_sg_acc_short: List[AccentedTuple] # 1; = n_sg_nom
   n_sg_gen_short: List[AccentedTuple] # 1; = m_sg_gen
   n_sg_dat_short: List[AccentedTuple] # 1; = m_sg_dat
   n_sg_loc_short: List[AccentedTuple] # 1; = m_sg_dat
   m_sg_acc_in_short: List[AccentedTuple] #; 1 = m_sg_nom
   m_sg_acc_an_short: List[AccentedTuple] #; 1 = m_sg_gen
   m_sg_ins_short: List[AccentedTuple]
   f_sg_ins_short: List[AccentedTuple]
   n_sg_ins_short: List[AccentedTuple]
   f_sg_gen_short: List[AccentedTuple]
   f_sg_dat_short: List[AccentedTuple]
   f_sg_loc_short: List[AccentedTuple]
   m_f_n_pl_gen_short: List[AccentedTuple]
   m_f_n_pl_dat_loc_ins_short: List[AccentedTuple]
   

short_adj = ShortAdj(
   [AccentedTuple('ø·', 'b.b:b?')], # ø is 'zero ending' (which, however, can take stress, in a way)
   [AccentedTuple('а·', 'b.b:b?d.d:')],
   [AccentedTuple('œ·', 'b.b:b?d.d:')],
   [AccentedTuple('и·', 'b.b:b?d.d:')],
   [AccentedTuple('е·', 'b.b:b?d.d:')],
   [AccentedTuple('а·', 'b.b:b?d.d:')],
   [AccentedTuple('е·', 'b.b:b?d.d:')],
   [AccentedTuple('е·', 'b.b:b?d.d:')], # = f_pl_nom
   [AccentedTuple('а·', 'b.b:b?d.d:')], # = n_pl_nom
   [AccentedTuple('а·', 'b.b:b?d.d:')],
   [AccentedTuple('у·', 'b.b:b?d.d:')],
   [AccentedTuple('у·', 'b.b:b?d.d:')],
   [AccentedTuple('у·', 'b.b:b?d.d:')],
   [AccentedTuple('œ·', 'b.b:b?d.d:')], # = n_sg_nom
   [AccentedTuple('а·', 'b.b:b?d.d:')], # = m_sg_gen
   [AccentedTuple('у·', 'b.b:b?d.d:')], # = m_sg_dat
   [AccentedTuple('у·', 'b.b:b?d.d:')], # = m_sg_dat
   [AccentedTuple('ø·', 'b.b:b?')], #; = m_sg_nom
   [AccentedTuple('а·', 'b.b:b?d.d:')], #; = m_sg_gen
   [AccentedTuple(f'и·{cmacron}м', 'b.b:b?d.d:')],
   [AccentedTuple(f'о·{cmacron}м', 'b.b:b?d.d:')],
   [AccentedTuple(f'и·{cmacron}м', 'b.b:b?d.d:')],
   [AccentedTuple(f'е·{cmacron}', 'b.b:b?d.d:')],
   [AccentedTuple(f'о·{cmacron}ј', 'b.b:b?d.d:')],
   [AccentedTuple(f'о·{cmacron}ј', 'b.b:b?d.d:')],
   [AccentedTuple(f'и·{cmacron}х', 'b.b:b?d.d:')],
   [AccentedTuple(f'и·{cmacron}м', 'b.b:b?d.d:'),
    AccentedTuple(f'и·{cmacron}ма', 'b.b:b?d.d:')]
   )

class LongAdj(NamedTuple):
   m_sg_nom_long: List[AccentedTuple] # len 1
   m_sg_gen_long: List[AccentedTuple] # ! len 2
   m_sg_dat_long: List[AccentedTuple] # ! len 3
   m_sg_ins_long: List[AccentedTuple] # 1
   m_sg_loc_long: List[AccentedTuple] # ! 3
   m_sg_acc_an_long: List[AccentedTuple] # ! 2; = m_sg_gen
   m_sg_acc_in_long: List[AccentedTuple] # 1; = m_sg_nom
   f_sg_nom_long: List[AccentedTuple] # 1
   f_sg_gen_long: List[AccentedTuple] # 1
   f_sg_dat_long: List[AccentedTuple] # 1
   f_sg_acc_long: List[AccentedTuple] # 1
   f_sg_ins_long: List[AccentedTuple] # 1
   f_sg_loc_long: List[AccentedTuple] # 1
   n_sg_nom_long: List[AccentedTuple] # 1
   n_sg_gen_long: List[AccentedTuple] # ! 2; = m_sg_gen
   n_sg_dat_long: List[AccentedTuple] # ! 3; = m_sg_dat
   n_sg_acc_long: List[AccentedTuple] # 1; = n_sg_nom
   n_sg_ins_long: List[AccentedTuple] # 1; = m_sg_ins
   n_sg_loc_long: List[AccentedTuple] # ! 3; = m_sg_loc
   m_pl_nom_long: List[AccentedTuple] # 1
   f_pl_nom_long: List[AccentedTuple] # 1
   n_pl_nom_long: List[AccentedTuple] # 1
   m_pl_acc_long: List[AccentedTuple] # 1
   f_pl_acc_long: List[AccentedTuple] # 1; = f_pl_nom
   n_pl_acc_long: List[AccentedTuple] # 1; = n_pl_nom
   m_f_n_pl_gen_long: List[AccentedTuple] # 1
   m_f_n_pl_dat_loc_ins_long: List[AccentedTuple] # ! 2

long_adj = LongAdj(
  [AccentedTuple(f'и·{cmacron}', 'c.c:')],
  [AccentedTuple(f'œ·{cmacron}г', 'c.c:'),
   AccentedTuple(f'œ·{cmacron}га', 'c.c:')],
  [AccentedTuple(f'œ·{cmacron}м', 'c.c:'),
   AccentedTuple(f'œ·{cmacron}ме', 'c.c:'),
   AccentedTuple(f'œ·{cmacron}му', 'c.c:')],
  [AccentedTuple(f'и·{cmacron}м', 'c.c:')],
  [AccentedTuple(f'œ·{cmacron}м', 'c.c:'),
   AccentedTuple(f'œ·{cmacron}ме', 'c.c:'),
   AccentedTuple(f'œ·{cmacron}му', 'c.c:')],
  [AccentedTuple(f'œ·{cmacron}г', 'c.c:'),
   AccentedTuple(f'œ·{cmacron}га', 'c.c:')],
  [AccentedTuple(f'и·{cmacron}', 'c.c:')],
  [AccentedTuple(f'а·{cmacron}', 'c.c:')],
  [AccentedTuple(f'е·{cmacron}', 'c.c:')],
  [AccentedTuple(f'о·{cmacron}ј', 'c.c:')],
  [AccentedTuple(f'у·{cmacron}', 'c.c:')],
  [AccentedTuple(f'о·{cmacron}м', 'c.c:')],
  [AccentedTuple(f'о·{cmacron}ј', 'c.c:')],
  [AccentedTuple(f'œ·{cmacron}', 'c.c:')],
  [AccentedTuple(f'œ·{cmacron}г', 'c.c:'),
   AccentedTuple(f'œ·{cmacron}га', 'c.c:')], # = m_sg_gen
  [AccentedTuple(f'œ·{cmacron}м', 'c.c:'),
   AccentedTuple(f'œ·{cmacron}ме', 'c.c:'),
   AccentedTuple(f'œ·{cmacron}му', 'c.c:')], # = m_sg_dat
  [AccentedTuple(f'œ·{cmacron}', 'c.c:')], # = n_sg_nom
  [AccentedTuple(f'и·{cmacron}м', 'c.c:')], # = m_sg_ins
  [AccentedTuple(f'œ·{cmacron}м', 'c.c:'),
   AccentedTuple(f'œ·{cmacron}ме', 'c.c:'),
   AccentedTuple(f'œ·{cmacron}му', 'c.c:')], # = m_sg_loc
  [AccentedTuple(f'и·{cmacron}', 'c.c:')],
  [AccentedTuple(f'е·{cmacron}', 'c.c:')],
  [AccentedTuple(f'а·{cmacron}', 'c.c:')],
  [AccentedTuple(f'е·{cmacron}', 'c.c:')],
  [AccentedTuple(f'е·{cmacron}', 'c.c:')], #  = f_pl_nom
  [AccentedTuple(f'а·{cmacron}', 'c.c:')], #  = n_pl_nom
  [AccentedTuple(f'и·{cmacron}х', 'c.c:')],
  [AccentedTuple(f'и·{cmacron}м', 'c.c:'),
   AccentedTuple(f'и·{cmacron}ма', 'c.c:')]
  )

class MixedAdj(NamedTuple):
   # TODO: sveto: document
   m_sg_nom_short: List[AccentedTuple]
   m_sg_gen_long: List[AccentedTuple]
   m_sg_gen_short: List[AccentedTuple]
   m_sg_dat_long: List[AccentedTuple]
   m_sg_dat_short: List[AccentedTuple]
   m_sg_ins_long: List[AccentedTuple]
   m_sg_loc_long: List[AccentedTuple]
   m_sg_loc_short: List[AccentedTuple]
   m_sg_acc_in_short: List[AccentedTuple]
   m_sg_acc_an_long: List[AccentedTuple]
   m_sg_acc_an_short: List[AccentedTuple]
   f_sg_nom_short: List[AccentedTuple]
   f_sg_gen_long: List[AccentedTuple]
   f_sg_dat_long: List[AccentedTuple]
   f_sg_acc_short: List[AccentedTuple]
   f_sg_ins_long: List[AccentedTuple]
   f_sg_loc_long: List[AccentedTuple]
   n_sg_nom_short: List[AccentedTuple]
   n_sg_gen_long: List[AccentedTuple]
   n_sg_gen_short: List[AccentedTuple]
   n_sg_dat_long: List[AccentedTuple]
   n_sg_dat_short: List[AccentedTuple]
   n_sg_acc_short: List[AccentedTuple]
   n_sg_ins_long: List[AccentedTuple]
   n_sg_loc_long: List[AccentedTuple]
   n_sg_loc_short: List[AccentedTuple]
   m_pl_nom_short: List[AccentedTuple]
   f_pl_nom_short: List[AccentedTuple]
   n_pl_nom_short: List[AccentedTuple]
   m_pl_acc_short: List[AccentedTuple]
   f_pl_acc_short: List[AccentedTuple]
   n_pl_acc_short: List[AccentedTuple]
   m_f_n_pl_gen_long: List[AccentedTuple]
   m_f_n_pl_dat_loc_ins_long: List[AccentedTuple]

mixed_adj = MixedAdj(
  m_sg_nom_short = short_adj.m_sg_nom_short,
  m_sg_gen_long = long_adj.m_sg_gen_long,
  m_sg_gen_short = short_adj.m_sg_gen_short,
  m_sg_dat_long = long_adj.m_sg_dat_long,
  m_sg_dat_short = short_adj.m_sg_dat_short,
  m_sg_ins_long = long_adj.m_sg_ins_long,
  m_sg_loc_long = long_adj.m_sg_loc_long,
  m_sg_loc_short = short_adj.m_sg_loc_short,
  m_sg_acc_in_short = short_adj.m_sg_acc_in_short,
  m_sg_acc_an_long = long_adj.m_sg_acc_an_long,
  m_sg_acc_an_short = short_adj.m_sg_acc_an_short,
  f_sg_nom_short = short_adj.f_sg_nom_short,
  f_sg_gen_long = long_adj.f_sg_gen_long,
  f_sg_dat_long = long_adj.f_sg_dat_long,
  f_sg_acc_short = short_adj.f_sg_acc_short,
  f_sg_ins_long = long_adj.f_sg_ins_long,
  f_sg_loc_long = long_adj.f_sg_loc_long,
  n_sg_nom_short = short_adj.n_sg_nom_short,
  n_sg_gen_long = long_adj.n_sg_gen_long,
  n_sg_gen_short = short_adj.n_sg_gen_short,
  n_sg_dat_long = long_adj.n_sg_dat_long,
  n_sg_dat_short = short_adj.n_sg_dat_short,
  n_sg_acc_short = short_adj.n_sg_acc_short,
  n_sg_ins_long = long_adj.n_sg_ins_long,
  n_sg_loc_long = long_adj.n_sg_loc_long,
  n_sg_loc_short = short_adj.n_sg_loc_short,
  m_pl_nom_short = short_adj.m_pl_nom_short,
  f_pl_nom_short = short_adj.f_pl_nom_short,
  n_pl_nom_short = short_adj.n_pl_nom_short,
  m_pl_acc_short = short_adj.m_pl_acc_short,
  f_pl_acc_short = short_adj.f_pl_acc_short,
  n_pl_acc_short = short_adj.n_pl_acc_short,
  m_f_n_pl_gen_long = long_adj.m_f_n_pl_gen_long,
  m_f_n_pl_dat_loc_ins_long = long_adj.m_f_n_pl_dat_loc_ins_long)

AdjParadigm = Union[ShortAdj, LongAdj, MixedAdj]
