from typing import Dict, NamedTuple, List
from .utils import insert

# TODO: when 3.7 is out, make Accents and GramInfo dataclasses

class Accents:

   def __init__(self, r, v: Dict[int, str]) -> None:
      self.r = r # syllabic r
      self.v = v # any other vowel

   def accentize(self, word: str) -> str: # traditional accentuation
      real_accent = {'`': '\u0300', '´': '\u0301', '¨': '\u030f', '^': '\u0311', '_': '\u0304'}
      if self.v:
         if self.r: # now we put the magic ring
            word = insert(word, self.r)
         # after that we create a dict with letter numbers representing vowels
         syllabic = 0
         position_to_accent: Dict[int, str] = {}
         for i, letter in enumerate(word):
            if letter in 'aeiouAEIOUаеиоуАЕИОУ\u0325':
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
   def __init__(self, infos, types: str) -> None:
      if infos:
         line_accents, AP, MP = infos.split('|')
         if '@' in infos:
            Rs, Vs = line_accents.split('@')
         else:
            Rs, Vs = None, line_accents
         accents = Accents(
             {int(i): '\u0325' for i in Rs[1:].split(',')} if Rs else {},
             {int(i[:-1]): i[-1] for i in Vs.split(',')} if line_accents else {}
         )
      else:
         raise ValueError("Can't decipher empty i")

      if types:
         POS, *other = types.split('|')
      else:
         raise ValueError("Can't decipher empty t")

      self.accents: Accents = accents
      self.AP: str = AP # accent paradigm
      self.MP: str = MP # morphological paradigm
      self.POS: str = POS # part of speech
      self.other: List[str] = other

class AccentedTuple(NamedTuple):
   morpheme: str
   accent: str

class ShortAdj(NamedTuple):
   m_sg_nom: [AccentedTuple('ø·', 'b.b:')] # len 1; ø means 'zero ending' (which, however, can take stress, in a way)
   f_sg_nom: [AccentedTuple('а·', 'b.b:')] # 1
   n_sg_nom: [AccentedTuple('œ·', 'b.b:')] # 1
   m_pl_nom: [AccentedTuple('и·', 'b.b:')] # 1
   f_pl_nom: [AccentedTuple('е·', 'b.b:')] # 1
   n_pl_nom: [AccentedTuple('а·', 'b.b:')] # 1
   m_pl_acc: [AccentedTuple('е·', 'b.b:')] # 1
   f_pl_acc: [AccentedTuple('е·', 'b.b:')] # 1; = f_pl_nom 
   n_pl_acc: [AccentedTuple('а·', 'b.b:')] # 1; = n_pl_nom
   m_sg_gen: [AccentedTuple('а·', 'b.b:')] # 1
   m_sg_dat: [AccentedTuple('у·', 'b.b:')] # 1
   m_sg_loc: [AccentedTuple('у·', 'b.b:')] # 1
   f_sg_acc: [AccentedTuple('у·', 'b.b:')] # 1
   n_sg_acc: [AccentedTuple('œ·', 'b.b:')] # 1; = n_sg_nom
   n_sg_gen: [AccentedTuple('а·', 'b.b:')] # 1; = m_sg_gen
   n_sg_dat: [AccentedTuple('у·', 'b.b:')] # 1; = m_sg_dat
   n_sg_loc: [AccentedTuple('у·', 'b.b:')] # 1; = m_sg_dat
   m_sg_acc_in: [AccentedTuple('ø·', 'b.b:')] #; 1 = m_sg_nom 
   m_sg_acc_an: [AccentedTuple('а·', 'b.b:')] #; 1 = m_sg_gen
   
