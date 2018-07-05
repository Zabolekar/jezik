from typing import NamedTuple, List, Union
from ..paradigm_helpers import AccentedTuple

class ShortAdj(NamedTuple):
   m_sg_nom: List[AccentedTuple] # len 1
   f_sg_nom: List[AccentedTuple] # 1
   n_sg_nom: List[AccentedTuple] # 1
   m_pl_nom: List[AccentedTuple] # 1
   f_pl_nom: List[AccentedTuple] # 1
   n_pl_nom: List[AccentedTuple] # 1
   m_pl_acc: List[AccentedTuple] # 1
   f_pl_acc: List[AccentedTuple] # 1; = f_pl_nom
   n_pl_acc: List[AccentedTuple] # 1; = n_pl_nom
   m_sg_gen: List[AccentedTuple] # 1
   m_sg_dat: List[AccentedTuple] # 1
   m_sg_loc: List[AccentedTuple] # 1
   f_sg_acc: List[AccentedTuple] # 1
   n_sg_acc: List[AccentedTuple] # 1; = n_sg_nom
   n_sg_gen: List[AccentedTuple] # 1; = m_sg_gen
   n_sg_dat: List[AccentedTuple] # 1; = m_sg_dat
   n_sg_loc: List[AccentedTuple] # 1; = m_sg_dat
   m_sg_acc_in: List[AccentedTuple] #; 1 = m_sg_nom
   m_sg_acc_an: List[AccentedTuple] #; 1 = m_sg_gen

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
   m_sg_nom: List[AccentedTuple] # len 1
   m_sg_gen: List[AccentedTuple] # ! len 2
   m_sg_dat: List[AccentedTuple] # ! len 3
   m_sg_ins: List[AccentedTuple] # 1
   m_sg_loc: List[AccentedTuple] # ! 3
   m_sg_acc_an: List[AccentedTuple] # ! 2; = m_sg_gen
   m_sg_acc_in: List[AccentedTuple] # 1; = m_sg_nom
   f_sg_nom: List[AccentedTuple] # 1
   f_sg_gen: List[AccentedTuple] # 1
   f_sg_dat: List[AccentedTuple] # 1
   f_sg_acc: List[AccentedTuple] # 1
   f_sg_ins: List[AccentedTuple] # 1
   f_sg_loc: List[AccentedTuple] # 1
   n_sg_nom: List[AccentedTuple] # 1
   n_sg_gen: List[AccentedTuple] # ! 2; = m_sg_gen
   n_sg_dat: List[AccentedTuple] # ! 3; = m_sg_dat
   n_sg_acc: List[AccentedTuple] # 1; = n_sg_nom
   n_sg_ins: List[AccentedTuple] # 1; = m_sg_ins
   n_sg_loc: List[AccentedTuple] # ! 3; = m_sg_loc
   m_pl_nom: List[AccentedTuple] # 1
   f_pl_nom: List[AccentedTuple] # 1
   n_pl_nom: List[AccentedTuple] # 1
   m_pl_acc: List[AccentedTuple] # 1
   f_pl_acc: List[AccentedTuple] # 1; = f_pl_nom
   n_pl_acc: List[AccentedTuple] # 1; = n_pl_nom
   pl_gen: List[AccentedTuple] # 1
   pl_rest: List[AccentedTuple] # ! 2

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

mixed_adj = LongAdj(
  m_sg_nom = short_adj.m_sg_nom,
  m_sg_gen = short_adj.m_sg_gen + long_adj.m_sg_gen,
  m_sg_dat = short_adj.m_sg_dat + long_adj.m_sg_dat,
  m_sg_ins = long_adj.m_sg_ins,
  m_sg_loc = short_adj.m_sg_loc + long_adj.m_sg_loc,
  m_sg_acc_in = short_adj.m_sg_acc_in,
  m_sg_acc_an = short_adj.m_sg_acc_an + long_adj.m_sg_acc_an,
  f_sg_nom = short_adj.f_sg_nom,
  f_sg_gen = long_adj.f_sg_gen,
  f_sg_dat = long_adj.f_sg_dat,
  f_sg_acc = short_adj.m_sg_nom,
  f_sg_ins = long_adj.f_sg_ins,
  f_sg_loc = long_adj.f_sg_loc,
  n_sg_nom = short_adj.n_sg_nom,
  n_sg_gen = short_adj.n_sg_gen + long_adj.n_sg_gen,
  n_sg_dat = short_adj.n_sg_dat + long_adj.n_sg_dat,
  n_sg_acc = short_adj.n_sg_acc,
  n_sg_ins = long_adj.n_sg_ins,
  n_sg_loc = short_adj.n_sg_loc + long_adj.n_sg_loc,
  m_pl_nom = short_adj.m_pl_nom,
  f_pl_nom = short_adj.f_pl_nom,
  n_pl_nom = short_adj.n_pl_nom,
  m_pl_acc = short_adj.m_pl_acc,
  f_pl_acc = short_adj.f_pl_acc,
  n_pl_acc = short_adj.n_pl_acc,
  pl_gen = long_adj.pl_gen,
  pl_rest = long_adj.pl_rest)

AdjParadigm = Union[ShortAdj, LongAdj]
