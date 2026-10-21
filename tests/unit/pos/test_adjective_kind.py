import pytest # type: ignore

from ....lookup.adjective import Adjective


def test_unknown_adjective_kind_raises_clear_error():
   with pytest.raises(NotImplementedError):
      Adjective("добар", "до¨бар", "A\\bogus", "A.", (), ())
