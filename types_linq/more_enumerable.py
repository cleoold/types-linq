from __future__ import annotations
from typing import Any, Callable

from .enumerable import Enumerable
from .more_typing import (
    TSource_co,
)


class MoreEnumerable(Enumerable[TSource_co]):

    def aggregate_right(self, *args) -> Any:
        # NOTE: a copy of the sequence is made in this call because it falls back
        it = iter(self.reverse())
        if len(args) == 3:
            seed, func, result_selector = args
        elif len(args) == 2:
            seed, func, result_selector = args[0], args[1], lambda x: x
        else:  # len(args) == 1
            func, result_selector = args[0], lambda x: x
            try:
                seed = next(it)
            except StopIteration:
                self._raise_empty_sequence()

        for elem in it:
            seed = func(elem, seed)
        return result_selector(seed)

    def as_more(self) -> MoreEnumerable[TSource_co]:  # pyright: reportIncompatibleMethodOverride=false
        return self

    def for_each(self, action: Callable[[TSource_co], Any]) -> None:
        for elem in self:
            action(elem)

    def for_each2(self, action: Callable[[TSource_co, int], Any]) -> None:
        for i, elem in enumerate(self):
            action(elem, i)
