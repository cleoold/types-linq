from __future__ import annotations
from typing import Any, Callable, Generic, Iterable, Iterator, Optional

from .enumerable import Enumerable

from .more_typing import (
    TSource_co,
    TKey,
    TKey2,
)


class OrderedEnumerable(Enumerable[TSource_co], Generic[TSource_co, TKey]):

    _parent: Optional[OrderedEnumerable[TSource_co, Any]]
    _key_selector: Callable[[TSource_co], TKey]
    _comparer: Optional[Callable[[TKey, TKey], int]]
    _descending: bool

    def __init__(self,
        source: Callable[[], Iterable[TSource_co]],  # pass along
        parent: Optional[OrderedEnumerable[TSource_co, Any]],
        key_selector: Callable[[TSource_co], TKey],
        comparer: Optional[Callable[[TKey, TKey], int]],
        descending: bool,
    ):
        super().__init__(source)
        self._parent = parent
        self._key_selector = key_selector
        self._comparer = comparer
        self._descending = descending

    def _get_iterable(self) -> Iterator[TSource_co]:
        lst = [elem for elem in super()._get_iterable()]
        curr = self
        while curr is not None:
            comparer = curr._comparer
            if comparer is None:
                # comparer-less overload for order_by(), etc. ensures TSource_co must support __lt__()
                key = curr._key_selector  # type: ignore
            else:
                selector = curr._key_selector
                class key:
                    def __init__(self, elem):
                        self.elem = elem
                    def __lt__(self, __o: key):
                        return comparer(selector(self.elem), selector(__o.elem)) < 0  # type: ignore
            lst.sort(key=key, reverse=curr._descending)
            curr = curr._parent
        yield from lst

    def create_ordered_enumerable(self,
        key_selector: Callable[[TSource_co], TKey2],
        comparer: Optional[Callable[[TKey2, TKey2], int]],
        descending: bool,
    ) -> OrderedEnumerable[TSource_co, TKey2]:
        return OrderedEnumerable(
            self._get_iterable,
            self,
            key_selector,
            comparer,
            descending,
        )

    def then_by(self,
        key_selector: Callable[[TSource_co], TKey2],
        *args: Callable[[TKey2, TKey2], int],
    ) -> OrderedEnumerable[TSource_co, TKey2]:
        if len(args) == 1:
            comparer = args[0]
        else:  # len(args) == 2:
            comparer = None
        return self.create_ordered_enumerable(
            key_selector,
            comparer,
            False,
        )

    def then_by_descending(self,
        key_selector: Callable[[TSource_co], TKey2],
        *args: Callable[[TKey2, TKey2], int],
    ) -> OrderedEnumerable[TSource_co, TKey2]:
        if len(args) == 1:
            comparer = args[0]
        else:  # len(args) == 2:
            comparer = None
        return self.create_ordered_enumerable(
            key_selector,
            comparer,
            True,
        )
