import pytest # type: ignore

from ...lookup.paradigm_helpers import GramInfo, OrderedSet, cut_AP, make_caption, str_find


def test_gram_info_parses_comments_paradigms_and_kind_labels():
   gram = GramInfo("V\\Refl\\Ipf", ["note\\a$/alpha", "b./beta"])

   assert gram.AP == ["a:", "b."]
   assert gram.MP == ["alpha", "beta"]
   assert gram.comment == ["note", ""]
   assert gram.POS == "V"
   assert gram.other == ["Refl", "Ipf"]


@pytest.mark.parametrize("kind, infos, message", [
   ("", ["a./alpha"], "empty t"),
   ("N", [""], "empty i"),
   ("N", ["a\\b\\c"], "backslashes"),
   ("N", ["a/b/c"], "slashes"),
])
def test_gram_info_rejects_malformed_metadata(kind, infos, message):
   with pytest.raises(ValueError, match=message):
      GramInfo(kind, infos)


def test_helper_edge_cases_keep_search_and_caption_semantics():
   assert str_find("реч", "ч") == 2
   assert str_find("реч", "x") == len("реч")
   assert cut_AP("comment\\a$/alpha") == "a:"
   assert list(OrderedSet(["a", "b", "a"])) == ["a", "b"]
   assert repr(OrderedSet(["a"])) == "OrderedSet(['a'])"
   assert make_caption(("именица", "II:"), 2, 1).full_caption == "именица (вар. 2)"
