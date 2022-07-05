from __future__ import annotations

from typing import Any, Callable, Deque, Iterable, Iterator, List, Optional, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from .extrema_enumerable import ExtremaEnumerable

from .more_error import DirectedGraphNotAcyclicError
from ..enumerable import Enumerable
from ..util import (
    ComposeMap,
    ComposeSet,
    default_equal,
    identity,
)
from ..more_typing import (
    TAccumulate,
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
            seed, func, result_selector = args[0], args[1], identity
        else:  # len(args) == 1
            func, result_selector = args[0], identity
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

    def pre_scan(self,
        identity: TAccumulate,
        transformation: Callable[[TAccumulate, TSource_co], TAccumulate],
    ) -> MoreEnumerable[TAccumulate]:
        def inner(aggregator: TAccumulate = identity):
            it = iter(self)
            try:
                past = next(it)
            except StopIteration:
                return
            yield identity
            for elem in it:
                aggregator = transformation(aggregator, past)
                yield aggregator
                past = elem
        return MoreEnumerable(inner)

    def rank(self, *args: Callable[[TSource_co, TSource_co], int]) -> MoreEnumerable[int]:
        return self.rank_by(identity, *args)

    def rank_by(self,
        key_selector: Callable[[TSource_co], TKey],
        *args: Callable[[TKey, TKey], int]) -> MoreEnumerable[int]:
        if len(args) == 0:
            # it is sufficient to have only equality
            comparer = lambda l, r: 0 if l == r else 1
        else:  # len(args) == 1
            comparer = args[0]

        def inner():
            # avoid enumerating twice
            copy = MoreEnumerable(self.select(key_selector).to_list())
            # this is different from morelinq
            ordered = copy.order_by_descending(identity, *args).to_list()
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
            comparer = default_equal
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

    def scan(self, *args) -> Any:
        if len(args) == 2:
            seed, transformation = args
        else:  # len(args) == 1
            transformation = args[0]
        def inner():
            it = iter(self)
            nonlocal seed
            if len(args) == 1:
                try:
                    seed = next(it)
                except StopIteration:
                    return
            yield seed
            for elem in it:
                seed = transformation(seed, elem)
                yield seed
        return MoreEnumerable(inner)

    def scan_right(self, *args) -> Any:
        if len(args) == 2:
            seed, func = args
        else:  # len(args) == 1
            func = args[0]
        def inner():
            # NOTE: a copy of the sequence is made in this call because it falls back
            it = iter(self.reverse())
            nonlocal seed
            if len(args) == 1:
                try:
                    seed = next(it)
                except StopIteration:
                    return
            results = []
            results.append(seed)
            for elem in it:
                seed = func(elem, seed)
                results.append(seed)
            yield from reversed(results)
        return MoreEnumerable(inner)

    def segment(self,
        new_segment_predicate: Callable[[TSource_co], bool],
    ) -> MoreEnumerable[MoreEnumerable[TSource_co]]:
        return self.segment3(lambda x, p, i: new_segment_predicate(x))

    def segment2(self,
        new_segment_predicate: Callable[[TSource_co, int], bool],
    ) -> MoreEnumerable[MoreEnumerable[TSource_co]]:
        return self.segment3(lambda x, _, i: new_segment_predicate(x, i))

    def segment3(self,
        new_segment_predicate: Callable[[TSource_co, TSource_co, int], bool],
    ) -> MoreEnumerable[MoreEnumerable[TSource_co]]:
        def inner():
            it = iter(self)
            try:
                prev = next(it)
            except StopIteration:
                return
            segment = [prev]
            for i, elem in enumerate(it, 1):
                if new_segment_predicate(elem, prev, i):
                    yield MoreEnumerable(segment)
                    segment = [elem]
                else:
                    segment.append(elem)
                prev = elem
            yield MoreEnumerable(segment)
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
                for child in reversed(children):
                    stack.append(child)
        return MoreEnumerable(inner)

    def traverse_topological(self,
        children_selector: Callable[[TSource_co], Iterable[TSource_co]],
        *args: Callable[[TSource_co], object],
    ) -> MoreEnumerable[TSource_co]:
        if len(args) == 0:
            key_selector = identity
        else:  # len(args) == 1
            key_selector = args[0]

        def inner():
            stack: List[Tuple[TSource_co, bool]] = []
            visited = ComposeMap()
            result: List[TSource_co] = []  # post order
            result_keys = ComposeSet()
            # NOTE: a copy of the sequence is made in this call because it falls back
            for root in self.reverse():
                if not visited.get(key_selector(root)):
                    stack.append((root, False))
                while stack:
                    node, done = stack.pop()
                    if done:
                        # detect cycle. normally edges from node will go to nodes in the
                        # result list. otherwise we found cycle
                        for child in children_selector(node):
                            if key_selector(child) not in result_keys:
                                raise DirectedGraphNotAcyclicError((node, child))
                        # good
                        result.append(node)
                        result_keys.add(key_selector(node))
                        continue
                    visited[key_selector(node)] = True
                    stack.append((node, True))
                    for child in children_selector(node):
                        if not visited.get(key_selector(child)):
                            stack.append((child, False))
            while result:
                yield result.pop()
        return MoreEnumerable(inner)
