from typing import Dict, NamedTuple, List

class Accents(NamedTuple):
   r: Dict[int, str] # syllabic r
   v: Dict[int, str] # any other vowel

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

class Ending(NamedTuple):
   theme: AccentedTuple
   ending: AccentedTuple

class Present(NamedTuple):
   prs1sg: Ending
   prs2sg: Ending
   prs3sg: Ending
   prs1pl: Ending
   prs2pl: Ending
   prs3pl: Ending
   imv2sg: Ending
   imv1pl: Ending
   imv2pl: Ending

class Past(NamedTuple):
   pfMsg: Ending
   pfFsg: Ending
   pfNsg: Ending
   pfMpl: Ending
   pfFpl: Ending
   pfnNpl: Ending
   aor1sg: Ending
   aor2sg: Ending
   aor3sg: Ending
   aor1pl: Ending
   aor2pl: Ending
   aor3pl: Ending
   infinitive: Ending
   ipf1sg: Ending
   ipf2sg: Ending
   ipf3sg: Ending
   ipf1pl: Ending
   ipf2pl: Ending
   ipf3pl: Ending

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
   Ending(i_theme_past, AccentedTuple('о', '')),
   Ending(i_theme_past, AccentedTuple('ла', '')),
   Ending(i_theme_past, AccentedTuple('ло', '')),
   Ending(i_theme_past, AccentedTuple('ли', '')),
   Ending(i_theme_past, AccentedTuple('ле', '')),
   Ending(i_theme_past, AccentedTuple('ла', '')),
   Ending(i_theme_past, ending_x),
   Ending(AccentedTuple('и·', 'c#'), AccentedTuple('0·~', 'ab.b:c.c:')),
   Ending(AccentedTuple('и·', 'c#'), AccentedTuple('0·~', 'ab.b:c.c:')),
   Ending(i_theme_past, ending_smo),
   Ending(i_theme_past, ending_ste),
   Ending(i_theme_past, ending_she),
   Ending(i_theme_past, ending_ti),
   Ending(i_theme_ipf, ending_x),
   Ending(i_theme_ipf, ending_she),
   Ending(i_theme_ipf, ending_she),
   Ending(i_theme_ipf, ending_smo),
   Ending(i_theme_ipf, ending_ste),
   Ending(i_theme_ipf, ending_xu)
)

a_past = Past(
   Ending(a_theme_past, AccentedTuple('о0·', 'x.')),
   Ending(a_theme_past, AccentedTuple('ла0·', 'x.')),
   Ending(a_theme_past, AccentedTuple('ло0·', 'x.')),
   Ending(a_theme_past, AccentedTuple('ли0·', 'x.')),
   Ending(a_theme_past, AccentedTuple('ле0·', 'x.')),
   Ending(a_theme_past, AccentedTuple('ла0·', 'x.')),
   Ending(a_theme_past, ending_x),
   Ending(AccentedTuple('а', 'c#cty:d.'), AccentedTuple('0·~', 'ax.z.b:c.')),
   Ending(AccentedTuple('а', 'c#cty:d.'), AccentedTuple('0·~', 'ax.z.b:c.')),
   Ending(a_theme_past, ending_smo),
   Ending(a_theme_past, ending_ste),
   Ending(a_theme_past, ending_she),
   Ending(a_theme_past, ending_ti),
   Ending(a_theme_ipf, ending_x),
   Ending(a_theme_ipf, ending_she),
   Ending(a_theme_ipf, ending_she),
   Ending(a_theme_ipf, ending_smo),
   Ending(a_theme_ipf, ending_smo),
   Ending(a_theme_ipf, ending_xu)
)

ie_past = Past(
   Ending(ie_theme_past, AccentedTuple('о', '')),
   Ending(ie_theme_past, AccentedTuple('ла', '')),
   Ending(ie_theme_past, AccentedTuple('ло', '')),
   Ending(ie_theme_past, AccentedTuple('ли', '')),
   Ending(ie_theme_past, AccentedTuple('ле', '')),
   Ending(ie_theme_past, AccentedTuple('ла', '')),
   Ending(ie_theme_past, ending_x),
   Ending(ie_theme_past, ending_null),
   Ending(ie_theme_past, ending_null),
   Ending(ie_theme_past, ending_smo),
   Ending(ie_theme_past, ending_ste),
   Ending(ie_theme_past, ending_she),
   Ending(ie_theme_past, ending_ti),
   Ending(ie_theme_ipf, ending_x),
   Ending(ie_theme_ipf, ending_she),
   Ending(ie_theme_ipf, ending_she),
   Ending(ie_theme_ipf, ending_smo),
   Ending(ie_theme_ipf, ending_ste),
   Ending(ie_theme_ipf, ending_xu)
)

