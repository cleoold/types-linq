from typing import Any, Callable, Dict, Generic, Iterable, Iterator, List, Optional, Sequence, Set, Tuple, Type, Union, overload

from .lookup import Lookup
from .grouping import Grouping
from .ordered_enumerable import OrderedEnumerable
from .cached_enumerable import CachedEnumerable
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
        '''

    @overload
    def __getitem__(self, index: int) -> TSource_co:
        '''
        Returns the element at specified index in the sequence. Prefers calling `__getitem__()` on the
        wrapped iterable if available, otherwise, calls `self.element_at()`.
        '''

    @overload
    def __getitem__(self, index: slice) -> Enumerable[TSource_co]:
        '''
        Produces a subsequence defined by the given slice notation. Prefers calling `__getitem__()` on the
        wrapped iterable if available, otherwise, calls `self.elements_in()`.
        '''

    def __iter__(self) -> Iterator[TSource_co]:
        '''
        Returns an iterator that enumerates the values in the sequence.
        '''

    def __len__(self) -> int:
        '''
        Returns the number of elements in the sequence. Prefers calling `__len__()` on the wrapped iterable
        if available, otherwise, calls `self.count()`.
        '''

    def __reversed__(self) -> Iterator[TSource_co]:
        '''
        Inverts the order of the elements in the sequence. Prefers calling `__reversed__()` on the wrapped
        iterable if available, otherwise, calls `self.reverse()`.
        '''

    @overload
    def aggregate(self,
        __seed: TAccumulate,
        __func: Callable[[TAccumulate, TSource_co], TAccumulate],
        __result_selector: Callable[[TAccumulate], TResult],
    ) -> TResult:
        '''
        Applies an accumulator function over the sequence. The seed is used as the initial
        accumulator value, and the result_selector is used to select the result value.
        '''

    @overload
    def aggregate(self,
        __seed: TAccumulate,
        __func: Callable[[TAccumulate, TSource_co], TAccumulate],
    ) -> TAccumulate:
        '''
        Applies an accumulator function over the sequence. The seed is used as the initial
        accumulator value
        '''

    @overload
    def aggregate(self,
        __func: Callable[[TAccumulate, TSource_co], TAccumulate],
    ) -> TAccumulate:
        '''
        Applies an accumulator function over the sequence. Raises `InvalidOperationError` if
        there is no value in the sequence.
        '''

    def all(self, predicate: Callable[[TSource_co], bool]) -> bool:
        '''
        Tests whether all elements of the sequence satisfy a condition.
        '''

    @overload
    def any(self) -> bool:
        '''
        Tests whether the sequence has any elements.
        '''

    @overload
    def any(self, __predicate: Callable[[TSource_co], bool]) -> bool:
        '''
        Tests whether any element of the sequence satisfy a condition.
        '''

    def append(self, element: TSource_co) -> Enumerable[TSource_co]:  # type: ignore
        '''
        Appends a value to the end of the sequence.
        '''

    def as_cached(self, *, cache_capacity: Optional[int] = None) -> CachedEnumerable[TSource_co]:
        '''
        Returns a CachedEnumerable to cache the enumerated results in this query so that if the wrapped
        iterable is not repeatable (e.g. generator object), it will be repeatable.

        By default, `Enumerable`s constructed from nonrepeatable sources cannot be enumerated multiple
        times, for example
        ```py
        def gen():
            yield 1
            yield 0
            yield 3

        query = Enumerable(gen())
        print(query.count())
        print(query.where(lambda x: x > 0).to_list())
        ```
        prints `3` followed by an empty list `[]`. This is because the `.count()` exhausts the contents
        in the generator before the second query is run.

        To avoid the issue, use this method which saves the results along the way.
        ```py
        query = Enumerable(gen()).as_cached()
        print(query.count())
        print(query.take(2).to_list())
        print(query.where(lambda x: x > 0).to_list())
        ```
        printing `3`, `[1, 0]` and `[1, 3]`.

        This is an alternative way to deal with non-repeatable sources other than passing function
        (`query = Enumerable(gen)`) or solidifying the source in advance (`query = Enumerable(list(gen))`).
        This method is useless if you have constructed an Enumerable from a repeatable source such as
        a builtin list, an iterable factory mentioned above, or other `Enumerable`'s query methods.

        If cache_capacity is None, it is infinite.

        Raises `InvalidOperationError` if cache_capacity is negative.

        The behavior of this method differs from that of CachedEnumerable.
        '''

    @overload
    def average(self: Enumerable[SupportsAverage[TResult]]) -> TResult:
        '''
        Computes the average value of the sequence. Raises `InvalidOperationError` if there
        is no value.

        The returned type is the type of the expression
        `(elem1 + elem2 + ...) / cast(int, ...)`.
        '''

    @overload
    def average(self, __selector: Callable[[TSource_co], SupportsAverage[TResult]]) -> TResult:
        '''
        Computes the average value of the sequence using the selector. Raises
        `InvalidOperationError` if there is no value.

        The returned type is the type of the expression
        `(selector(elem1) + selector(elem2) + ...) / cast(int, ...)`.
        '''

    @overload
    def average2(self: Enumerable[SupportsAverage[TResult]],
        __default: TDefault,
    ) -> Union[TResult, TDefault]:
        '''
        Computes the average value of the sequence. Returns `default` if there is no value.

        The returned type is the type of the expression
        `(elem1 + elem2 + ...) / cast(int, ...)` or `TDefault`.
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
        '''

    def cast(self, __t_result: Type[TResult]) -> Enumerable[TResult]:
        '''
        Casts the elements to the specified type.
        '''

    def concat(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        '''
        Concatenates two sequences.
        '''

    @overload
    def contains(self, value: object) -> bool:
        '''
        Tests whether the sequence contains the specified element using `==`.
        '''

    @overload
    def contains(self, value: TOther, __comparer: Callable[[TSource_co, TOther], bool]) -> bool:
        '''
        Tests whether the sequence contains the specified element using the provided comparer.
        '''

    @overload
    def count(self) -> int:
        '''
        Returns the number of elements in the sequence.
        '''

    @overload
    def count(self, __predicate: Callable[[TSource_co], bool]) -> int:
        '''
        Returns the number of elements that satisfy the condition.
        '''

    def default_if_empty(self,
        default: TDefault,
    ) -> Union[Enumerable[TSource_co], Enumerable[TDefault]]:
        '''
        Returns the elements of the sequence or the provided value in a singleton collection if
        the sequence is empty.
        '''

    def distinct(self) -> Enumerable[TSource_co]:
        '''
        Returns distinct elements from the sequence.
        '''

    @overload
    def element_at(self, index: int) -> TSource_co:
        '''
        Returns the element at specified index in the sequence. `IndexOutOfRangeError` is raised if
        no such element exists.
        '''

    @overload
    def element_at(self, index: int, __default: TDefault) -> Union[TSource_co, TDefault]:
        '''
        Returns the element at specified index in the sequence. Default value is returned if no
        such element exists.
        '''

    @staticmethod
    def empty() -> Enumerable[TSource_co]:
        '''
        Returns an empty enumerable.
        '''

    def except1(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        '''
        Produces the set difference of two sequences: self - second.
        '''

    @overload
    def first(self) -> TSource_co:
        '''
        Returns the first element of the sequence. Raises `InvalidOperationError` if there is no
        first element.
        '''

    @overload
    def first(self, __predicate: Callable[[TSource_co], bool]) -> TSource_co:
        '''
        Returns the first element of the sequence that satisfies the condition. Raises
        `InvalidOperationError` if no such element exists.
        '''

    @overload
    def first2(self, __default: TDefault) -> Union[TSource_co, TDefault]:
        '''
        Returns the first element of the sequence or a default value if there is no such
        element.
        '''

    @overload
    def first2(self,
        __predicate: Callable[[TSource_co], bool],
        __default: TDefault,
    ) -> Union[TSource_co, TDefault]:
        '''
        Returns the first element of the sequence that satisfies the condition or a default value if
        no such element exists.
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
        '''

    @overload
    def group_by(self,
        key_selector: Callable[[TSource_co], TKey],
        value_selector: Callable[[TSource_co], TValue],
    ) -> Enumerable[Grouping[TKey, TValue]]:
        '''
        Groups the elements of the sequence according to specified key selector and value selector.
        '''

    @overload
    def group_by2(self,
        key_selector: Callable[[TSource_co], TKey],
        __result_selector: Callable[[TKey, Enumerable[TSource_co]], TResult],
    ) -> Enumerable[TResult]:
        '''
        Groups the elements of the sequence according to a specified key selector function and creates a
        result value using each grouping and its key.
        '''

    @overload
    def group_by2(self,
        key_selector: Callable[[TSource_co], TKey],
    ) -> Enumerable[Grouping[TKey, TSource_co]]:
        '''
        Groups the elements of the sequence according to a specified key selector function.
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
        '''

    def intersect(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        '''
        Produces the set intersection of two sequences: self * second.
        '''

    def join(self,
        inner: Iterable[TInner],
        outer_key_selector: Callable[[TSource_co], TKey],
        inner_key_selector: Callable[[TInner], TKey],
        result_selector: Callable[[TSource_co, TInner], TResult],
    ) -> Enumerable[TResult]:
        '''
        Correlates the elements of two sequences based on matching keys.
        '''

    @overload
    def last(self) -> TSource_co:
        '''
        Returns the last element of the sequence. Raises `InvalidOperationError` if there is no first
        element.
        '''

    @overload
    def last(self, __predicate: Callable[[TSource_co], bool]) -> TSource_co:
        '''
        Returns the last element of the sequence that satisfies the condition. Raises
        `InvalidOperationError` if no such element exists.
        '''

    @overload
    def last2(self, __default: TDefault) -> Union[TSource_co, TDefault]:
        '''
        Returns the last element of the sequence or a default value if there is no such
        element.
        '''

    @overload
    def last2(self,
        __predicate: Callable[[TSource_co], bool],
        __default: TDefault,
    ) -> Union[TSource_co, TDefault]:
        '''
        Returns the last element of the sequence that satisfies the condition or a default value if
        no such element exists.
        '''

    @overload
    def max(self: Enumerable[TSupportsLessThan]) -> TSupportsLessThan:
        '''
        Returns the maximum value in the sequence. Raises `InvalidOperationError` if there is no value.
        '''

    @overload
    def max(self, __result_selector: Callable[[TSource_co], TSupportsLessThan]) -> TSupportsLessThan:
        '''
        Invokes a transform function on each element of the sequence and returns the maximum of the
        resulting values. Raises `InvalidOperationError` if there is no value.
        '''

    @overload
    def max2(self: Enumerable[TSupportsLessThan],
        __default: TDefault,
    ) -> Union[TSupportsLessThan, TDefault]:
        '''
        Returns the maximum value in the sequence, or the default one if there is no value.
        '''

    @overload
    def max2(self,
        __result_selector: Callable[[TSource_co], TSupportsLessThan],
        __default: TDefault,
    ) -> Union[TSupportsLessThan, TDefault]:
        '''
        Invokes a transform function on each element of the sequence and returns the maximum of the
        resulting values. Returns the default one if there is no value.
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

    def of_type(self, t_result: Type[TResult]) -> Enumerable[TResult]:
        '''
        Filters elements based on the specified type.

        Builtin `isinstance()` is used.
        '''

    @overload
    def order_by(self,
        key_selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> OrderedEnumerable[TSource_co, TSupportsLessThan]:
        '''
        Sorts the elements of the sequence in ascending order according to a key.
        '''

    @overload
    def order_by(self,
        key_selector: Callable[[TSource_co], TKey],
        __comparer: Callable[[TKey, TKey], int],
    ) -> OrderedEnumerable[TSource_co, TKey]:
        '''
        Sorts the elements of the sequence in ascending order by using a specified comparer.
        '''

    @overload
    def order_by_descending(self,
        key_selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> OrderedEnumerable[TSource_co, TSupportsLessThan]:
        '''
        Sorts the elements of the sequence in descending order according to a key.
        '''

    @overload
    def order_by_descending(self,
        key_selector: Callable[[TSource_co], TKey],
        __comparer: Callable[[TKey, TKey], int],
    ) -> OrderedEnumerable[TSource_co, TKey]:
        '''
        Sorts the elements of the sequence in descending order by using a specified comparer.
        '''

    def prepend(self, element: TSource_co) -> Enumerable[TSource_co]:  # type: ignore
        '''
        Adds a value to the beginning of the sequence.
        '''

    # count: Optional[int] is nonstandard behavior
    @staticmethod
    def range(start: int, count: Optional[int]) -> Enumerable[int]:
        '''
        Generates a sequence of `count` integral numbers from `start`, incrementing each by one.

        If `count` is `None`, the sequence is infinite. Raises `InvalidOperationError` if `count`
        is negative.
        '''

    # count: Optional[int] is nonstandard behavior
    @staticmethod
    def repeat(value: TResult, count: Optional[int] = None) -> Enumerable[TResult]:
        '''
        Generates a sequence that contains one repeated value.

        If `count` is `None`, the sequence is infinite. Raises `InvalidOperationError` if `count`
        is negative.
        '''

    def reverse(self) -> Enumerable[TSource_co]:
        '''
        Inverts the order of the elements in the sequence.
        '''

    def select(self, selector: Callable[[TSource_co], TResult]) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence into a new form.
        '''

    def select2(self, selector: Callable[[TSource_co, int], TResult]) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence into a new form by incorporating the indices.
        '''

    @overload
    def select_many(self,
        collection_selector: Callable[[TSource_co], Iterable[TCollection]],
        __result_selector: Callable[[TSource_co, TCollection], TResult],
    ) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence into an iterable, flattens the resulting sequence
        into one sequence, then calls result_selector on each element therein.
        '''

    @overload
    def select_many(self,
        __selector: Callable[[TSource_co], Iterable[TResult]],
    ) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence to an iterable and flattens the resultant sequences.
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
        '''

    def sequence_equal(self, second: Iterable[TSource_co]) -> bool:
        '''
        Determines whether two sequences are equal using `==` on each element.
        '''

    @overload
    def single(self) -> TSource_co:
        '''
        Returns the only element in the sequence. Raises `InvalidOperationError` if the sequence does not
        contain exactly one element.
        '''

    @overload
    def single(self, __predicate: Callable[[TSource_co], bool]) -> TSource_co:
        '''
        Returns the only element in the sequence that satisfies the condition. Raises `InvalidOperationError`
        if no element satisfies the condition, or more than one do.
        '''

    @overload
    def single2(self, __default: TDefault) -> Union[TSource_co, TDefault]:
        '''
        Returns the only element in the sequence or the default value if the sequence is empty. Raises
        `InvalidOperationError` if there are more than one elements in the sequence.
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
        '''

    def skip(self, count: int) -> Enumerable[TSource_co]:
        '''
        Bypasses a specified number of elements in the sequence and then returns the remaining.
        '''

    def skip_last(self, count: int) -> Enumerable[TSource_co]:
        '''
        Returns a new sequence that contains the elements of the current one with `count` elements omitted.
        '''

    def skip_while(self, predicate: Callable[[TSource_co], bool]) -> Enumerable[TSource_co]:
        '''
        Bypasses elements in the sequence as long as the condition is true and then returns the remaining
        elements.
        '''

    def skip_while2(self, predicate: Callable[[TSource_co, int], bool]) -> Enumerable[TSource_co]:
        '''
        Bypasses elements in the sequence as long as the condition is true and then returns the remaining
        elements. The element's index is used in the predicate function.
        '''

    # returning 0 conforms the builtin sum() function
    @overload
    def sum(self: Enumerable[TSupportsAdd]) -> Union[TSupportsAdd, int]:
        '''
        Computes the sum of the sequence, or `0` if the sequence is empty.
        '''

    # returning 0 conforms the builtin sum() function
    @overload
    def sum(self, __selector: Callable[[TSource_co], TSupportsAdd]) -> Union[TSupportsAdd, int]:
        '''
        Computes the sum of the sequence using the selector. Returns `0` if the sequence is empty.
        '''

    @overload
    def sum2(self: Enumerable[TSupportsAdd],
        __default: TDefault,
    ) -> Union[TSupportsAdd, TDefault]:
        '''
        Computes the sum of the sequence. Returns the default value if it is empty.
        '''

    @overload
    def sum2(self,
        __selector: Callable[[TSource_co], TSupportsAdd],
        __default: TDefault,
    ) -> Union[TSupportsAdd, TDefault]:
        '''
        Computes the sum of the sequence using the selector. Returns the default value if it is empty.
        '''

    def take(self, count: int) -> Enumerable[TSource_co]:
        '''
        Returns a specified number of contiguous elements from the start of the sequence.
        '''

    def take_last(self, count: int) -> Enumerable[TSource_co]:
        '''
        Returns a new sequence that contains the last `count` elements.
        '''

    def take_while(self, predicate: Callable[[TSource_co], bool]) -> Enumerable[TSource_co]:
        '''
        Returns elements from the sequence as long as the condition is true and skips the remaining.
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
        selector and value selector.
        '''

    @overload
    def to_lookup(self,
        key_selector: Callable[[TSource_co], TKey],
    ) -> Lookup[TKey, TSource_co]:
        '''
        Enumerates all values and returns a lookup containing them according to the specified
        key selector.
        '''

    def union(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        '''
        Produces the set union of two sequences: self + second.
        '''

    def where(self, predicate: Callable[[TSource_co], bool]) -> Enumerable[TSource_co]:
        '''
        Filters the sequence of values based on a predicate.
        '''

    def where2(self, predicate: Callable[[TSource_co, int], bool]) -> Enumerable[TSource_co]:
        '''
        Filters the sequence of values based on a predicate. Each element's index is used in the
        predicate logic.
        '''

    @overload
    def zip(self,
        __second: Iterable[TOther],
    ) -> Enumerable[Tuple[TSource_co, TOther]]:
        '''
        Produces a sequence of 2-element tuples from the two sequences.
        '''

    @overload
    def zip(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
    ) -> Enumerable[Tuple[TSource_co, TOther, TOther2]]: ...

    @overload
    def zip(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
        __fourth: Iterable[TOther3],
    ) -> Enumerable[Tuple[TSource_co, TOther, TOther2, TOther3]]: ...

    @overload
    def zip(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
        __fourth: Iterable[TOther3],
        __fifth: Iterable[TOther4],
    ) -> Enumerable[Tuple[TSource_co, TOther, TOther2, TOther3, TOther4]]: ...

    @overload
    def zip(self,
        __second: Iterable[Any],
        __third: Iterable[Any],
        __fourth: Iterable[Any],
        __fifth: Iterable[Any],
        __sixth: Iterable[Any],
        *iters: Iterable[Any],
    ) -> Enumerable[Tuple[Any, ...]]: ...

    @overload
    def zip2(self,
        __second: Iterable[TOther],
        __result_selector: Callable[[TSource_co, TOther], TResult],
    ) -> Enumerable[TResult]:
        '''
        Applies a specified function to the corresponding elements of two sequences, producing a
        sequence of the results.
        '''

    @overload
    def zip2(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
        __result_selector: Callable[[TSource_co, TOther, TOther2], TResult],
    ) -> Enumerable[TResult]: ...

    @overload
    def zip2(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
        __fourth: Iterable[TOther3],
        __result_selector: Callable[[TSource_co, TOther, TOther2, TOther3], TResult],
    ) -> Enumerable[TResult]: ...

    @overload
    def zip2(self,
        __second: Iterable[TOther],
        __third: Iterable[TOther2],
        __fourth: Iterable[TOther3],
        __fifth: Iterable[TOther4],
        __result_selector: Callable[[TSource_co, TOther, TOther2, TOther3, TOther4], TResult],
    ) -> Enumerable[TResult]: ...

    @overload
    def zip2(self,
        __second: Iterable[Any],
        __third: Iterable[Any],
        __fourth: Iterable[Any],
        __fifth: Iterable[Any],
        __sixth: Iterable[Any],
        *iters_and_result_selector: Union[Iterable[Any], Callable[..., Any]],
    ) -> Enumerable[Any]: ...

    # Methods below are non-standard. They do not have .NET builtin equivalence and are here just
    # for convenience.

    @overload
    def elements_in(self, __index: slice) -> Enumerable[TSource_co]:
        '''
        Produces a subsequence defined by the given slice notation.
        '''

    @overload
    def elements_in(self, __start: int, __stop: int, __step: int = 1) -> Enumerable[TSource_co]:
        '''
        Produces a subsequence with indices that define a slice.
        '''