class LongAdj(NamedTuple):
  m_sg_nom: [AccentedTuple('и_·', 'c.c:')] # len 1
  m_sg_gen: [AccentedTuple('œ_·г', 'c.c:'), AccentedTuple('œ_·га', 'c.c:')] # ! len 2
  m_sg_dat: [AccentedTuple('œ_·м', 'c.c:'), AccentedTuple('œ_·ме', 'c.c:'), AccentedTuple('œ_·му', 'c.c:')] # ! len 3
  m_sg_ins: [AccentedTuple('и_·м', 'c.c:')] # 1
  m_sg_loc: [AccentedTuple('œ_·м', 'c.c:'), AccentedTuple('œ_·ме', 'c.c:'), AccentedTuple('œ_·му', 'c.c:')] # ! 3
  m_sg_acc_an: [AccentedTuple('œ_·г', 'c.c:'), AccentedTuple('œ_·га', 'c.c:')] # ! 2; = m_sg_gen
  m_sg_acc_in: [AccentedTuple('и_·', 'c.c:')] # 1; = m_sg_nom
  f_sg_nom: [AccentedTuple('а_·', 'c.c:')] # 1
  f_sg_gen: [AccentedTuple('е_·', 'c.c:')] # 1
  f_sg_dat: [AccentedTuple('о_·ј', 'c.c:')] # 1
  f_sg_acc: [AccentedTuple('у_·', 'c.c:')] # 1
  f_sg_ins: [AccentedTuple('о_·м', 'c.c:')] # 1
  f_sg_loc: [AccentedTuple('о_·ј', 'c.c:')] # 1
  n_sg_nom: [AccentedTuple('œ_·', 'c.c:')] # 1
  n_sg_gen: [AccentedTuple('œ_·г', 'c.c:'), AccentedTuple('œ_·га', 'c.c:')] # ! 2; = m_sg_gen
  n_sg_dat: [AccentedTuple('œ_·м', 'c.c:'), AccentedTuple('œ_·ме', 'c.c:'), AccentedTuple('œ_·му', 'c.c:')] # ! 3; = m_sg_dat
  n_sg_acc: [AccentedTuple('œ_·', 'c.c:')] # 1; = n_sg_nom
  n_sg_ins: [AccentedTuple('и_·м', 'c.c:')] # 1; = m_sg_ins
  n_sg_loc: [AccentedTuple('œ_·м', 'c.c:'), AccentedTuple('œ_·ме', 'c.c:'), AccentedTuple('œ_·му', 'c.c:')] # ! 3; = m_sg_loc
  m_pl_nom: [AccentedTuple('и_·', 'c.c:')] # 1
  f_pl_nom: [AccentedTuple('е_·', 'c.c:')] # 1
  n_pl_nom: [AccentedTuple('а_·', 'c.c:')] # 1
  m_pl_acc: [AccentedTuple('е_·', 'c.c:')] # 1
  f_pl_acc: [AccentedTuple('е_·', 'c.c:')] # 1; = f_pl_nom
  n_pl_acc: [AccentedTuple('а_·', 'c.c:')] # 1; = n_pl_nom
  pl_gen: [AccentedTuple('и_·х', 'c.c:')] # 1
  pl_rest: [AccentedTuple('и_·м', 'c.c:'), AccentedTuple('и_·ма', 'c.c:')] # ! 2
  
class OvAdj(NamedTuple):
  m_sg_nom = ShortAdj.m_sg_nom
  m_sg_gen = ShortAdj.m_sg_gen + LongAdj.m_sg_gen
  m_sg_dat = ShortAdj.m_sg_dat + LongAdj.m_sg_dat
  m_sg_ins = LongAdj.m_sg_ins
  m_sg_loc = ShortAdj.m_sg_loc + LongAdj.m_sg_loc
  m_sg_acc_in = ShortAdj.m_sg_acc_in
  m_sg_acc_an = ShortAdj.m_sg_acc_an + LongAdj.m_sg_acc_an
  f_sg_nom = ShortAdj.f_sg_nom
  f_sg_gen = LongAdj.f_sg_gen
  f_sg_dat = LongAdj.f_sg_dat
  f_sg_acc = ShortAdj.m_sg_nom
  f_sg_ins = LongAdj.f_sg_ins
  f_sg_loc = LongAdj.f_sg_loc
  n_sg_nom = ShortAdj.n_sg_nom
  n_sg_gen = ShortAdj.n_sg_gen + LongAdj.n_sg_gen # = m_sg_gen
  n_sg_dat = ShortAdj.n_sg_dat + LongAdj.n_sg_dat # = m_sg_dat
  n_sg_acc = ShortAdj.n_sg_acc # = n_sg_nom
  n_sg_ins = LongAdj.n_sg_ins # = m_sg_ins
  n_sg_loc = ShortAdj.n_sg_loc + LongAdj.n_sg_loc # = m_sg_loc
  m_pl_nom = ShortAdj.m_pl_nom
  f_pl_nom = ShortAdj.f_pl_nom
  n_pl_nom = ShortAdj.n_pl_nom
  m_pl_acc = ShortAdj.m_pl_acc
  f_pl_acc = ShortAdj.f_pl_acc
  n_pl_acc = ShortAdj.n_pl_acc # = n_pl_nom
  pl_gen = LongAdj.pl_gen
  pl_rest = longAdj.pl_rest
  
   
