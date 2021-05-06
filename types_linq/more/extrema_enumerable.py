from __future__ import annotations
from typing import Callable, Deque, Generic, Iterable, Optional, Union

from .more_enumerable import MoreEnumerable
from ..more_typing import (
    TKey,
    TSource,
    TSource_co,
)


# appreciation to: MoreLinq.IExtremaEnumerable by morelinq
class ExtremaEnumerable(MoreEnumerable[TSource_co], Generic[TSource_co, TKey]):

    _selector: Callable[[TSource_co], TKey]
    _comparer: Optional[Callable[[TKey, TKey], int]]
    _for_min: bool

    def __init__(self,
        source: Iterable[TSource_co],
        selector: Callable[[TSource_co], TKey],
        comparer: Optional[Callable[[TKey, TKey], int]],
        for_min: bool,
    ) -> None:
        super().__init__(source)
        self._selector = selector
        self._comparer = comparer
        self._for_min = for_min

    # only enumerate extrema when needed. __iter__-ing it will get all extrema; take()-ing it with
    # count elems only store that number of elems in the buffer
    def _get_iterable(self) -> Iterable[TSource_co]:
        it = super()._get_iterable()
        getter = lambda: _FirstExtrema(None)
        return _extrema_by(it, getter, self._selector, self._comparer, self._for_min)

    # please maintain same overloads
    def first(self, *args):  # pyright: reportIncompatibleMethodOverride=false
        if len(args) == 0:
            return MoreEnumerable.first(self.take(1))
        else:  # len(args) == 1
            return super().first(*args)

    # please maintain same overloads
    def first2(self, *args):
        if len(args) == 1:
            return MoreEnumerable.first2(self.take(1), *args)
        else:  # len(args) == 2
            return super().first2(*args)

    # please maintain same overloads
    def last(self, *args):
        if len(args) == 0:
            return MoreEnumerable.last(self.take_last(1))
        else:  # len(args) == 1
            return super().last(*args)

    # please maintain same overloads
    def last2(self, *args):
        if len(args) == 1:
            return MoreEnumerable.last2(self.take_last(1), *args)
        else:  # len(args) == 2
            return super().last2(*args)

    # please maintain same overloads
    def single(self, *args):
        if len(args) == 0:
            return MoreEnumerable.single(self.take(2))
        else:  # len(args) == 1
            return super().single(*args)

    # please maintain same overloads
    def single2(self, *args):
        if len(args) == 1:
            return MoreEnumerable.single2(self.take(2), *args)
        else:  # len(args) == 2
            return super().single2(*args)

    def take(self, count: int) -> MoreEnumerable[TSource_co]:
        if count <= 0:
            return MoreEnumerable(())
        it = super()._get_iterable()
        getter = lambda: _FirstExtrema(count)
        return _extrema_by(it, getter, self._selector, self._comparer, self._for_min)

    def take_last(self, count: int) -> MoreEnumerable[TSource_co]:
        if count <= 0:
            return MoreEnumerable(())
        it = super()._get_iterable()
        getter = lambda: _LastExtrema(count)
        return _extrema_by(it, getter, self._selector, self._comparer, self._for_min)


def _extrema_by(
    source: Iterable[TSource],
    extrema_getter: Callable[[], _Extrema[TSource]],
    selector: Callable[[TSource], TKey],
    comparer: Optional[Callable[[TKey, TKey], int]],
    for_min: bool,
) -> MoreEnumerable[TSource]:
    it = iter(source)
    try:
        elem = next(it)
    except StopIteration:
        return MoreEnumerable(())

    if comparer is None:
        # None comparer ensures TSource must support __lt__()
        comparer = _lt_comparer
    if for_min:
        comparer = lambda x, y, comp=comparer: comp(y, x)

    extrema = extrema_getter()
    extrema.add(elem)
    extremum_key = selector(elem)
    for elem in it:
        key = selector(elem)
        cmp = comparer(key, extremum_key)
        if cmp > 0:
            extrema.restart()
            extrema.add(elem)
            extremum_key = key
        elif cmp == 0:
            extrema.add(elem)

    def inner():
        yield from extrema.store
    return MoreEnumerable(inner)


def _lt_comparer(x, y) -> int:
    if x < y: return -1
    # assumes total ordering
    elif y < x: return 1
    return 0


class _FirstExtrema(Generic[TSource]):
    def __init__(self, capacity: Optional[int]) -> None:
        self.store = []
        self.capacity = capacity

    def add(self, element: TSource) -> None:
        if self.capacity is None or len(self.store) < self.capacity:
            self.store.append(element)

    def restart(self) -> None:
        self.store.clear()


class _LastExtrema(Generic[TSource]):
    def __init__(self, capacity: Optional[int]) -> None:
        self.store = Deque()
        self.capacity = capacity

    def add(self, element: TSource) -> None:
        if self.capacity is not None and len(self.store) == self.capacity:
            self.store.popleft()
        self.store.append(element)

    def restart(self) -> None:
        self.store.clear()


_Extrema = Union[_FirstExtrema[TSource], _LastExtrema[TSource]]
