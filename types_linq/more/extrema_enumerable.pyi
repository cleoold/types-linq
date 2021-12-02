from typing import Callable, Generic, Iterable, Optional

from .more_enumerable import MoreEnumerable
from ..more_typing import (
    TKey,
    TSource_co,
)


class ExtremaEnumerable(MoreEnumerable[TSource_co], Generic[TSource_co, TKey]):
    '''
    .. code-block:: python

        from types_linq.more.extrema_enumerable import ExtremaEnumerable

    Specialization for manipulating extrema.

    Users should not construct instances of this class directly. Use ``MoreEnumerable.maxima_by()``
    instead.

    Revisions:
        - v0.2.0: New.
    '''

    def __init__(self,
        source: Iterable[TSource_co],
        selector: Callable[[TSource_co], TKey],
        comparer: Optional[Callable[[TKey, TKey], int]],
        for_min: bool,
    ) -> None: ...  # internal

    def take(self, count: int) -> MoreEnumerable[TSource_co]:
        '''
        Returns a specified number of contiguous elements from the start of the sequence.
        '''

    def take_last(self, count: int) -> MoreEnumerable[TSource_co]:
        '''
        Returns a new sequence that contains the last `count` elements.
        '''
