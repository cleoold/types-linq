from __future__ import annotations

from typing import Any, Callable, Deque, Iterable, Iterator, List, Optional, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from .extrema_enumerable import ExtremaEnumerable

from ..enumerable import Enumerable
from ..util import ComposeMap, ComposeSet
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

    def consume(self) -> None:
        for _ in self:
            ...

    def cycle(self, count: Optional[int] = None) -> MoreEnumerable[TSource_co]:
        if count is not None:
            if count < 0:
                self._raise_count_negative()  # type: ignore
            elif count == 0:
                return MoreEnumerable(())
            elif count == 1:
                return self

        def inner(cnt=count):
            memo: List[TSource_co] = []
            for elem in self:
                memo.append(elem)
                yield elem
            while cnt is None or cnt > 1:
                yield from memo
                if cnt is not None:
                    cnt -= 1
        return MoreEnumerable(inner)

    def enumerate(self, start: int = 0) -> MoreEnumerable[Tuple[int, TSource_co]]:
        return MoreEnumerable(lambda: enumerate(self, start))

    def except_by2(self,
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

    def rank(self, *args: Callable[[TSource_co, TSource_co], int]) -> MoreEnumerable[int]:
        return self.rank_by(lambda x: x, *args)

    def rank_by(self,
        key_selector: Callable[[TSource_co], TKey],
        *args: Callable[[TKey, TKey], int]) -> MoreEnumerable[int]:
        if len(args) == 0:
            comparer = None
        else:  # len(args) == 1
            comparer = args[0]

        def inner():
            # avoid enumerating twice
            copy = MoreEnumerable(self.select(key_selector).to_list())
            ordered = copy.distinct() \
                .order_by_descending(lambda x: x, *args)
            if comparer is None:
                # replaces .enumerate()
                rank_map = ComposeMap(ordered.select2(lambda x, i: (x, i + 1)))
            else:
                # this is different from morelinq
                ordered = ordered.to_list()
                if not ordered:
                    return
                rank_map = ComposeMap()
                rank_map[ordered[0]] = 1
                rank = 1
                for i in range(1, len(ordered)):
                    if comparer(ordered[i - 1], ordered[i]) != 0:
                        rank += 1
                    rank_map[ordered[i]] = rank
            for key in copy:
                yield rank_map[key]
        return MoreEnumerable(inner)

    def run_length_encode(self,
        *args: Callable[[TSource_co, TSource_co], bool],
    ) -> MoreEnumerable[Tuple[TSource_co, int]]:
        if len(args) == 0:
            comparer = lambda x, y: x == y
        else:
            comparer = args[0]
        def inner():
            iterator = iter(self)
            try:
                prev_elem = next(iterator)
            except StopIteration:
                return
            count = 1
            while True:
                try:
                    elem = next(iterator)
                except StopIteration:
                    break
                if comparer(prev_elem, elem):
                    count += 1
                else:
                    yield (prev_elem, count)
                    prev_elem = elem
                    count = 1
            yield (prev_elem, count)
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
