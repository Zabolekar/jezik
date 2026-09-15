from ...lookup import lookup


def test_dictionary_view_target_is_preserved_in_the_lookup_table():
   table = lookup("адвокатирати")[0]

   assert table.view == "адвокатисати"
