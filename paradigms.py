from typing import Dict, Iterator, NamedTuple, List, Optional, Tuple, Union
from .utils import insert, all_vowels

# TODO: when 3.7 is out, make Accents and GramInfo dataclasses

class Accents:

   def __init__(self, r: Dict[int, str], v: Dict[int, str]) -> None:
      self.r = r # syllabic r
      self.v = v # any other vowel

   def accentize(self, word: str) -> str: # traditional accentuation
      real_accent = {'`': '\u0300', '´': '\u0301', '¨': '\u030f', '^': '\u0311', '_': '\u0304', '!': '!'}
      if self.v:
         if self.r: # now we put the magic ring
            word = insert(word, self.r)
         # after that we create a dict with letter numbers representing vowels
         syllabic = 0
         position_to_accent: Dict[int, str] = {}
         for i, letter in enumerate(word):
            if letter in all_vowels:
               syllabic += 1
               if syllabic in self.v:
                  position_to_accent[i+1] = real_accent[self.v[syllabic]]
         return insert(word, position_to_accent) # then we insert accents into word!
      else:
         return word

class GramInfo:
   """
   How to read the field `other`:
   - If the word is a verb, then `other` contains a list with two elements,
   one of "Tr", "Itr", "Refl" (which means transitive, intransitive,
   reflexive) and one of "Pf", "Ipf", "Dv" (perfective, imperfective,
   biaspectual; abbreviation "Dv" comes from "dvòvīdan")
   """
   def __init__(self, infos: List[str], types: str) -> None:
      Rs: Optional[str] # circles below syllabic r's
      Vs: str # accents above vowels AND above circles (see Rs)
      accents = []
      self.AP: List[str] = []
      for inf in infos:
         if inf:
            print(inf)
            line_accents, AP, MP = inf.split('|')
            if '@' in inf:
               Rs, Vs = line_accents.split('@')
            else:
               Rs, Vs = None, line_accents
            accents.append(Accents(
                {int(i): '\u0325' for i in Rs[1:].split(',')} if Rs else {},
                {int(i[:-1]): i[-1] for i in Vs.split(',')} if line_accents else {}
            )              )
            self.AP.append(AP) # accent paradigm
         else:
            raise ValueError("Can't decipher empty i")

      if types:
         POS, *other = types.split('|')
      else:
         raise ValueError("Can't decipher empty t")

      self.accents: List[Accents] = accents
      
      self.MP: str = MP # morphological paradigm
      self.POS: str = POS # part of speech
      self.other: List[str] = other

class AccentedTuple(NamedTuple):
   morpheme: str
   accent: str

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

class VerbEnding(NamedTuple):
   theme: AccentedTuple
   ending: AccentedTuple

LabeledEnding = Tuple[NamedTuple, NamedTuple]

class Present(List[NamedTuple]):
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
      yield from zip(self._fields, super().__iter__())

class Past(List[NamedTuple]):
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
      yield from zip(self._fields, super().__iter__())

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
