from __future__ import annotations

from typing import Any, Callable, Deque, Iterable, Iterator, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .extrema_enumerable import ExtremaEnumerable

from ..enumerable import Enumerable
from ..util import ComposeSet
from ..more_typing import (
    TKey,
    TSource,
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

    def distinct_by(self, key_selector: Callable[[TSource_co], object]) -> MoreEnumerable[TSource_co]:
        return self.except_by((), key_selector)

    def except_by(self,
        second: Iterable[TSource_co],
        key_selector: Callable[[TSource_co], object],
    ) -> MoreEnumerable[TSource_co]:
        def inner():
            s = ComposeSet(key_selector(s) for s in second)
            for elem in self:
                key = key_selector(elem)
                if key in s:
                    continue
                s.add(key)
                yield elem
        return MoreEnumerable(inner)

    def flatten(self, *args: Callable[[Iterable[Any]], bool]) -> MoreEnumerable[Any]:
        if len(args) == 0:
            return self.flatten(lambda x: not isinstance(x, (str, bytes)))
        else:  # len(args) == 1
            predicate = args[0]
            return self.flatten2(lambda x: x
                if isinstance(x, Iterable) and predicate(x)
                else None)

    def flatten2(self, selector: Callable[[Any], Optional[Iterable[object]]]) -> MoreEnumerable[Any]:
        def inner():
            stack: List[Iterator[object]] = [iter(self)]
            while stack:
                it = stack.pop()
                while True:
                    try:
                        elem = next(it)
                    except StopIteration:
                        break
                    nested = selector(elem)
                    if nested is not None:
                        stack.append(it)
                        it = iter(nested)
                        continue
                    yield elem
        return MoreEnumerable(inner)

    def for_each(self, action: Callable[[TSource_co], object]) -> None:
        for elem in self:
            action(elem)

    def for_each2(self, action: Callable[[TSource_co, int], object]) -> None:
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

    def maxima_by(self,
        selector: Callable[[TSource_co], TKey],
        *args: Callable[[TKey, TKey], int],
    ) -> ExtremaEnumerable[TSource_co, TKey]:
        from .extrema_enumerable import ExtremaEnumerable
        if len(args) == 0:
            comparer = None
        else:  # len(args) == 1
            comparer = args[0]
        return ExtremaEnumerable(self, selector, comparer, False)

    def minima_by(self,
        selector: Callable[[TSource_co], TKey],
        *args: Callable[[TKey, TKey], int],
    ) -> ExtremaEnumerable[TSource_co, TKey]:
        from .extrema_enumerable import ExtremaEnumerable
        if len(args) == 0:
            comparer = None
        else:  # len(args) == 1
            comparer = args[0]
        return ExtremaEnumerable(self, selector, comparer, True)

    def pipe(self, action: Callable[[TSource_co], object]) -> MoreEnumerable[TSource_co]:
        def inner():
            for elem in self:
                action(elem)
                yield elem
        return MoreEnumerable(inner)

    @staticmethod
    def traverse_breath_first(
        root: TSource,
        children_selector: Callable[[TSource], Iterable[TSource]],
    ) -> MoreEnumerable[TSource]:
        def inner():
            queue = Deque((root,))
            while queue:
                elem = queue.popleft()
                yield elem
                for child in children_selector(elem):
                    queue.append(child)
        return MoreEnumerable(inner)

    @staticmethod
    def traverse_depth_first(
        root: TSource,
        children_selector: Callable[[TSource], Iterable[TSource]],
    ) -> MoreEnumerable[TSource]:
        def inner():
            stack = [root]
            while stack:
                elem = stack.pop()
                yield elem
                children = [*children_selector(elem)]
                for children in reversed(children):
                    stack.append(children)
        return MoreEnumerable(inner)
