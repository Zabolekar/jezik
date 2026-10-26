import pytest # type: ignore

from ...fun_utils import compose1


def test_compose1_applies_functions_right_to_left():
   f = compose1(lambda x: x + "f", lambda x: x + "g", lambda x: x + "h")

   assert f("") == "hgf"


def test_compose1_without_functions_is_the_identity():
   assert compose1()("x") == "x"


def test_compose1_passes_only_the_requested_kwargs():
   def g(x, a):
      return x + a
   def h(x): # would raise TypeError if it got any kwargs
      return x + "h"

   composed = compose1(str.upper, (g, ("a",)), h)

   assert composed("", a="a", b="b") == "HA"


def test_compose1_requires_the_requested_kwargs():
   composed = compose1((lambda x, a: x + a, ("a",)))

   with pytest.raises(KeyError):
      composed("x")
