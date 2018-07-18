from typing import NamedTuple, List, Union
from ..paradigm_helpers import AccentedTuple

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

short_adj = ShortAdj(
   [AccentedTuple('ø·', 'b.b:b?')], # ø means 'zero ending' (which, however, can take stress, in a way)
   [AccentedTuple('а·', 'b.b:b?')],
   [AccentedTuple('œ·', 'b.b:b?')],
   [AccentedTuple('и·', 'b.b:b?')],
   [AccentedTuple('е·', 'b.b:b?')],
   [AccentedTuple('а·', 'b.b:b?')],
   [AccentedTuple('е·', 'b.b:b?')],
   [AccentedTuple('е·', 'b.b:b?')], # = f_pl_nom
   [AccentedTuple('а·', 'b.b:b?')], # = n_pl_nom
   [AccentedTuple('а·', 'b.b:b?')],
   [AccentedTuple('у·', 'b.b:b?')],
   [AccentedTuple('у·', 'b.b:b?')],
   [AccentedTuple('у·', 'b.b:b?')],
   [AccentedTuple('œ·', 'b.b:b?')], # = n_sg_nom
   [AccentedTuple('а·', 'b.b:b?')], # = m_sg_gen
   [AccentedTuple('у·', 'b.b:b?')], # = m_sg_dat
   [AccentedTuple('у·', 'b.b:b?')], # = m_sg_dat
   [AccentedTuple('ø·', 'b.b:b?')], #; = m_sg_nom
   [AccentedTuple('а·', 'b.b:b?')] #; = m_sg_gen
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
  [AccentedTuple('и·̄', 'c.c:')],
  [AccentedTuple('œ·̄г', 'c.c:'), AccentedTuple('œ·̄га', 'c.c:')],
  [AccentedTuple('œ·̄м', 'c.c:'), AccentedTuple('œ·̄ме', 'c.c:'), AccentedTuple('œ·̄му', 'c.c:')],
  [AccentedTuple('и·̄м', 'c.c:')],
  [AccentedTuple('œ·̄м', 'c.c:'), AccentedTuple('œ·̄ме', 'c.c:'), AccentedTuple('œ·̄му', 'c.c:')],
  [AccentedTuple('œ·̄г', 'c.c:'), AccentedTuple('œ·̄га', 'c.c:')],
  [AccentedTuple('и·̄', 'c.c:')],
  [AccentedTuple('а·̄', 'c.c:')],
  [AccentedTuple('е·̄', 'c.c:')],
  [AccentedTuple('о·̄ј', 'c.c:')],
  [AccentedTuple('у·̄', 'c.c:')],
  [AccentedTuple('о·̄м', 'c.c:')],
  [AccentedTuple('о·̄ј', 'c.c:')],
  [AccentedTuple('œ·̄', 'c.c:')],
  [AccentedTuple('œ·̄г', 'c.c:'), AccentedTuple('œ·̄га', 'c.c:')], # = m_sg_gen
  [AccentedTuple('œ·̄м', 'c.c:'), AccentedTuple('œ·̄ме', 'c.c:'), AccentedTuple('œ·̄му', 'c.c:')], # = m_sg_dat
  [AccentedTuple('œ·̄', 'c.c:')], # = n_sg_nom
  [AccentedTuple('и·̄м', 'c.c:')], # = m_sg_ins
  [AccentedTuple('œ·̄м', 'c.c:'), AccentedTuple('œ·̄ме', 'c.c:'), AccentedTuple('œ·̄му', 'c.c:')], # = m_sg_loc
  [AccentedTuple('и·̄', 'c.c:')],
  [AccentedTuple('е·̄', 'c.c:')],
  [AccentedTuple('а·̄', 'c.c:')],
  [AccentedTuple('е·̄', 'c.c:')],
  [AccentedTuple('е·̄', 'c.c:')], #  = f_pl_nom
  [AccentedTuple('а·̄', 'c.c:')], #  = n_pl_nom
  [AccentedTuple('и·̄х', 'c.c:')],
  [AccentedTuple('и·̄м', 'c.c:'), AccentedTuple('и·̄ма', 'c.c:')]
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
  f_sg_acc_short = short_adj.m_sg_nom_short,
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
