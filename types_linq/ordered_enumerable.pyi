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
    .. code-block:: python

        from types_linq.ordered_enumerable import OrderedEnumerable

    Represents a sorted Enumerable sequence that is sorted by some key.

    Users should not construct instances of this class directly. Use ``Enumerable.order_by()`` instead.
    '''

    def __init__(self, *args): ...

    def create_ordered_enumerable(self,
        key_selector: Callable[[TSource_co], TKey2],
        comparer: Optional[Callable[[TKey2, TKey2], int]],
        descending: bool,
    ) -> OrderedEnumerable[TSource_co, TKey2]:
        '''
        Performs a subsequent ordering on the elements of the sequence according to a key.

        Comparer takes two values and return positive ints when lhs > rhs, negative ints
        if lhs < rhs, and 0 if they are equal.

        Revisions:
            - v0.1.2: Fixed incorrect parameter type of comparer.
        '''

    @overload
    def then_by(self,
        key_selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> OrderedEnumerable[TSource_co, TSupportsLessThan]:
        '''
        Performs a subsequent ordering of the elements in ascending order according to key.

        Example
            .. code-block:: python

                >>> class Pet(NamedTuple):
                ...     name: str
                ...     age: int

                >>> pets = [Pet('Barley', 8), Pet('Boots', 4), Pet('Roman', 5), Pet('Daisy', 4)]
                >>> Enumerable(pets).order_by(lambda p: p.age) \\
                ...     .then_by(lambda p: p.name)             \\
                ...     .select(lambda p: p.name)              \\
                ...     .to_list()
                ['Boots', 'Daisy', 'Roman', 'Barley']
        '''

    @overload
    def then_by(self,
        key_selector: Callable[[TSource_co], TKey2],
        __comparer: Callable[[TKey2, TKey2], int],
    ) -> OrderedEnumerable[TSource_co, TKey2]:
        '''
        Performs a subsequent ordering of the elements in ascending order by using a specified comparer.

        Such comparer takes two values and return positive ints when lhs > rhs, negative ints
        if lhs < rhs, and 0 if they are equal.
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

        Such comparer takes two values and return positive ints when lhs > rhs, negative ints
        if lhs < rhs, and 0 if they are equal.
        '''
