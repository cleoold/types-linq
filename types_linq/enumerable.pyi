from typing import Any, Callable, Dict, Generic, Iterable, Iterator, List, MutableSequence, NoReturn, Optional, Sequence, Set, Tuple, Type, Union, overload

from .lookup import Lookup
from .grouping import Grouping
from .ordered_enumerable import OrderedEnumerable
from .cached_enumerable import CachedEnumerable
from .more import MoreEnumerable
from .more_typing import (
    SupportsAverage,
    TAccumulate,
    TCollection,
    TDefault,
    TInner,
    TKey,
    TOther,
    TOther2,
    TOther3,
    TOther4,
    TResult,
    TSource_co,
    TSupportsAdd,
    TSupportsLessThan,
    TValue,
)


class Enumerable(Sequence[TSource_co], Generic[TSource_co]):
    '''
    .. code-block:: python

        from types_linq import Enumerable

    Provides a set of helper methods for querying iterable objects.
    '''

    @overload
    def __init__(self, __iterable: Iterable[TSource_co]) -> None:
        '''
        Wraps an iterable.
        '''

    @overload
    def __init__(self, __iterable_factory: Callable[[], Iterable[TSource_co]]) -> None:
        '''
        Wraps an iterable returned from the iterable factory. The factory will be called whenever
        an enumerating operation is performed.
        '''

    def _get_iterable(self) -> Iterable[TSource_co]: ...  # internal

    def __contains__(self, value: object) -> bool:
        '''
        Tests whether the sequence contains the specified element. Prefers calling `__contains__()`
        on the wrapped iterable if available, otherwise, calls `self.contains()`.

        Example
            >>> en = Enumerable([1, 10, 100])
            >>> 1000 in en
            False
        '''

    @overload
    def __getitem__(self, index: int) -> TSource_co:
        '''
        Returns the element at specified index in the sequence. Prefers calling `__getitem__()` on the
        wrapped iterable if available, otherwise, calls `self.element_at()`.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100

                >>> Enumerable(gen())[1]
                10
        '''

    @overload
    def __getitem__(self, __index_and_default: Tuple[int, TDefault]) -> Union[TSource_co, TDefault]:
        '''
        Returns the element at specified index in the sequence or returns the default value if it does not
        exist. Prefers calling `__getitem__()` on the wrapped iterable if available, otherwise, calls
        `self.element_at()`.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100

                >>> Enumerable(gen())[3, 1000]
                1000

        Revisions:
            - v1.0.0: New.
        '''

    @overload
    def __getitem__(self, index: slice) -> Enumerable[TSource_co]:
        '''
        Produces a subsequence defined by the given slice notation. Prefers calling `__getitem__()` on the
        wrapped iterable if available, otherwise, calls `self.elements_in()`.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100; yield 1000; yield 10000

                >>> Enumerable(gen())[1:3].to_list()
                [10, 100]
        '''

    def __iter__(self) -> Iterator[TSource_co]:
        '''
        Returns an iterator that enumerates the values in the sequence.

        Example

        .. code-block:: python

            def gen():
                print('working...')
                yield 1; yield 10; yield 100

            query = Enumerable(gen()).select(lambda e: e * 1000)
            print('go!')
            for e in query:
                print(e)

            # output:
            # go!
            # working...
            # 1000
            # 10000
            # 100000
        '''

    def __len__(self) -> int:
        '''
        Returns the number of elements in the sequence. Prefers calling `__len__()` on the wrapped iterable
        if available, otherwise, calls `self.count()`.

        Example
            >>> en = Enumerable([1, 10, 100])
            >>> len(en)
            3
        '''

    def __reversed__(self) -> Iterator[TSource_co]:
        '''
        Inverts the order of the elements in the sequence. Prefers calling `__reversed__()` on the wrapped
        iterable if available, otherwise, calls `self.reverse()`.

        Example
            >>> ints = [1, 10, 100]
            >>> en = Enumerable(ints)
            >>> for e in reversed(en):
            ...     print(e)
            100
            10
            1
        '''

    @staticmethod
    def _raise_empty_sequence() -> NoReturn: ...  # internal

    @overload
    def aggregate(self,
        __seed: TAccumulate,
        __func: Callable[[TAccumulate, TSource_co], TAccumulate],
        __result_selector: Callable[[TAccumulate], TResult],
    ) -> TResult:
        '''
        Applies an accumulator function over the sequence. The seed is used as the initial
        accumulator value, and the result_selector is used to select the result value.

        Example
            >>> fruits = ['apple', 'mango', 'orange', 'passionfruit', 'grape']
            >>> Enumerable(fruits).aggregate('banana', lambda acc, e: e if len(e) > len(acc) else acc, str.upper)
            'PASSIONFRUIT'
        '''

    @overload
    def aggregate(self,
        __seed: TAccumulate,
        __func: Callable[[TAccumulate, TSource_co], TAccumulate],
    ) -> TAccumulate:
        '''
        Applies an accumulator function over the sequence. The seed is used as the initial
        accumulator value

        Example
            >>> words = 'the quick brown fox jumps over the lazy dog'.split(' ')
            >>> Enumerable(words).aggregate('end', lambda acc, e: f'{e} {acc}')
            'dog lazy the over jumps fox brown quick the end'
        '''

    @overload
    def aggregate(self,
        __func: Callable[[TAccumulate, TSource_co], TAccumulate],
    ) -> TAccumulate:
        '''
        Applies an accumulator function over the sequence. Raises `InvalidOperationError` if
        there is no value in the sequence.

        Example
            >>> words = 'the quick brown fox jumps over the lazy dog'.split(' ')
            >>> Enumerable(words).aggregate(lambda acc, e: f'{e} {acc}')
            'dog lazy the over jumps fox brown quick the'

        Example
            >>> Enumerable.range(1, 10).aggregate(lambda acc, e: acc * e)
            3628800
        '''

    def all(self, predicate: Callable[[TSource_co], bool]) -> bool:
        '''
        Tests whether all elements of the sequence satisfy a condition.

        Example
            >>> ints = [1, 3, 5, 7, 9]
            >>> Enumerable(ints).all(lambda e: e % 2 == 1)
            True
        '''

    @overload
    def any(self) -> bool:
        '''
        Tests whether the sequence has any elements.

        Example
            >>> Enumerable([]).any()
            False
            >>> Enumerable([1]).any()
            True
        '''

    @overload
    def any(self, __predicate: Callable[[TSource_co], bool]) -> bool:
        '''
        Tests whether any element of the sequence satisfy a condition.

        Example
            >>> ints = [1, 3, 5, 7, 9]
            >>> Enumerable(ints).any(lambda e: e % 2 == 0)
            False
        '''

    def append(self, element: TSource_co) -> Enumerable[TSource_co]:  # type: ignore
        '''
        Appends a value to the end of the sequence. Again, this does not affect the original wrapped
        object.

        Example
            >>> ints = [1, 3, 5, 7, 9]
            >>> Enumerable(ints).append(11).to_list()
            [1, 3, 5, 7, 9, 11]
            >>> ints
            [1, 3, 5, 7, 9]
        '''

    def as_cached(self, *, cache_capacity: Optional[int] = None) -> CachedEnumerable[TSource_co]:
        '''
        Returns a CachedEnumerable to cache the enumerated results in this query so that if the wrapped
        iterable is not repeatable (e.g. generator object), it will be repeatable.

        By default, ``Enumerable`` s constructed from nonrepeatable sources cannot be enumerated multiple
        times, for example

        .. code-block:: python

            def gen():
                yield 1
                yield 0
                yield 3

            query = Enumerable(gen())
            print(query.count())
            print(query.where(lambda x: x > 0).to_list())

        prints ``3`` followed by an empty list ``[]``. This is because the ``.count()`` exhausts the
        contents in the generator before the second query is run.

        To avoid the issue, use this method which saves the results along the way.
    
        .. code-block:: python

            query = Enumerable(gen()).as_cached()
            print(query.count())
            print(query.take(2).to_list())
            print(query.where(lambda x: x > 0).to_list())


        printing ``3``, ``[1, 0]`` and ``[1, 3]``.

        This is an alternative way to deal with non-repeatable sources other than passing function
        (``query = Enumerable(gen)``) or solidifying the source in advance
        (``query = Enumerable(list(gen))``).
        This method is useless if you have constructed an Enumerable from a repeatable source such as
        a builtin list, an iterable factory mentioned above, or other ``Enumerable``'s query methods.

        If cache_capacity is None, it is infinite.

        Raises `InvalidOperationError` if cache_capacity is negative.

        The behavior of this method differs from that of ``CachedEnumerable``.

        Revisions:
            - v0.1.1: New.
        '''

    def as_more(self) -> MoreEnumerable[TSource_co]:
        '''
        Returns a MoreEnumerable that has more non-standard query methods available.

        Example
            >>> Enumerable([1, 2, 3]).as_more()

        Revisions:
            - v0.2.0: New.
        '''

    @overload
    def average(self: Enumerable[SupportsAverage[TResult]]) -> TResult:
        '''
        Computes the average value of the sequence. Raises `InvalidOperationError` if there
        is no value.

        The returned type is the type of the expression
        `(elem1 + elem2 + ...) / cast(int, ...)`.

        Example
            >>> ints = [1, 3, 5, 9, 11]
            >>> Enumerable(ints).average()
            5.8
        '''

    @overload
    def average(self, __selector: Callable[[TSource_co], SupportsAverage[TResult]]) -> TResult:
        '''
        Computes the average value of the sequence using the selector. Raises
        `InvalidOperationError` if there is no value.

        The returned type is the type of the expression
        `(selector(elem1) + selector(elem2) + ...) / cast(int, ...)`.

        Example
            >>> strs = ['1', '3', '5', '9', '11']
            >>> Enumerable(strs).average(lambda e: int(e) * 1000)
            5800.0
        '''

    @overload
    def average2(self: Enumerable[SupportsAverage[TResult]],
        __default: TDefault,
    ) -> Union[TResult, TDefault]:
        '''
        Computes the average value of the sequence. Returns `default` if there is no value.

        The returned type is the type of the expression
        `(elem1 + elem2 + ...) / cast(int, ...)` or `TDefault`.

        Example
            >>> Enumerable([1, 2]).average2(0)
            1.5
            >>> Enumerable([]).average2(0)
            0
        '''

    @overload
    def average2(self,
        __selector: Callable[[TSource_co], SupportsAverage[TResult]],
        __default: TDefault,
    ) -> Union[TResult, TDefault]:
        '''
        Computes the average value of the sequence using the selector. Returns `default` if there
        is no value.

        The returned type is the type of the expression
        `(selector(elem1) + selector(elem2) + ...) / cast(int, ...)` or `TDefault`.

        Example
            >>> Enumerable([]).average2(lambda e: int(e) * 1000, 0)
            0
        '''

    def cast(self, __t_result: Type[TResult]) -> Enumerable[TResult]:
        '''
        Casts the elements to the specified type.
        
        This method does not change anything. It returns the original Enumerable reference unchanged.

        Example
            .. code-block:: python

                query: Enumerable[object] = ...
                same_query: Enumerable[int] = query.cast(int)
        '''

    # nonstanard: .NET returns fix-size arrays as elements instead
    def chunk(self, size: int) -> Enumerable[MutableSequence[TSource_co]]:
        '''
        Splits the elements of a sequence into chunks of size at most the provided size. Raises
        `InvalidOperationError` if `size` is less than 1.

        Example
            .. code-block:: python

                >>> def source(i):
                ...     while True:
                ...         yield i
                ...         i *= 3

                >>> en = Enumerable(source(1)).chunk(4).take(3)
                >>> for chunk in en:
                ...     print(chunk)
                [1, 3, 9, 27]
                [81, 243, 729, 2187]
                [6561, 19683, 59049, 177147]

        Revisions:
            - v1.0.0: New.
        '''

    def concat(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        '''
        Concatenates two sequences.

        Example
            >>> en1 = Enumerable([1, 2, 3])
            >>> en2 = Enumerable([1, 2, 4])
            >>> en1.concat(en2).to_list()
            [1, 2, 3, 1, 2, 4]
        '''

    @overload
    def contains(self, value: object) -> bool:
        '''
        Tests whether the sequence contains the specified element using `==`.

        This method always uses a generic element-finding method (O(n)) regardless the implementation
        of the wrapped iterable.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100

                >>> Enumerable(gen()).contains(11)
                False
        '''

    @overload
    def contains(self, value: TOther, __comparer: Callable[[TSource_co, TOther], bool]) -> bool:
        '''
        Tests whether the sequence contains the specified element using the provided comparer that
        returns True if two values are equal.

        Example
            >>> ints = [1, 3, 5, 7, 9]
            >>> Enumerable(ints).contains('9', lambda x, y: str(x) == y)
            True
        '''

    @overload
    def count(self) -> int:
        '''
        Returns the number of elements in the sequence.

        This method always uses a generic length-finding method (O(n)) regardless the implementation
        of the wrapped iterable.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100

                >>> Enumerable(gen()).count()
                3
        '''

    @overload
    def count(self, __predicate: Callable[[TSource_co], bool]) -> int:
        '''
        Returns the number of elements that satisfy the condition.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100

                >>> Enumerable(gen()).count(lambda e: e % 10 == 0)
                2
        '''

    def default_if_empty(self,
        default: TDefault,
    ) -> Union[Enumerable[TSource_co], Enumerable[TDefault]]:
        '''
        Returns the elements of the sequence or the provided value in a singleton collection if
        the sequence is empty.

        Example
            >>> Enumerable([]).default_if_empty(0).to_list()
            [0]
            >>> Enumerable([44, 45, 56]).default_if_empty(0).to_list()
            [44, 45, 56]
        '''

    def distinct(self) -> Enumerable[TSource_co]:
        '''
        Returns distinct elements from the sequence.

        Example
            >>> ints = [1, 4, 5, 6, 4, 3, 1, 99]
            >>> Enumerable(ints).distinct().to_list()
            [1, 4, 5, 6, 3, 99]

        Revisions:
            - v0.2.1: Added preliminary support for unhashable values.
        '''

    def distinct_by(self, key_selector: Callable[[TSource_co], object]) -> Enumerable[TSource_co]:
        '''
        Returns distinct elements from the sequence where "distinctness" is determined by the value
        returned by the selector.

        Example
            >>> ints = [1, 4, 5, 6, 4, 3, 1, 99]
            >>> Enumerable(ints).distinct_by(lambda x: x // 2).to_list()
            [1, 4, 6, 3, 99]

        Revisions:
            - v1.0.0: New. The method with same name (but different return type) in MoreEnumerable class
              was removed.
        '''

    @overload
    def element_at(self, index: int) -> TSource_co:
        '''
        Returns the element at specified index in the sequence. `IndexOutOfRangeError` is raised if
        no such element exists.

        If the index is negative, it means counting from the end.

        This method always uses a generic list element-finding method (O(n)) regardless the
        implementation of the wrapped iterable.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100

                >>> Enumerable(gen()).element_at(1)
                10

                >>> Enumerable(gen()).element_at(-1)
                100

        Revisions:
            - v1.0.0: Added support for negative index.
        '''

    @overload
    def element_at(self, index: int, __default: TDefault) -> Union[TSource_co, TDefault]:
        '''
        Returns the element at specified index in the sequence. Default value is returned if no
        such element exists.

        If the index is negative, it means counting from the end.

        This method always uses a generic list element-finding method (O(n)) regardless the
        implementation of the wrapped iterable.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100

                >>> Enumerable(gen()).element_at(3, 0)
                0

        Revisions:
            - v1.0.0: Added support for negative index.
        '''

    @staticmethod
    def empty() -> Enumerable[TSource_co]:
        '''
        Returns an empty enumerable.

        Example
            >>> en := Enumerable.empty()
            <types_linq.enumerable.Enumerable at 0x00000000000>
            >>> en.to_list()
            []
        '''

    def except1(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        '''
        Produces the set difference of two sequences: self - second.

        Note ``except`` is a keyword in Python.

        Example
            >>> ints = [1, 2, 3, 4, 5]
            >>> Enumerable(ints).except1([1, 3, 5, 7, 9]).to_list()
            [2, 4]

        Revisions:
            - v0.2.1: Added preliminary support for unhashable values.
        '''

    def except_by(self,
        second: Iterable[TKey],
        key_selector: Callable[[TSource_co], TKey],
    ) -> Enumerable[TSource_co]:
        '''
        Produces the set difference of two sequences: self - second, according to a key selector that
        determines "distinctness".

        Example
            >>> first = [(16, 'x'), (9, 'y'), (12, 'd'), (16, 't')]
            >>> second = ['y', 'd']
            >>> Enumerable(first).except_by(second, lambda x: x[1]).to_list()
            [(16, 'x'), (16, 't')]

        Revisions:
            - v1.0.0: New. The method with same name (but different usage) in MoreEnumerable class was
              renamed as ``except_by2()`` to accommodate this.
        '''

    @overload
    def first(self) -> TSource_co:
        '''
        Returns the first element of the sequence. Raises `InvalidOperationError` if there is no
        first element.

        This method always uses a generic method to enumerate the first element regardless the
        implementation of the wrapped iterable.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100

                >>> Enumerable(gen()).first()
                1
        '''

    @overload
    def first(self, __predicate: Callable[[TSource_co], bool]) -> TSource_co:
        '''
        Returns the first element of the sequence that satisfies the condition. Raises
        `InvalidOperationError` if no such element exists.

        Example
            >>> ints = [1, 3, 5, 7, 9, 11, 13]
            >>> Enumerable(ints).first(lambda e: e > 10)
            11
        '''

    @overload
    def first2(self, __default: TDefault) -> Union[TSource_co, TDefault]:
        '''
        Returns the first element of the sequence or a default value if there is no such
        element.

        This method always uses a generic method to enumerate the first element regardless the
        implementation of the wrapped iterable.

        Example
            .. code-block:: python

                >>> def gen(ok: bool):
                ...     if ok:
                ...         yield 1; yield 10; yield 100

                >>> Enumerable(gen(True)).first2(0)
                1
                >>> Enumerable(gen(False)).first2(0)
                0
        '''

    @overload
    def first2(self,
        __predicate: Callable[[TSource_co], bool],
        __default: TDefault,
    ) -> Union[TSource_co, TDefault]:
        '''
        Returns the first element of the sequence that satisfies the condition or a default value if
        no such element exists.

        Example
            >>> ints = [1, 3, 5, 7, 9, 11, 13]
            >>> Enumerable(ints).first2(lambda e: e > 100, 100)
            100
        '''

    @overload
    def group_by(self,
        key_selector: Callable[[TSource_co], TKey],
        value_selector: Callable[[TSource_co], TValue],
        __result_selector: Callable[[TKey, Enumerable[TValue]], TResult],
    ) -> Enumerable[TResult]:
        '''
        Groups the elements of the sequence according to specified key selector and value selector. Then
        it returns the result value using each grouping and its key.

        Example
            .. code-block:: python

                >>> pets_list = [
                ...     ('Barley', 8.3), ('Boots', 4.9), ('Whiskers', 1.5), ('Daisy', 4.3),
                ...     ('Roman', 8.6), ('Fangus', 8.6), ('Roam', 2.2), ('Roll', 1.4),
                ... ]

                >>> en = Enumerable(pets_list).group_by(
                ...     lambda pet: math.floor(pet[1]),
                ...     lambda pet: pet[0],
                ...     lambda age_floored, names: (age_floored, names.to_set()),
                ... )

                >>> for obj in en:
                ...     print(obj)
                (8, {'Fangus', 'Roman', 'Barley'})
                (4, {'Boots', 'Daisy'})
                (1, {'Roll', 'Whiskers'})
                (2, {'Roam'})

        Revisions:
            - v0.2.1: Added preliminary support for unhashable keys.
        '''

    @overload
    def group_by(self,
        key_selector: Callable[[TSource_co], TKey],
        value_selector: Callable[[TSource_co], TValue],
    ) -> Enumerable[Grouping[TKey, TValue]]:
        '''
        Groups the elements of the sequence according to specified key selector and value selector.

        Example
            .. code-block:: python

                >>> en = Enumerable(pets_list).group_by(
                ...     lambda pet: math.floor(pet[1]),
                ...     lambda pet: pet[0],
                ... )

                >>> for grouping in en:
                ...     print(grouping.key, grouping.to_set())
                8 {'Fangus', 'Roman', 'Barley'}
                4 {'Boots', 'Daisy'}
                1 {'Roll', 'Whiskers'}
                2 {'Roam'}

        Revisions:
            - v0.2.1: Added preliminary support for unhashable keys.
        '''

    @overload
    def group_by2(self,
        key_selector: Callable[[TSource_co], TKey],
        __result_selector: Callable[[TKey, Enumerable[TSource_co]], TResult],
    ) -> Enumerable[TResult]:
        '''
        Groups the elements of the sequence according to a specified key selector function and creates a
        result value using each grouping and its key.

        Example
            .. code-block:: python

                >>> en = Enumerable(pets_list).group_by2(
                ...     lambda pet: math.floor(pet[1]),
                ...     lambda age_floored, pets: (age_floored, pets.to_list()),
                ... )

                >>> for obj in en:
                ...     print(obj)
                (8, [('Barley', 8.3), ('Roman', 8.6), ('Fangus', 8.6)])
                (4, [('Boots', 4.9), ('Daisy', 4.3)])
                (1, [('Whiskers', 1.5), ('Roll', 1.4)])
                (2, [('Roam', 2.2)])

        Revisions:
            - v0.2.1: Added preliminary support for unhashable keys.
        '''

    @overload
    def group_by2(self,
        key_selector: Callable[[TSource_co], TKey],
    ) -> Enumerable[Grouping[TKey, TSource_co]]:
        '''
        Groups the elements of the sequence according to a specified key selector function.

        Example
            .. code-block:: python

                >>> en = Enumerable(pets_list).group_by2(
                ...     lambda pet: math.floor(pet[1]),
                ... )

                >>> for grouping in en:
                ...     print(grouping.key, grouping.to_list())
                8 [('Barley', 8.3), ('Roman', 8.6), ('Fangus', 8.6)]
                4 [('Boots', 4.9), ('Daisy', 4.3)]
                1 [('Whiskers', 1.5), ('Roll', 1.4)]
                2 [('Roam', 2.2)]

        Revisions:
            - v0.2.1: Added preliminary support for unhashable keys.
        '''

    def group_join(self,
        inner: Iterable[TInner],
        outer_key_selector: Callable[[TSource_co], TKey],
        inner_key_selector: Callable[[TInner], TKey],
        result_selector: Callable[[TSource_co, Enumerable[TInner]], TResult],
    ) -> Enumerable[TResult]:
        '''
        Correlates the elements of two sequences based on equality of keys and groups the results using the
        selector.

        In normal cases, the iteration preserves order of elements in self (outer), and for each element in
        self, the order of matching elements from inner.
        
        Unhashable keys are supported (where hashibility is determined by checking `typing.Hashable`). If any
        keys formed by key selectors involve such types, the order is unspecified.

        Example
            .. code-block:: python

                >>> class Person(NamedTuple):
                ...     name: str
                >>> class Pet(NamedTuple):
                ...     name: str
                ...     owner: Person

                >>> magnus = Person('Hedlund, Magnus')
                >>> terry = Person('Adams, Terry')
                >>> charlotte = Person('Weiss, Charlotte')
                >>> poor = Person('Animal, No')
                >>> barley = Pet('Barley', owner=terry)
                >>> boots = Pet('Boots', owner=terry)
                >>> whiskers = Pet('Whiskers', owner=charlotte)
                >>> daisy = Pet('Daisy', owner=magnus)
                >>> roman = Pet('Roman', owner=terry)

                >>> people = [magnus, terry, charlotte, poor]
                >>> pets = [barley, boots, whiskers, daisy, roman]

                >>> en = Enumerable(people).group_join(
                ...     pets,
                ...     lambda person: person,
                ...     lambda pet: pet.owner,
                ...     lambda person, pet_collection: (
                ...         person.name,
                ...         pet_collection.select(lambda pet: pet.name).to_set(),
                ...     ),
                ... )

                >>> for obj in en:
                ...     print(obj)
                ('Hedlund, Magnus', {'Daisy'})
                ('Adams, Terry', {'Boots', 'Roman', 'Barley'})
                ('Weiss, Charlotte', {'Whiskers'})
                ('Animal, No', set())

        Revisions:
            - v0.2.1: Added preliminary support for unhashable keys.
        '''

    def intersect(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        '''
        Produces the set intersection of two sequences: self * second.

        Example
            >>> ints = [1, 3, 5, 7, 9, 11]
            >>> Enumerable(ints).intersect([1, 2, 3, 4, 5]).to_list()
            [1, 3, 5]

        Revisions:
            - v0.2.1: Added preliminary support for unhashable values.
        '''

    def intersect_by(self,
        second: Iterable[TKey],
        key_selector: Callable[[TSource_co], TKey],
    ) -> Enumerable[TSource_co]:
        '''
        Produces the set intersection of two sequences: self * second according to a
        specified key selector.

        Example
            >>> strs = ['+1', '-3', '+5', '-7', '+9', '-11']
            >>> Enumerable(strs).intersect_by([1, 2, 3, 5, 9], lambda x: abs(int(x))).to_list()
            ['+1', '-3', '+5', '+9']

        Revisions:
            - v1.0.0: New.
        '''

    def join(self,
        inner: Iterable[TInner],
        outer_key_selector: Callable[[TSource_co], TKey],
        inner_key_selector: Callable[[TInner], TKey],
        result_selector: Callable[[TSource_co, TInner], TResult],
    ) -> Enumerable[TResult]:
        '''
        Correlates the elements of two sequences based on matching keys.

        In normal cases, the iteration preserves order of elements in self (outer), and for each element in
        self, the order of matching elements from inner.
        
        Unhashable keys are supported (where hashibility is determined by checking `typing.Hashable`). If any
        keys formed by key selectors involve such types, the order is unspecified.

        Example
            .. code-block:: python

                # Please refer to group_join() for definition of people and pets

                >>> en = Enumerable(people).join(
                ...     pets,
                ...     lambda person: person,
                ...     lambda pet: pet.owner,
                ...     lambda person, pet: (person.name, pet.name),
                ... )

                >>> for obj in en:
                ...     print(obj)
                ('Hedlund, Magnus', 'Daisy')
                ('Adams, Terry', 'Barley')
                ('Adams, Terry', 'Boots')
                ('Adams, Terry', 'Roman')
                ('Weiss, Charlotte', 'Whiskers')

        Revisions:
            - v0.2.1: Added preliminary support for unhashable keys.
        '''

    @overload
    def last(self) -> TSource_co:
        '''
        Returns the last element of the sequence. Raises `InvalidOperationError` if there is no first
        element.

        This method always uses a generic method to enumerate the last element (O(n)) regardless the
        implementation of the wrapped iterable.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100

                >>> Enumerable(gen()).last()
                100
        '''

    @overload
    def last(self, __predicate: Callable[[TSource_co], bool]) -> TSource_co:
        '''
        Returns the last element of the sequence that satisfies the condition. Raises
        `InvalidOperationError` if no such element exists.

        Example
            >>> ints = [1, 3, 5, 7, 9, 11, 13]
            >>> Enumerable(ints).last(lambda e: e < 10)
            9
        '''

    @overload
    def last2(self, __default: TDefault) -> Union[TSource_co, TDefault]:
        '''
        Returns the last element of the sequence or a default value if there is no such
        element.

        This method always uses a generic method to enumerate the last element (O(n)) regardless the
        implementation of the wrapped iterable.

        Example
            .. code-block:: python

                >>> def gen(ok: bool):
                ...     if ok:
                ...         yield 1; yield 10; yield 100

                >>> Enumerable(gen(True)).last2(9999)
                100
                >>> Enumerable(gen(False)).last2(9999)
                9999
        '''

    @overload
    def last2(self,
        __predicate: Callable[[TSource_co], bool],
        __default: TDefault,
    ) -> Union[TSource_co, TDefault]:
        '''
        Returns the last element of the sequence that satisfies the condition or a default value if
        no such element exists.

        Example
            >>> ints = [13, 11, 9, 7, 5, 3, 1]
            >>> Enumerable(ints).last2(lambda e: e < 0, 9999)
            9999
        '''

    @overload
    def max(self: Enumerable[TSupportsLessThan]) -> TSupportsLessThan:
        '''
        Returns the maximum value in the sequence. Raises `InvalidOperationError` if there is no value.

        Example
            >>> nums = [1, 5, 2.2, 5, 1, 2]
            >>> Enumerable(nums).max()
            5
        '''

    @overload
    def max(self, __result_selector: Callable[[TSource_co], TSupportsLessThan]) -> TSupportsLessThan:
        '''
        Invokes a transform function on each element of the sequence and returns the maximum of the
        resulting values. Raises `InvalidOperationError` if there is no value.

        Example
            >>> strs = ['aaa', 'bb', 'c', 'dddd']
            >>> Enumerable(strs).max(len)
            4
        '''

    @overload
    def max2(self: Enumerable[TSupportsLessThan],
        __default: TDefault,
    ) -> Union[TSupportsLessThan, TDefault]:
        '''
        Returns the maximum value in the sequence, or the default one if there is no value.

        Example
            >>> Enumerable([]).max2(0)
            0
        '''

    @overload
    def max2(self,
        __result_selector: Callable[[TSource_co], TSupportsLessThan],
        __default: TDefault,
    ) -> Union[TSupportsLessThan, TDefault]:
        '''
        Invokes a transform function on each element of the sequence and returns the maximum of the
        resulting values. Returns the default one if there is no value.

        Example
            >>> Enumerable([]).max2(len, 0)
            0
            >>> Enumerable(['a']).max2(len, 0)
            1
        '''

    @overload
    def max_by(self, key_selector: Callable[[TSource_co], TSupportsLessThan]) -> TSource_co:
        '''
        Returns the maximal element of the sequence based on the given key selector. Raises
        `InvalidOperationError` if there is no value.

        Example
            >>> strs = ['aaa', 'bb', 'c', 'dddd']
            >>> Enumerable(strs).max_by(len)
            'dddd'

        Revisions:
            - v1.0.0: New.
        '''

    @overload
    def max_by(self,
        key_selector: Callable[[TSource_co], TKey],
        __comparer: Callable[[TKey, TKey], int],
    ) -> TSource_co:
        '''
        Returns the maximal element of the sequence based on the given key selector and the comparer.
        Raises `InvalidOperationError` if there is no value.

        Such comparer takes two values and return positive ints when lhs > rhs, negative ints
        if lhs < rhs, and 0 if they are equal.

        Revisions:
            - v1.0.0: New.
        '''

    @overload
    def min(self: Enumerable[TSupportsLessThan]) -> TSupportsLessThan:
        '''
        Returns the minimum value in the sequence. Raises `InvalidOperationError` if there is no value.
        '''

    @overload
    def min(self, __result_selector: Callable[[TSource_co], TSupportsLessThan]) -> TSupportsLessThan:
        '''
        Invokes a transform function on each element of the sequence and returns the minimum of the
        resulting values. Raises `InvalidOperationError` if there is no value.
        '''

    @overload
    def min2(self: Enumerable[TSupportsLessThan],
        __default: TDefault,
    ) -> Union[TSupportsLessThan, TDefault]:
        '''
        Returns the minimum value in the sequence, or the default one if there is no value.
        '''

    @overload
    def min2(self,
        __result_selector: Callable[[TSource_co], TSupportsLessThan],
        __default: TDefault,
    ) -> Union[TSupportsLessThan, TDefault]:
        '''
        Invokes a transform function on each element of the sequence and returns the minimum of the
        resulting values. Returns the default one if there is no value.
        '''

    @overload
    def min_by(self, key_selector: Callable[[TSource_co], TSupportsLessThan]) -> TSource_co:
        '''
        Returns the minimal element of the sequence based on the given key selector. Raises
        `InvalidOperationError` if there is no value.

        Revisions:
            - v1.0.0: New.
        '''

    @overload
    def min_by(self,
        key_selector: Callable[[TSource_co], TKey],
        __comparer: Callable[[TKey, TKey], int],
    ) -> TSource_co:
        '''
        Returns the minimal element of the sequence based on the given key selector and the comparer.
        Raises `InvalidOperationError` if there is no value.

        Such comparer takes two values and return positive ints when lhs > rhs, negative ints
        if lhs < rhs, and 0 if they are equal.

        Revisions:
            - v1.0.0: New.
        '''

    def of_type(self, t_result: Type[TResult]) -> Enumerable[TResult]:
        '''
        Filters elements based on the specified type.

        Builtin `isinstance()` is used.

        Example
            >>> lst = [1, 14, object(), True, []]
            >>> Enumerable(lst).of_type(int).to_list()
            [1, 14, True]
        '''

    @overload
    def order_by(self,
        key_selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> OrderedEnumerable[TSource_co, TSupportsLessThan]:
        '''
        Sorts the elements of the sequence in ascending order according to a key.

        Example
            >>> ints = [8, 4, 5, 2]
            >>> Enumerable(ints).order_by(lambda e: e).to_list()
            [2, 4, 5, 8]

        Example
            .. code-block:: python

                >>> class Pet(NamedTuple):
                ...     name: str
                ...     age: int

                >>> pets = [Pet('Barley', 8), Pet('Boots', 4), Pet('Roman', 5)]
                >>> Enumerable(pets).order_by(lambda p: p.age) \\
                ...     .select(lambda p: p.name)              \\
                ...     .to_list()
                ['Boots', 'Roman', 'Barley']

        Subsequent ordering is supported. See ``OrderedEnumerable``.
        '''

    @overload
    def order_by(self,
        key_selector: Callable[[TSource_co], TKey],
        __comparer: Callable[[TKey, TKey], int],
    ) -> OrderedEnumerable[TSource_co, TKey]:
        '''
        Sorts the elements of the sequence in ascending order by using a specified comparer.

        Such comparer takes two values and return positive ints when lhs > rhs, negative ints
        if lhs < rhs, and 0 if they are equal. In fact, this overload should not be used
        (see `Sorting HOW TO <https://docs.python.org/3/howto/sorting.html#the-old-way-using-the-cmp-parameter>`_).

        Example
            >>> Enumerable(pets).order_by(lambda p: p, lambda pl, pr: pl.age - pr.age) \\
            ...     .select(lambda p: p.name)                                          \\
            ...     .to_list()
            ['Boots', 'Roman', 'Barley']
        '''

    @overload
    def order_by_descending(self,
        key_selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> OrderedEnumerable[TSource_co, TSupportsLessThan]:
        '''
        Sorts the elements of the sequence in descending order according to a key.

        Example
            >>> ints = [8, 4, 5, 2]
            >>> Enumerable(ints).order_by_descending(lambda e: e).to_list()
            [8, 5, 4, 2]
        '''

    @overload
    def order_by_descending(self,
        key_selector: Callable[[TSource_co], TKey],
        __comparer: Callable[[TKey, TKey], int],
    ) -> OrderedEnumerable[TSource_co, TKey]:
        '''
        Sorts the elements of the sequence in descending order by using a specified comparer.

        Such comparer takes two values and return positive ints when lhs > rhs, negative ints
        if lhs < rhs, and 0 if they are equal.
        '''

    def prepend(self, element: TSource_co) -> Enumerable[TSource_co]:  # type: ignore
        '''
        Adds a value to the beginning of the sequence. Again, this does not affect the original
        wrapped object.

        Example
            >>> ints = [1, 3, 5, 7, 9]
            >>> Enumerable(ints).prepend(-1).to_list()
            [-1, 1, 3, 5, 7, 9]
        '''

    # count: Optional[int] is nonstandard behavior
    @staticmethod
    def range(start: int, count: Optional[int]) -> Enumerable[int]:
        '''
        Generates a sequence of `count` integral numbers from `start`, incrementing each by one.

        If `count` is `None`, the sequence is infinite. Raises `InvalidOperationError` if `count`
        is negative.

        Example
            >>> Enumerable.range(-5, 6).to_list()
            [-5, -4, -3, -2, -1, 0]
        '''

    # count: Optional[int] is nonstandard behavior
    @staticmethod
    def repeat(value: TResult, count: Optional[int] = None) -> Enumerable[TResult]:
        '''
        Generates a sequence that contains one repeated value.

        If `count` is `None`, the sequence is infinite. Raises `InvalidOperationError` if `count`
        is negative.

        Example
            >>> Enumerable.repeat(0, 6).to_list()
            [0, 0, 0, 0, 0, 0]
        '''

    def reverse(self) -> Enumerable[TSource_co]:
        '''
        Inverts the order of the elements in the sequence.

        This method always uses a generic reverse traversal method regardless the implementation of
        the wrapped iterable.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100

                >>> Enumerable(gen()).reverse().to_list()
                [100, 10, 1]
        '''

    def select(self, selector: Callable[[TSource_co], TResult]) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence into a new form.

        Example
            >>> ints = [1, 3, 5, 7, 9]
            >>> Enumerable(ints).select(lambda e: '*' * e).to_list()
            ['*', '***', '*****', '*******', '*********']
        '''

    def select2(self, selector: Callable[[TSource_co, int], TResult]) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence into a new form by incorporating the indices.

        Example
            >>> ints = [1, 3, 5, 7, 9]
            >>> Enumerable(ints).select2(lambda e, i: e * (i + 1)).to_list()
            [1, 6, 15, 28, 45]
        '''

    @overload
    def select_many(self,
        collection_selector: Callable[[TSource_co], Iterable[TCollection]],
        __result_selector: Callable[[TSource_co, TCollection], TResult],
    ) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence into an iterable, flattens the resulting sequence
        into one sequence, then calls result_selector on each element therein.

        Example
            .. code-block:: python

                >>> pet_owners = [
                ...     {'name': 'Higa', 'pets': ['Scruffy', 'Sam']},
                ...     {'name': 'Ashkenazi', 'pets': ['Walker', 'Sugar']},
                ...     {'name': 'Hines',  'pets': ['Dusty']},
                ... ]

                >>> en = Enumerable(pet_owners).select_many(
                ...     lambda owner: owner['pets'],
                ...     lambda owner, name: (name, owner['name']),
                ... )

                >>> for tup in en:
                ...     print(tup)
                ('Scruffy', 'Higa')
                ('Sam', 'Higa')
                ('Walker', 'Ashkenazi')
                ('Sugar', 'Ashkenazi')
                ('Dusty', 'Hines')
        '''

    @overload
    def select_many(self,
        __selector: Callable[[TSource_co], Iterable[TResult]],
    ) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence to an iterable and flattens the resultant sequences.

        Example
            >>> sentences = ['i select things', 'i do many times']
            >>> Enumerable(sentences).select_many(str.split).to_list()
            ['i', 'select', 'things', 'i', 'do', 'many', 'times']
        '''

    @overload
    def select_many2(self,
        collection_selector: Callable[[TSource_co, int], Iterable[TCollection]],
        __result_selector: Callable[[TSource_co, TCollection], TResult],
    ) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence into an iterable, flattens the resulting sequence
        into one sequence, then calls result_selector on each element therein. The indices of
        source elements are used.
        '''

    @overload
    def select_many2(self,
        __selector: Callable[[TSource_co, int], Iterable[TResult]],
    ) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence to an iterable and flattens the resultant sequences.
        The indices of source elements are used.

        Example
            >>> dinner = ['Ramen with Egg and Beef', 'Gyoza', 'Fried Chicken']
            >>> en = Enumerable(dinner).select_many2(
            ...     lambda e, i: Enumerable(e.split(' '))
            ...         .where(lambda w: w[0].isupper())
            ...         .select(lambda w: f'Table {i}: {w}'),
            ... )
            >>> for s in en:
            ...     print(s)
            Table 0: Ramen
            Table 0: Egg  
            Table 0: Beef 
            Table 1: Gyoza
            Table 2: Fried
            Table 2: Chicken
        '''

    @overload
    def sequence_equal(self, second: Iterable[TSource_co]) -> bool:
        '''
        Determines whether two sequences are equal using `==` on each element.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100
                >>> lst = [1, 10, 100]

                >>> Enumerable(gen()).sequence_equal(lst)
                True
        '''

    @overload
    def sequence_equal(self,
        second: Iterable[TOther],
        __comparer: Callable[[TSource_co, TOther], bool],
    ) -> bool:
        '''
        Determines whether two sequences are equal using a comparer that returns True if two values
        are equal, on each element.

        Example
            >>> ints = [1, 3, 5, 7, 9]
            >>> strs = ['1', '3', '5', '7', '9']
            >>> Enumerable(ints).sequence_equal(strs, lambda x, y: str(x) == y)
            True

        Revisions:
            - v0.1.2: New.
        '''

    @overload
    def single(self) -> TSource_co:
        '''
        Returns the only element in the sequence. Raises `InvalidOperationError` if the sequence does not
        contain exactly one element.

        Example
            >>> Enumerable([5]).single()
            5

        Example
            >>> lst = [5, 6]
            >>> try:
            ...     print(Enumerable(lst).single())
            ... except InvalidOperationError:
            ...     print('Collection does not contain exactly one element. Sorry.')
            Collection does not contain exactly one element. Sorry.
        '''

    @overload
    def single(self, __predicate: Callable[[TSource_co], bool]) -> TSource_co:
        '''
        Returns the only element in the sequence that satisfies the condition. Raises `InvalidOperationError`
        if no element satisfies the condition, or more than one do.

        Example
            >>> ints = [1, 3, 5, 7, 9, 11, 9]
            >>> Enumerable(ints).single(lambda e: e > 10)
            11
            >>> try:
            ...     Enumerable(ints).single(lambda e: e == 9)
            ... except InvalidOperationError:
            ...     print('Too many nines!')
            Too many nines!
        '''

    @overload
    def single2(self, __default: TDefault) -> Union[TSource_co, TDefault]:
        '''
        Returns the only element in the sequence or the default value if the sequence is empty. Raises
        `InvalidOperationError` if there are more than one elements in the sequence.

        Example
            >>> Enumerable([]).single2(0)
            0
        '''

    @overload
    def single2(self,
        __predicate: Callable[[TSource_co], bool],
        __default: TDefault,
    ) -> Union[TSource_co, TDefault]:
        '''
        Returns the only element in the sequence that satisfies the condition, or the default value if there is
        no such element. Raises `InvalidOperationError` if there are more than one elements satisfying the
        condition.

        Example
            >>> fruits = ['apple', 'banana', 'mango']
            >>> Enumerable(fruits).single2(lambda e: len(e) > 10, 'sorry')
            'sorry'
        '''

    def skip(self, count: int) -> Enumerable[TSource_co]:
        '''
        Bypasses a specified number of elements in the sequence and then returns the remaining.

        Example
            >>> grades = [59, 82, 70, 56, 92, 98, 85]
            >>> Enumerable(grades).order_by_descending(lambda g: g).skip(3).to_list()
            [82, 70, 59, 56]
        '''

    def skip_last(self, count: int) -> Enumerable[TSource_co]:
        '''
        Returns a new sequence that contains the elements of the current sequence with last `count` elements
        omitted.

        Example
            >>> grades = [59, 82, 70, 56, 92, 98, 85]
            >>> Enumerable(grades).order_by_descending(lambda g: g).skip_last(3).to_list()
            [98, 92, 85, 82]
        '''

    def skip_while(self, predicate: Callable[[TSource_co], bool]) -> Enumerable[TSource_co]:
        '''
        Bypasses elements in the sequence as long as the condition is true and then returns the remaining
        elements.

        Example
            >>> grades = [59, 82, 70, 56, 92, 98, 85]
            >>> Enumerable(grades).order_by_descending(lambda g: g) \\
            ...     .skip_while(lambda g: g >= 80)                  \\
            ...     .to_list()
            [70, 59, 56]
        '''

    def skip_while2(self, predicate: Callable[[TSource_co, int], bool]) -> Enumerable[TSource_co]:
        '''
        Bypasses elements in the sequence as long as the condition is true and then returns the remaining
        elements. The element's index is used in the predicate function.

        Example
            >>> amounts = [500, 250, 900, 800, 650, 400, 150, 550]
            >>> Enumerable(amounts).skip_while2(lambda a, i: a > i * 100).to_list()
            [400, 150, 550]
        '''

    # returning 0 conforms the builtin sum() function
    @overload
    def sum(self: Enumerable[TSupportsAdd]) -> Union[TSupportsAdd, int]:
        '''
        Computes the sum of the sequence, or `0` if the sequence is empty.

        Example
            >>> floats = [.1, .3, .5, .9, 1.1]
            >>> Enumerable(floats).sum()
            2.9000000000000004
        '''

    # returning 0 conforms the builtin sum() function
    @overload
    def sum(self, __selector: Callable[[TSource_co], TSupportsAdd]) -> Union[TSupportsAdd, int]:
        '''
        Computes the sum of the sequence using the selector. Returns `0` if the sequence is empty.

        Example
            >>> floats = [.1, .3, .5, .9, 1.1]
            >>> Enumerable(floats).sum(lambda e: int(e * 1000))
            2900
        '''

    @overload
    def sum2(self: Enumerable[TSupportsAdd],
        __default: TDefault,
    ) -> Union[TSupportsAdd, TDefault]:
        '''
        Computes the sum of the sequence. Returns the default value if it is empty.

        Example
            >>> Enumerable([]).sum2(880)
            880
        '''

    @overload
    def sum2(self,
        __selector: Callable[[TSource_co], TSupportsAdd],
        __default: TDefault,
    ) -> Union[TSupportsAdd, TDefault]:
        '''
        Computes the sum of the sequence using the selector. Returns the default value if it is empty.

        Example
            >>> Enumerable([]).sum2(lambda e: int(e * 1000), 880)
            880
        '''

    @overload
    def take(self, count: int) -> Enumerable[TSource_co]:
        '''
        Returns a specified number of contiguous elements from the start of the sequence.

        Example
            >>> grades = [98, 92, 85, 82, 70, 59, 56]
            >>> Enumerable(grades).take(3).to_list()
            [98, 92, 85]
        '''

    @overload
    def take(self, __index: slice) -> Enumerable[TSource_co]:
        '''
        Produces a subsequence defined by the given slice notation.

        This method always uses a generic list slicing method regardless the implementation of the
        wrapped iterable.

        This method currently is identical to `elements_in()` when it takes a slice.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100; yield 1000; yield 10000

                >>> Enumerable(gen()).take(slice(1, 3)).to_list()
                [10, 100]

        Revisions:
            - v1.0.0: New.
        '''

    def take_last(self, count: int) -> Enumerable[TSource_co]:
        '''
        Returns a new sequence that contains the last `count` elements.

        Example
            >>> grades = [98, 92, 85, 82, 70, 59, 56]
            >>> Enumerable(grades).take_last(3).to_list()
            [70, 59, 56]
        '''

    def take_while(self, predicate: Callable[[TSource_co], bool]) -> Enumerable[TSource_co]:
        '''
        Returns elements from the sequence as long as the condition is true and skips the remaining.

        Example
            >>> strs = ['1', '3', '5', '7', '', '1', '4', '5']
            >>> Enumerable(strs).take_while(lambda g: g).to_list()
            ['1', '3', '5', '7']
        '''

    def take_while2(self, predicate: Callable[[TSource_co, int], bool]) -> Enumerable[TSource_co]:
        '''
        Returns elements from the sequence as long as the condition is true and skips the remaining. The
        element's index is used in the predicate function.
        '''

    @overload
    def to_dict(self,
        key_selector: Callable[[TSource_co], TKey],
        __value_selector: Callable[[TSource_co], TValue],
    ) -> Dict[TKey, TValue]:
        '''
        Enumerates all values and returns a dict containing them. key_selector and value_selector
        are used to select keys and values.
        '''

    @overload
    def to_dict(self,
        key_selector: Callable[[TSource_co], TKey],
    ) -> Dict[TKey, TSource_co]:
        '''
        Enumerates all values and returns a dict containing them. key_selector is used to select
        keys.
        '''

    def to_set(self) -> Set[TSource_co]:
        '''
        Enumerates all values and returns a set containing them.
        '''

    def to_list(self) -> List[TSource_co]:
        '''
        Enumerates all values and returns a list containing them.
        '''

    @overload
    def to_lookup(self,
        key_selector: Callable[[TSource_co], TKey],
        __value_selector: Callable[[TSource_co], TValue],
    ) -> Lookup[TKey, TValue]:
        '''
        Enumerates all values and returns a lookup containing them according to specified key
        selector and value selector. The values within each group are in the same order as in
        self.

        Example
            >>> food = [
            ...     ('main', 'ramen'), ('main', 'noodles'), ('side', 'chicken'),
            ...     ('main', 'spaghetti'), ('snack', 'popcorns'), ('side', 'apples'),
            ...     ('side', 'orange'), ('drink', 'coke'), ('main', 'birthdaycake'),
            ... ]
            >>> lookup = Enumerable(food).to_lookup(lambda e: e[0], lambda e: e[1])
            >>> lookup.select(lambda grouping: grouping.key).to_list()
            ['main', 'side', 'snack', 'drink']
            >>> if 'side' in lookup:
            ...     print(lookup['side'].to_list())
            ['chicken', 'apples', 'orange']

        Revisions:
            - v0.2.1: Added preliminary support for unhashable keys.
        '''

    @overload
    def to_lookup(self,
        key_selector: Callable[[TSource_co], TKey],
    ) -> Lookup[TKey, TSource_co]:
        '''
        Enumerates all values and returns a lookup containing them according to the specified
        key selector. The values within each group are in the same order as in self.

        Revisions:
            - v0.2.1: Added preliminary support for unhashable keys.
        '''

    def union(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        '''
        Produces the set union of two sequences: self + second.

        Example
            >>> gen = (i for i in range(5))
            >>> lst = [5, 3, 9, 7, 5, 9, 3, 7]
            >>> Enumerable(gen).union(lst).to_list()
            [0, 1, 2, 3, 4, 5, 9, 7]

        Revisions:
            - v0.2.1: Added preliminary support for unhashable values.
        '''

    def union_by(self,
        second: Iterable[TSource_co],
        key_selector: Callable[[TSource_co], object],
    ) -> Enumerable[TSource_co]:
        '''
        Produces the set union of two sequences: self + second according to a specified key
        selector.

        Example
            >>> en = Enumerable([1, 9, -2, -7, 14])
            >>> en.union_by([15, 2, -26, -7], abs).to_list()
            [1, 9, -2, -7, 14, 15, -26]  # abs(-2) == abs(2)

        Revisions:
            - v1.0.0: New.
        '''

    def where(self, predicate: Callable[[TSource_co], bool]) -> Enumerable[TSource_co]:
        '''
        Filters the sequence of values based on a predicate.

        Example
            >>> strs = ['apple', 'orange', 'Apple', 'xx', 'Grapes']
            >>> Enumerable(strs).where(str.istitle).to_list()
            ['Apple', 'Grapes']
        '''

    def where2(self, predicate: Callable[[TSource_co, int], bool]) -> Enumerable[TSource_co]:
        '''
        Filters the sequence of values based on a predicate. Each element's index is used in the
        predicate logic.

        Example
            >>> ints = [0, 30, 20, 15, 90, 85, 40, 75]
            >>> Enumerable(ints).where2(lambda e, i: e <= i * 10).to_list()
            [0, 20, 15, 40]
        '''

    @overload
    def zip(self,
        __second: Iterable[TOther],
    ) -> Enumerable[Tuple[TSource_co, TOther]]:
        '''
        Produces a sequence of 2-element tuples from the two sequences.

        Example
            >>> ints = [1, 2, 3, 4]
            >>> dims = ['x', 'y', 'z', 't', 'u', 'v']
            >>> Enumerable(ints).zip(dims).to_list()
            [(1, 'x'), (2, 'y'), (3, 'z'), (4, 't')]
        '''

    @overload
    def zip(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
    ) -> Enumerable[Tuple[TSource_co, TOther, TOther2]]:
        '''
        Revisions
            - v0.1.1: New.
        '''

    @overload
    def zip(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
        __fourth: Iterable[TOther3],
    ) -> Enumerable[Tuple[TSource_co, TOther, TOther2, TOther3]]:
        '''
        Revisions
            - v0.1.1: New.
        '''

    @overload
    def zip(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
        __fourth: Iterable[TOther3],
        __fifth: Iterable[TOther4],
    ) -> Enumerable[Tuple[TSource_co, TOther, TOther2, TOther3, TOther4]]:
        '''
        Revisions
            - v0.1.1: New.
        '''

    @overload
    def zip(self,
        __second: Iterable[Any],
        __third: Iterable[Any],
        __fourth: Iterable[Any],
        __fifth: Iterable[Any],
        __sixth: Iterable[Any],
        *iters: Iterable[Any],
    ) -> Enumerable[Tuple[Any, ...]]:
        '''
        Revisions
            - v0.1.1: New.
        '''

    @overload
    def zip2(self,
        __second: Iterable[TOther],
        __result_selector: Callable[[TSource_co, TOther], TResult],
    ) -> Enumerable[TResult]:
        '''
        Applies a specified function to the corresponding elements of two sequences, producing a
        sequence of the results.

        Example
            >>> ints = [1, 2, 3, 4]
            >>> dims = ['x', 'y', 'z', 't', 'u', 'v']
            >>> Enumerable(ints).zip2(dims, lambda i, d: f'{i}.{d}').to_list()
            ['1.x', '2.y', '3.z', '4.t']
        '''

    @overload
    def zip2(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
        __result_selector: Callable[[TSource_co, TOther, TOther2], TResult],
    ) -> Enumerable[TResult]:
        '''
        Revisions
            - v0.1.1: New.
        '''

    @overload
    def zip2(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
        __fourth: Iterable[TOther3],
        __result_selector: Callable[[TSource_co, TOther, TOther2, TOther3], TResult],
    ) -> Enumerable[TResult]:
        '''
        Revisions
            - v0.1.1: New.
        '''

    @overload
    def zip2(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
        __fourth: Iterable[TOther3],
        __fifth: Iterable[TOther4],
        __result_selector: Callable[[TSource_co, TOther, TOther2, TOther3, TOther4], TResult],
    ) -> Enumerable[TResult]:
        '''
        Revisions
            - v0.1.1: New.
        '''

    @overload
    def zip2(self,
        __second: Iterable[Any],
        __third: Iterable[Any],
        __fourth: Iterable[Any],
        __fifth: Iterable[Any],
        __sixth: Iterable[Any],
        *iters_and_result_selector: Union[Iterable[Any], Callable[..., Any]],
    ) -> Enumerable[Any]:
        '''
        Revisions
            - v0.1.1: New.
        '''

    # Methods below are non-standard. They do not have .NET builtin equivalence and are here just
    # for convenience.

    @overload
    def elements_in(self, __index: slice) -> Enumerable[TSource_co]:
        '''
        Produces a subsequence defined by the given slice notation.

        This method always uses a generic list slicing method regardless the implementation of the
        wrapped iterable.

        This method currently is identical to `take()` when it takes a slice.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100; yield 1000; yield 10000

                >>> Enumerable(gen()).elements_in(slice(1, 3)).to_list()
                [10, 100]
        '''

    @overload
    def elements_in(self, __start: int, __stop: int, __step: int = 1) -> Enumerable[TSource_co]:
        '''
        Produces a subsequence with indices that define a slice.

        This method always uses a generic list slicing method regardless the implementation of the
        wrapped iterable.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 1; yield 10; yield 100; yield 1000; yield 10000

                >>> Enumerable(gen()).elements_in(1, 3).to_list()
                [10, 100]
        '''

    def to_tuple(self) -> Tuple[TSource_co, ...]:
        '''
        Enumerates all values and returns a tuple containing them.

        Revisions:
            - v0.1.2: New.
        '''
