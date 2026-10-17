from ....lookup.verb.paradigms import (
   MP_to_verb_stems, VerbParadigm, i_past, i_present
)


def test_alpha_is_a_flat_ordered_sequence_of_labeled_forms():
   paradigm = MP_to_verb_stems["alpha"]

   assert isinstance(paradigm, VerbParadigm)
   assert [form.label for form in paradigm.forms] == [
      "prs 1 sg", "prs 2 sg", "prs 3 sg", "prs 1 pl", "prs 2 pl", "prs 3 pl",
      "imv 2 sg", "imv 1 pl", "imv 2 pl",
      "pf m sg", "pf f sg", "pf n sg", "pf m pl", "pf f pl", "pf n pl",
      "aor 1 sg", "aor 2 sg", "aor 3 sg", "aor 1 pl", "aor 2 pl", "aor 3 pl",
      "infinitive",
      "ipf 1 sg", "ipf 2 sg", "ipf 3 sg", "ipf 1 pl", "ipf 2 pl", "ipf 3 pl",
   ]
   assert len(paradigm.forms[3].variants) == 2


def test_alpha_combines_i_present_and_i_past_forms():
   combined_forms = (*i_present.forms, *i_past.forms)

   assert MP_to_verb_stems["alpha"].forms == combined_forms


def test_every_verb_type_uses_a_flat_paradigm():
   assert all(isinstance(paradigm, VerbParadigm) for paradigm in MP_to_verb_stems.values())


def test_every_verb_type_has_the_complete_set_of_form_labels():
   expected_labels = [form.label for form in MP_to_verb_stems["alpha"].forms]

   for paradigm in MP_to_verb_stems.values():
      assert [form.label for form in paradigm.forms] == expected_labels