ova_past = Past(
   Ending(AccentedTuple('ова~', ''), AccentedTuple('о0·', 'cp')),
   Ending(AccentedTuple('ова~', ''), AccentedTuple('ла0·', 'cp')),
   Ending(AccentedTuple('ова~', ''), AccentedTuple('ло0·', 'cp')),
   Ending(AccentedTuple('ова~', ''), AccentedTuple('ли0·', 'cp')),
   Ending(AccentedTuple('ова~', ''), AccentedTuple('ле0·', 'cp')),
   Ending(AccentedTuple('ова~', ''), AccentedTuple('ла0·', 'cp')),
   Ending(ova_theme_past, ending_x),
   Ending(AccentedTuple('ова', ''), AccentedTuple('0·~', 'acp')),
   Ending(AccentedTuple('ова', ''), AccentedTuple('0·~', 'acp')),
   Ending(ova_theme_past, ending_smo),
   Ending(ova_theme_past, ending_ste),
   Ending(ova_theme_past, ending_she),
   Ending(ova_theme_past, ending_ti),
   Ending(ova_theme_ipf, ending_x),
   Ending(ova_theme_ipf, ending_she),
   Ending(ova_theme_ipf, ending_she),
   Ending(ova_theme_ipf, ending_smo),
   Ending(ova_theme_ipf, ending_ste),
   Ending(ova_theme_ipf, ending_xu)
)

iva_past = Past(
   Ending(iva_theme_past, AccentedTuple('о', '')),
   Ending(iva_theme_past, AccentedTuple('ла', '')),
   Ending(iva_theme_past, AccentedTuple('ло', '')),
   Ending(iva_theme_past, AccentedTuple('ли', '')),
   Ending(iva_theme_past, AccentedTuple('ле', '')),
   Ending(iva_theme_past, AccentedTuple('ла', '')),
   Ending(iva_theme_past, ending_x),
   Ending(iva_theme_past, AccentedTuple('·', 'ct')),
   Ending(iva_theme_past, AccentedTuple('·', 'ct')),
   Ending(iva_theme_past, ending_smo),
   Ending(iva_theme_past, ending_ste),
   Ending(iva_theme_past, ending_she),
   Ending(iva_theme_past, ending_ti),
   Ending(iva_theme_ipf, ending_x),
   Ending(iva_theme_ipf, ending_she),
   Ending(iva_theme_ipf, ending_she),
   Ending(iva_theme_ipf, ending_smo),
   Ending(iva_theme_ipf, ending_ste),
   Ending(iva_theme_ipf, ending_xu)
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
   Ending(i_theme_prs, ending_m),
   Ending(i_theme_prs, ending_sh),
   Ending(i_theme_prs, ending_null),
   Ending(AccentedTuple('и·\u0304', 'c.c:'), AccentedTuple('мо', 'c#')),
   Ending(AccentedTuple('и·\u0304', 'c.c:'), AccentedTuple('те', 'c#')),
   Ending(AccentedTuple('е·\u0304', 'c.c:c#'), ending_null),
   Ending(i_theme_imv, ending_null),
   Ending(i_theme_imv, ending_mo),
   Ending(i_theme_imv, ending_te)
)

je_present = Present(
   Ending(je_theme_prs, ending_m),
   Ending(je_theme_prs, ending_sh),
   Ending(je_theme_prs, ending_null),
   Ending(AccentedTuple('\u0237е·\u0304', ''), AccentedTuple('мо', 'y#')),
   Ending(AccentedTuple('\u0237е·\u0304', ''), AccentedTuple('те', 'y#')),
   Ending(AccentedTuple('\u0237у·\u0304', 'y#'), ending_null),
   Ending(je_theme_imv, ending_null),
   Ending(je_theme_imv, ending_mo),
   Ending(je_theme_imv, ending_te)
)

a_present = Present(
   Ending(a_theme_prs, ending_m),
   Ending(a_theme_prs, ending_sh),
   Ending(a_theme_prs, ending_null),
   Ending(AccentedTuple('а·\u0304', 'c.cp'), AccentedTuple('мо', 'c#')),
   Ending(AccentedTuple('а·\u0304', 'c.cp'), AccentedTuple('те', 'c#')),
   Ending(AccentedTuple('а·ју\u0304', 'b:d.с.c#cp'), ending_null),
   Ending(a_theme_imv, ending_null),
   Ending(a_theme_imv, ending_mo),
   Ending(a_theme_imv, ending_te)
)

uje_present = Present(
   Ending(uje_theme_prs, ending_m),
   Ending(uje_theme_prs, ending_sh),
   Ending(uje_theme_prs, ending_null),
   Ending(uje_theme_prs, ending_mo),
   Ending(uje_theme_prs, ending_te),
   Ending(AccentedTuple('у·ју\u0304', 'cpct'), ending_null),
   Ending(uje_theme_imv, ending_null),
   Ending(uje_theme_imv, ending_mo),
   Ending(uje_theme_imv, ending_te)
)

MP_to_stems: Dict[str, Stems] = dict(
   alpha=Stems(i_present, i_past),
   beta=Stems(a_present, a_past),
   delta=Stems(je_present, a_past),
   epsilon=Stems(uje_present, ova_past),
   zeta=Stems(uje_present, iva_past),
   eta=Stems(i_present, ie_past),
)
