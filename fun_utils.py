from typing import Callable, Sequence, TypeVar, Union

_T = TypeVar('_T')

Transform = Callable[..., _T] # this is too liberal but at least works nice

_ComposeArg = Union[
   Callable[[_T], _T],
   tuple[Transform[_T], Sequence[str]]
]

def compose1(*functions: _ComposeArg[_T]) -> Transform[_T]:
   """Composes a sequence of functions T -> T.

      `compose1(f, g, h)(x) == f(g(h(x)))`

      If kwargs are given, they can be supplied to these functions by
      specifying which ones to give:

      `compose1(f, (g, ('a')), h)(x, a=1, b=2) = f(g(h(x), a=1))`"""
   def composition(arg, **kwargs):
      for f in reversed(functions):
         if isinstance(f, tuple):
            f, kws = f
            arg = f(arg, **{kw: kwargs[kw] for kw in kws})
         else:
            arg = f(arg)
      return arg
   return composition
