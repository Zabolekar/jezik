from ....lookup.verb import Verb


def _forms(replacements, latin=False):
   verb = Verb("бојати", "бо`јати", "V\\Refl\\Ipf", "a./beta", replacements, ())
   return dict(verb.multiforms(latin=latin))


def test_replaced_forms_of_reflexive_verb_keep_the_particle():
   forms = _forms((("prs 1 sg", ["бо`јим"]),))

   assert forms["prs 1 sg"][0].endswith(" се")
   assert all(f.endswith(" се") for f in forms["prs 2 sg"])


def test_replaced_forms_of_reflexive_verb_keep_latin_particle():
   forms = _forms((("prs 1 sg", ["бо`јим"]),), latin=True)

   assert forms["prs 1 sg"][0].endswith(" se")
