from __future__ import annotations
from typing import Any, Callable, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from .extrema_enumerable import ExtremaEnumerable

from .enumerable import Enumerable
from .more_typing import (
    TSource_co,
    TSupportsLessThan,
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

    def interleave(self, *iters: Iterable[TSource_co]) -> MoreEnumerable[TSource_co]:
        def inner():
            its = [iter(self)]
            for iter_ in iters:
                its.append(iter(iter_))
            while its:
                i = 0
                while i < len(its):
                    try:
                        yield next(its[i])
                        i += 1
                    except StopIteration:
                        its.pop(i)
        return MoreEnumerable(inner)

    def max_by(self,
        selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> ExtremaEnumerable[TSource_co, TSupportsLessThan]:
        from .extrema_enumerable import ExtremaEnumerable
        return ExtremaEnumerable(self, selector, lambda x, y: y < x)

    def min_by(self,
        selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> ExtremaEnumerable[TSource_co, TSupportsLessThan]:
        from .extrema_enumerable import ExtremaEnumerable
        return ExtremaEnumerable(self, selector, lambda x, y: x < y)
