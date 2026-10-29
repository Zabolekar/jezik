import pytest # type: ignore

from ..entries import make_entry
from ...lookup.utils import expose as expose_module
from ...lookup import pos
from ...lookup.adjective import Adjective
from ...lookup.noun import Noun
from ...lookup.verb import Verb


def _words():
   zub = Noun("зуб", make_entry("зу^б", "N\\m", "c$", amendments=(("pl gen", ["зу´би_"]),)))
   mogti = Verb("могти", make_entry("мо`гˌти", "V\\Itr\\Ipf", "eʹ/kappa3",
      amendments=(("prs 2 sg", ["мо¨жеш"]),)
   ))
   dobar = Adjective("добар", make_entry("до¨бар", "A\\all", "A.",
      amendments=(("m sg nom short", ["до¨бри_"]),)
   ))
   return {"noun": zub, "verb": mogti, "adjective": dobar}

_label = {"noun": "pl gen", "verb": "prs 2 sg", "adjective": "m sg nom short"}
_amendment = {"noun": "зу´би_", "verb": "мо¨жеш", "adjective": "до¨бри_"}


@pytest.fixture
def expose_inputs(monkeypatch):
   """Records every string that is passed to `expose` anywhere in lookup."""
   inputs = []
   def recording(form, *args, **kwargs):
      inputs.append(form)
      return real_expose(form, *args, **kwargs)
   real_expose = expose_module.expose
   for module in (expose_module, pos):
      monkeypatch.setattr(module, "expose", recording)
   return inputs


@pytest.mark.parametrize("pos", ["noun", "verb", "adjective"])
@pytest.mark.parametrize("yat", ["e", "ije"])
def test_amended_forms_are_exposed_exactly_once(pos, yat, expose_inputs):
   forms = dict(_words()[pos].multiforms(yat=yat))[_label[pos]]
   amended = forms[-1] # amendments come after generated forms

   assert amended == expose_module.expose_replacement(_amendment[pos], yat), "not amended"
   assert amended not in expose_inputs, "amended form was exposed twice"


def test_amended_form_is_listed_after_generated_ones():
   forms = dict(_words()["verb"].multiforms())["prs 2 sg"]

   assert forms[-1] == "мо̏жеш"
   assert len(forms) > 1


def test_amended_forms_of_a_reflexive_verb_keep_the_particle():
   verb = Verb("могти", make_entry("мо`гˌти", "V\\Refl\\Ipf", "eʹ/kappa3",
      amendments=(("prs 2 sg", ["мо¨жеш"]),)
   ))

   forms = dict(verb.multiforms())["prs 2 sg"]
   latin_forms = dict(verb.multiforms(latin=True))["prs 2 sg"]

   assert all(f.endswith(" се") for f in forms)
   assert all(f.endswith(" se") for f in latin_forms)


def test_amended_forms_of_a_noun_without_regular_declension():
   pron = Noun("шта", make_entry("шта¨", "N\\0", "0", amendments=(("sg nom", ["шта¨"]),)))

   forms = dict(pron.multiforms())

   assert list(forms) == ["sg nom"]
   assert len(forms["sg nom"]) == 1


def test_adjective_replacements_and_amendments_use_spaced_labels():
   adjective = Adjective("добар", make_entry("до¨бар", "A\\all", "A.",
      replacements=(("f sg nom short", ["до¨бра_"]),),
      amendments=(("n sg nom short", ["до¨бро_"]),)
   ))

   forms = dict(adjective.multiforms())
   plain = dict(Adjective("добар", make_entry("до¨бар", "A\\all", "A.")).multiforms())

   assert forms["f sg nom short"] == [forms["f sg nom short"][0]]
   assert forms["f sg nom short"] != plain["f sg nom short"]
   assert len(forms["n sg nom short"]) == len(plain["n sg nom short"]) + 1


def test_adjective_labels_with_underscores_are_not_recognized():
   adjective = Adjective("добар", make_entry("до¨бар", "A\\all", "A.",
      replacements=(("f_sg_nom_short", ["до¨бра_"]),)
   ))
   plain = Adjective("добар", make_entry("до¨бар", "A\\all", "A."))

   assert dict(adjective.multiforms()) == dict(plain.multiforms())
