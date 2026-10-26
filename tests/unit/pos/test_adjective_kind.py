import pytest # type: ignore

from ...entries import make_entry
from ....lookup.adjective import Adjective


def test_unknown_adjective_kind_raises_clear_error():
   with pytest.raises(NotImplementedError):
      Adjective("добар", make_entry("до¨бар", "A\\bogus", "A."))
