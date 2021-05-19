from __future__ import annotations
from typing import Dict, Iterable, Iterator, Optional

from .enumerable import Enumerable
from .types_linq_error import InvalidOperationError

from .more_typing import (
    TSource_co,
)


class CachedEnumerable(Enumerable[TSource_co]):
    '''
    .. code-block:: python

        from types_linq.cached_enumerable import CachedEnumerable

    Enumerable that stores the enumerated results which can be accessed repeatedly.

    Users should not construct instances of this class directly. Use ``Enumerable.as_cached()`` instead.
    '''

    _iter: Iterator[TSource_co]
    _cache_capacity: Optional[int]
    _enumerated_values: Dict[int, TSource_co]
    _min_index: int
    _tracked: int

    def __init__(self, source: Iterable[TSource_co], cache_capacity: Optional[int]):
        if cache_capacity is not None and cache_capacity < 0:
            raise InvalidOperationError('cache_capacity must be nonnegative')
        self._iter = iter(source)
        super().__init__(self._iter)
        self._cache_capacity = cache_capacity
        self._enumerated_values = {}
        self._min_index = 0
        self._tracked = 0

    def _get_iterable(self) -> Iterator[TSource_co]:
        i = 0
        while True:
            while i < self._tracked and self._cache_capacity != 0:
                i = max(self._min_index, i)
                res = self._enumerated_values[i]
                i += 1
                yield res
            try:
                res = next(self._iter)
            except StopIteration:
                break
            len_ = len(self._enumerated_values)
            if self._cache_capacity is not None and \
                len_ > 0 and len_ == self._cache_capacity:
                del self._enumerated_values[self._min_index]
                self._min_index += 1
            self._enumerated_values[self._tracked] = res
            self._tracked += 1
            i += 1
            yield res

    def as_cached(self, *, cache_capacity: Optional[int] = None) -> CachedEnumerable[TSource_co]:
        '''
        Updates settings and returns the original CachedEnumerable reference.

        Raises `InvalidOperationError` if cache_capacity is negative.
        '''
        if cache_capacity is not None:
            if cache_capacity < 0:
                raise InvalidOperationError('cache_capacity must be nonnegative')
            while len(self._enumerated_values) > cache_capacity:
                del self._enumerated_values[self._min_index]
                self._min_index += 1
        self._cache_capacity = cache_capacity
        return self