class VerbEnding(NamedTuple):
   theme: AccentedTuple
   ending: AccentedTuple

class Present(NamedTuple):
   prs1sg: VerbEnding
   prs2sg: VerbEnding
   prs3sg: VerbEnding
   prs1pl: VerbEnding
   prs2pl: VerbEnding
   prs3pl: VerbEnding
   imv2sg: VerbEnding
   imv1pl: VerbEnding
   imv2pl: VerbEnding

class Past(NamedTuple):
   pfMsg: VerbEnding
   pfFsg: VerbEnding
   pfNsg: VerbEnding
   pfMpl: VerbEnding
   pfFpl: VerbEnding
   pfnNpl: VerbEnding
   aor1sg: VerbEnding
   aor2sg: VerbEnding
   aor3sg: VerbEnding
   aor1pl: VerbEnding
   aor2pl: VerbEnding
   aor3pl: VerbEnding
   infinitive: VerbEnding
   ipf1sg: VerbEnding
   ipf2sg: VerbEnding
   ipf3sg: VerbEnding
   ipf1pl: VerbEnding
   ipf2pl: VerbEnding
   ipf3pl: VerbEnding

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

i_theme_past = AccentedTuple('и·', 'b.b:c.c:c#')
a_theme_past = AccentedTuple('а·~', 'b.b:c.c:c#cjctx.y.y:y#z.')
ie_theme_past = AccentedTuple('е·', 'b.c.c:')
#zero_theme_past = AccentedTuple('', '')
#nu_theme_past = AccentedTuple('ну', '') # TODO: finish the book first!
ova_theme_past = AccentedTuple('ова·', 'cp')
iva_theme_past = AccentedTuple('и\u0304ва·', 'ct')

i_theme_ipf = AccentedTuple('ȷа\u0304·', 'c.c:c#')
ie_theme_ipf = AccentedTuple('ȷа\u0304·', 'c.c:')
a_theme_ipf = AccentedTuple('а\u0304·', 'c.cpc#y#')
ova_theme_ipf = AccentedTuple('о·ва\u0304', 'cp')
iva_theme_ipf = AccentedTuple('и\u0304·ва\u0304', 'ct')

ending_null = AccentedTuple('', '')
ending_x = AccentedTuple('х', '')
ending_she = AccentedTuple('ше', '')
ending_smo = AccentedTuple('смо', '')
ending_ste = AccentedTuple('сте', '')
ending_xu = AccentedTuple('ху', '')
ending_ti = AccentedTuple('ти', '')

i_past = Past(
   VerbEnding(i_theme_past, AccentedTuple('ʌ', '')),
   VerbEnding(i_theme_past, AccentedTuple('ла', '')),
   VerbEnding(i_theme_past, AccentedTuple('ло', '')),
   VerbEnding(i_theme_past, AccentedTuple('ли', '')),
   VerbEnding(i_theme_past, AccentedTuple('ле', '')),
   VerbEnding(i_theme_past, AccentedTuple('ла', '')),
   VerbEnding(i_theme_past, ending_x),
   VerbEnding(AccentedTuple('и·', 'c#'), AccentedTuple('0·~', 'ab.b:c.c:')),
   VerbEnding(AccentedTuple('и·', 'c#'), AccentedTuple('0·~', 'ab.b:c.c:')),
   VerbEnding(i_theme_past, ending_smo),
   VerbEnding(i_theme_past, ending_ste),
   VerbEnding(i_theme_past, ending_she),
   VerbEnding(i_theme_past, ending_ti),
   VerbEnding(i_theme_ipf, ending_x),
   VerbEnding(i_theme_ipf, ending_she),
   VerbEnding(i_theme_ipf, ending_she),
   VerbEnding(i_theme_ipf, ending_smo),
   VerbEnding(i_theme_ipf, ending_ste),
   VerbEnding(i_theme_ipf, ending_xu)
)

