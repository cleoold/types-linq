from __future__ import annotations
from typing import Callable, Generic, Optional, overload

from .enumerable import Enumerable
from .more_typing import (
    TSource_co,
    TKey,
    TKey2,
    TSupportsLessThan,
)


class OrderedEnumerable(Enumerable[TSource_co], Generic[TSource_co, TKey]):
    '''
    Represents a sorted Enumerable sequence that is sorted by some key.
    '''

    def __init__(self, *args): ...

    def create_ordered_enumerable(self,
        key_selector: Callable[[TSource_co], TKey2],
        comparer: Optional[Callable[[TKey2], int]],
        descending: bool,
    ) -> OrderedEnumerable[TSource_co, TKey2]:
        '''
        Performs a subsequent ordering on the elements of the sequence according to a key.
        '''

    @overload
    def then_by(self,
        key_selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> OrderedEnumerable[TSource_co, TSupportsLessThan]:
        '''
        Performs a subsequent ordering of the elements in ascending order according to key.
        '''

    @overload
    def then_by(self,
        key_selector: Callable[[TSource_co], TKey2],
        __comparer: Callable[[TKey2, TKey2], int],
    ) -> OrderedEnumerable[TSource_co, TKey2]:
        '''
        Performs a subsequent ordering of the elements in ascending order by using a specified comparer.
        '''

    @overload
    def then_by_descending(self,
        key_selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> OrderedEnumerable[TSource_co, TSupportsLessThan]:
        '''
        Performs a subsequent ordering of the elements in descending order according to key.
        '''

    @overload
    def then_by_descending(self,
        key_selector: Callable[[TSource_co], TKey2],
        __comparer: Callable[[TKey2, TKey2], int],
    ) -> OrderedEnumerable[TSource_co, TKey2]:
        '''
        Performs a subsequent ordering of the elements in descending order by using a specified comparer.
        '''
