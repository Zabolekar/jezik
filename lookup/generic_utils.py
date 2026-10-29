from typing import Callable, Generic, Iterable, Sequence, TypeVar, Union
from collections import OrderedDict
from itertools import repeat

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


def str_find(word:str, substr:str) -> int:
   found = word.find(substr)
   if found == -1:
      return len(word)
   return found

def has(word:Union[str, list[str]], *args:str) -> bool:
   """
   Actually could've been called smth like "contains_any"
   but we need some brevity here.
   """
   for arg in args:
      if arg in word:
         return True
   return False

def append_def(
   target_list:list[str],
   input_list:list[str],
   appendable:list[str],
   default_item:str
) -> list[str]:
   appended = False
   for item in input_list:
      if item in appendable:
         target_list.append(item)
         appended = True
   if not appended:
      target_list.append(default_item)
   return target_list

class OrderedSet(OrderedDict, Generic[_T]):
   def __init__(self, i:Iterable[_T]) -> None:
      super().__init__(zip(i, repeat(None)))

   def __repr__(self) -> str:
      return f"OrderedSet({list(self)})"

def uniq(i:Iterable[_T]) -> list[_T]:
   return list(OrderedSet(i))

def strip_suffix(value:str, suffixes:Iterable[str]) -> tuple[str, bool]:
   """
   Tries to strip one of the given suffixes, iterating over them.
   If succesful, returns (stripped_value, True).
   Otherwise, returns (value, False).
   """
   for suffix in suffixes:
      if value.endswith(suffix):
         return value[:len(value) - len(suffix)], True
   return value, False
