from typing import Callable, Generic, Iterable

from .more_enumerable import MoreEnumerable
from ..more_typing import (
    TSource_co,
    TSupportsLessThan,
)


class ExtremaEnumerable(MoreEnumerable[TSource_co], Generic[TSource_co, TSupportsLessThan]):
    '''
    Specialization for manipulating extrema.
    '''

    def __init__(self,
        source: Iterable[TSource_co],
        selector: Callable[[TSource_co], TSupportsLessThan],
        lt_op: Callable[[TSupportsLessThan, TSupportsLessThan], bool],
    ) -> None: ...  # internal

    def take(self, count: int) -> MoreEnumerable[TSource_co]:
        '''
        Returns a specified number of contiguous elements from the start of the sequence.
        '''

    def take_last(self, count: int) -> MoreEnumerable[TSource_co]:
        '''
        Returns a new sequence that contains the last `count` elements.
        '''