a_past = Past(
   VerbEnding(a_theme_past, AccentedTuple('ʌ0·', 'x.')),
   VerbEnding(a_theme_past, AccentedTuple('ла0·', 'x.')),
   VerbEnding(a_theme_past, AccentedTuple('ло0·', 'x.')),
   VerbEnding(a_theme_past, AccentedTuple('ли0·', 'x.')),
   VerbEnding(a_theme_past, AccentedTuple('ле0·', 'x.')),
   VerbEnding(a_theme_past, AccentedTuple('ла0·', 'x.')),
   VerbEnding(a_theme_past, ending_x),
   VerbEnding(AccentedTuple('а', 'c#cty:d.'), AccentedTuple('0·~', 'ax.z.b:c.')),
   VerbEnding(AccentedTuple('а', 'c#cty:d.'), AccentedTuple('0·~', 'ax.z.b:c.')),
   VerbEnding(a_theme_past, ending_smo),
   VerbEnding(a_theme_past, ending_ste),
   VerbEnding(a_theme_past, ending_she),
   VerbEnding(a_theme_past, ending_ti),
   VerbEnding(a_theme_ipf, ending_x),
   VerbEnding(a_theme_ipf, ending_she),
   VerbEnding(a_theme_ipf, ending_she),
   VerbEnding(a_theme_ipf, ending_smo),
   VerbEnding(a_theme_ipf, ending_smo),
   VerbEnding(a_theme_ipf, ending_xu)
)

ie_past = Past(
   VerbEnding(ie_theme_past, AccentedTuple('ʌ', '')),
   VerbEnding(ie_theme_past, AccentedTuple('ла', '')),
   VerbEnding(ie_theme_past, AccentedTuple('ло', '')),
   VerbEnding(ie_theme_past, AccentedTuple('ли', '')),
   VerbEnding(ie_theme_past, AccentedTuple('ле', '')),
   VerbEnding(ie_theme_past, AccentedTuple('ла', '')),
   VerbEnding(ie_theme_past, ending_x),
   VerbEnding(ie_theme_past, ending_null),
   VerbEnding(ie_theme_past, ending_null),
   VerbEnding(ie_theme_past, ending_smo),
   VerbEnding(ie_theme_past, ending_ste),
   VerbEnding(ie_theme_past, ending_she),
   VerbEnding(ie_theme_past, ending_ti),
   VerbEnding(ie_theme_ipf, ending_x),
   VerbEnding(ie_theme_ipf, ending_she),
   VerbEnding(ie_theme_ipf, ending_she),
   VerbEnding(ie_theme_ipf, ending_smo),
   VerbEnding(ie_theme_ipf, ending_ste),
   VerbEnding(ie_theme_ipf, ending_xu)
)

ova_past = Past(
   VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ʌ0·', 'cp')),
   VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ла0·', 'cp')),
   VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ло0·', 'cp')),
   VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ли0·', 'cp')),
   VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ле0·', 'cp')),
   VerbEnding(AccentedTuple('ова~', ''), AccentedTuple('ла0·', 'cp')),
   VerbEnding(ova_theme_past, ending_x),
   VerbEnding(AccentedTuple('ова', ''), AccentedTuple('0·~', 'acp')),
   VerbEnding(AccentedTuple('ова', ''), AccentedTuple('0·~', 'acp')),
   VerbEnding(ova_theme_past, ending_smo),
   VerbEnding(ova_theme_past, ending_ste),
   VerbEnding(ova_theme_past, ending_she),
   VerbEnding(ova_theme_past, ending_ti),
   VerbEnding(ova_theme_ipf, ending_x),
   VerbEnding(ova_theme_ipf, ending_she),
   VerbEnding(ova_theme_ipf, ending_she),
   VerbEnding(ova_theme_ipf, ending_smo),
   VerbEnding(ova_theme_ipf, ending_ste),
   VerbEnding(ova_theme_ipf, ending_xu)
)

iva_past = Past(
   VerbEnding(iva_theme_past, AccentedTuple('ʌ', '')),
   VerbEnding(iva_theme_past, AccentedTuple('ла', '')),
   VerbEnding(iva_theme_past, AccentedTuple('ло', '')),
   VerbEnding(iva_theme_past, AccentedTuple('ли', '')),
   VerbEnding(iva_theme_past, AccentedTuple('ле', '')),
   VerbEnding(iva_theme_past, AccentedTuple('ла', '')),
   VerbEnding(iva_theme_past, ending_x),
   VerbEnding(iva_theme_past, AccentedTuple('·', 'ct')),
   VerbEnding(iva_theme_past, AccentedTuple('·', 'ct')),
   VerbEnding(iva_theme_past, ending_smo),
   VerbEnding(iva_theme_past, ending_ste),
   VerbEnding(iva_theme_past, ending_she),
   VerbEnding(iva_theme_past, ending_ti),
   VerbEnding(iva_theme_ipf, ending_x),
   VerbEnding(iva_theme_ipf, ending_she),
   VerbEnding(iva_theme_ipf, ending_she),
   VerbEnding(iva_theme_ipf, ending_smo),
   VerbEnding(iva_theme_ipf, ending_ste),
   VerbEnding(iva_theme_ipf, ending_xu)
)

