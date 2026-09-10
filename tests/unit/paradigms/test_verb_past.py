from ....lookup.verb.paradigms import a_past, a_theme_ipf, ending_ste


def test_a_past_imperfect_second_person_plural_ends_in_ste():
   assert a_past.ipf_2_pl == [[a_theme_ipf, ending_ste]]
