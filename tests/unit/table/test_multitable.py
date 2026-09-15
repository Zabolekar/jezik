from ....lookup import lookup


def test_form_query_without_matches_returns_an_empty_multitable():
   result = lookup("свет")["does-not-exist"]

   assert len(result) == 0
   assert not result