#("e", Present),   — todo later
#("ie", Present), — todo later
#("ne", Present) — todo after finishing the book

i_theme_prs = AccentedTuple('и·\u0304', 'c.c:c#')
je_theme_prs = AccentedTuple('\u0237е·\u0304', 'y#')
a_theme_prs = AccentedTuple('а·\u0304', 'c.cpc#')
uje_theme_prs = AccentedTuple('у·је\u0304', 'cpct')

i_theme_imv = AccentedTuple('й·', 'b.b:c.c:c#')
je_theme_imv = AccentedTuple('\u0237й·', 'x.y.y#y:z.')
a_theme_imv = AccentedTuple('а·\u0304ј', 'с.cpc#')
uje_theme_imv = AccentedTuple('у·\u0304ј', 'cpct')

ending_mo = AccentedTuple('мо', '')
ending_te = AccentedTuple('те', '')
ending_m = AccentedTuple('м', '')
ending_sh = AccentedTuple('ш', '')

i_present = Present(
   VerbEnding(i_theme_prs, ending_m),
   VerbEnding(i_theme_prs, ending_sh),
   VerbEnding(i_theme_prs, ending_null),
   VerbEnding(AccentedTuple('и·\u0304', 'c.c:'), AccentedTuple('мо', 'c#')),
   VerbEnding(AccentedTuple('и·\u0304', 'c.c:'), AccentedTuple('те', 'c#')),
   VerbEnding(AccentedTuple('е·\u0304', 'c.c:c#'), ending_null),
   VerbEnding(i_theme_imv, ending_null),
   VerbEnding(i_theme_imv, ending_mo),
   VerbEnding(i_theme_imv, ending_te)
)

je_present = Present(
   VerbEnding(je_theme_prs, ending_m),
   VerbEnding(je_theme_prs, ending_sh),
   VerbEnding(je_theme_prs, ending_null),
   VerbEnding(AccentedTuple('\u0237е·\u0304', ''), AccentedTuple('мо', 'y#')),
   VerbEnding(AccentedTuple('\u0237е·\u0304', ''), AccentedTuple('те', 'y#')),
   VerbEnding(AccentedTuple('\u0237у·\u0304', 'y#'), ending_null),
   VerbEnding(je_theme_imv, ending_null),
   VerbEnding(je_theme_imv, ending_mo),
   VerbEnding(je_theme_imv, ending_te)
)

a_present = Present(
   VerbEnding(a_theme_prs, ending_m),
   VerbEnding(a_theme_prs, ending_sh),
   VerbEnding(a_theme_prs, ending_null),
   VerbEnding(AccentedTuple('а·\u0304', 'c.cp'), AccentedTuple('мо', 'c#')),
   VerbEnding(AccentedTuple('а·\u0304', 'c.cp'), AccentedTuple('те', 'c#')),
   VerbEnding(AccentedTuple('а·ју\u0304', 'b:d.с.c#cp'), ending_null),
   VerbEnding(a_theme_imv, ending_null),
   VerbEnding(a_theme_imv, ending_mo),
   VerbEnding(a_theme_imv, ending_te)
)

uje_present = Present(
   VerbEnding(uje_theme_prs, ending_m),
   VerbEnding(uje_theme_prs, ending_sh),
   VerbEnding(uje_theme_prs, ending_null),
   VerbEnding(uje_theme_prs, ending_mo),
   VerbEnding(uje_theme_prs, ending_te),
   VerbEnding(AccentedTuple('у·ју\u0304', 'cpct'), ending_null),
   VerbEnding(uje_theme_imv, ending_null),
   VerbEnding(uje_theme_imv, ending_mo),
   VerbEnding(uje_theme_imv, ending_te)
)

MP_to_verb_stems: Dict[str, Stems] = dict(
   alpha=Stems(i_present, i_past),
   beta=Stems(a_present, a_past),
   delta=Stems(je_present, a_past),
   epsilon=Stems(uje_present, ova_past),
   zeta=Stems(uje_present, iva_past),
   eta=Stems(i_present, ie_past),
)
