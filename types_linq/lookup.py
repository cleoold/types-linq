from __future__ import annotations
from typing import Callable, Iterable

from .enumerable import Enumerable
from .grouping import Grouping
from .util import ComposeMap

from .more_typing import (
    TSource,
    TKey_co,
    TValue_co,
    TResult,
)


# TODO: Wish to support Mapping[TKey, TValue], but its default mixin methods are doing something
# weird.
class Lookup(Enumerable[Grouping[TKey_co, TValue_co]]):
    '''
    .. code-block:: python

        from types_linq.lookup import Lookup

    A lookup is a one-to-many dictionary. It maps keys to Enumerable sequences of values.

    Users should not construct instances of this class directly. Use ``Enumerable.to_lookup()``
    instead.
    '''

    _groupings: ComposeMap[TKey_co, Grouping[TKey_co, TValue_co]]

    def __init__(self,
        source: Iterable[TSource],
        key_selector: Callable[[TSource], TKey_co],
        value_selector: Callable[[TSource], TValue_co],
    ):
        self._groupings = ComposeMap()

        for src in source:
            key = key_selector(src)
            elem = value_selector(src)
            if key not in self._groupings:
                self._groupings[key] = Grouping(key)
            self._groupings[key]._append(elem)

        super().__init__(self._groupings.values())

    def __contains__(self, value: object) -> bool:
        '''
        Tests whether key is in the lookup.
        '''
        return value in self._groupings

    def __len__(self) -> int:
        '''
        Gets the number of key-collection pairs.
        '''
        return len(self._groupings)

    def __getitem__(self, key: TKey_co) -> Enumerable[TValue_co]:  # type: ignore
        '''
        Gets the collection of values indexed by the specified key, or empty if no such key
        exists.
        '''
        if key in self._groupings:
            return self._groupings[key]
        return Enumerable.empty()  # type: ignore

    def apply_result_selector(self,
        result_selector: Callable[[TKey_co, Enumerable[TValue_co]], TResult],
    ) -> Enumerable[TResult]:
        '''
        Applies a transform function to each key and its associated values, then returns the
        results.
        '''
        def inner():
            for key, grouping in self._groupings.items():
                yield result_selector(key, grouping)
        return Enumerable(inner)

    def contains(self, value: object) -> bool:  # type: ignore[override]
        '''
        Tests whether key is in the lookup.
        '''
        return value in self

    @property
    def count(self) -> int:    # type: ignore[override]
        '''
        Gets the number of key-collection pairs.
        '''
        return len(self)
