from typing import Any, Callable, Dict, Generic, Iterable, Iterator, List, Sequence, Set, Tuple, Type, TypeVar, Union, overload

from .lookup import Lookup
from .grouping import Grouping


TSource_co = TypeVar('TSource_co', covariant=True)
TAccumulate = TypeVar('TAccumulate')
TResult = TypeVar('TResult')
TDefault = TypeVar('TDefault')
TOther = TypeVar('TOther')
TKey = TypeVar('TKey')
TValue = TypeVar('TValue')
TCollection = TypeVar('TCollection')


class Enumerable(Sequence[TSource_co], Generic[TSource_co]):

    @overload
    def __init__(self, iterable: Iterable[TSource_co]): ...

    @overload
    def __init__(self, iterable_factory: Callable[[], Iterable[TSource_co]]): ...

    def __contains__(self, value: object) -> bool: ...

    @overload
    def __getitem__(self, index: int) -> TSource_co: ...

    @overload
    def __getitem__(self, index: slice) -> Enumerable[TSource_co]: ...

    def __iter__(self) -> Iterator[TSource_co]: ...

    def __len__(self) -> int: ...

    def __reversed__(self) -> Iterator[TSource_co]: ...

    @overload
    def aggregate(self,
        seed: TAccumulate,
        func: Callable[[TAccumulate, TSource_co], TAccumulate],
        result_selector: Callable[[TAccumulate], TResult],
    ) -> TResult:
        '''
        Applies an accumulator function over the sequence. The seed is used as the initial
        accumulator value, and the result_selector is used to select the result value.
        '''

    @overload
    def aggregate(self,
        seed: TAccumulate,
        func: Callable[[TAccumulate, TSource_co], TAccumulate],
    ) -> TAccumulate:
        '''
        Applies an accumulator function over the sequence. The seed is used as the initial
        accumulator value
        '''

    @overload
    def aggregate(self,
        func: Callable[[TAccumulate, TSource_co], TAccumulate],
    ) -> TAccumulate:
        '''
        Applies an accumulator function over the sequence. Raises `TypeError` if there is no
        value.
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
    def any(self, predicate: Callable[[TSource_co], bool]) -> bool:
        '''
        Tests whether any element of the sequence satisfy a condition.
        '''

    def append(self, element: TSource_co) -> Enumerable[TSource_co]:  # type: ignore
        '''
        Appends a value to the end of the sequence.
        '''

    @overload
    def average(self) -> Any:
        '''
        Computes the average value of the sequence. Raises `TypeError` if there is no value.

        Not type-safe. The returned type is the type of the expression
        `(elem1 + elem2 + ...) / cast(int, ...)`. Runtime errors are raised if the expression
        is unsupported.
        '''

    @overload
    def average(self, selector: Callable[[TSource_co], Any]) -> Any:
        '''
        Computes the average value of the sequence using the selector. Raises `TypeError`
        if there is no value.

        Not type-safe. The returned type is the type of the expression
        `(selector(elem1) + selector(elem2) + ...) / cast(int, ...)`. Runtime errors are raised
        if the expression is unsupported.
        '''

    @overload
    def average2(self, default: TDefault) -> Union[TDefault, Any]:
        '''
        Computes the average value of the sequence. Returns `default` if there is no value.

        Not type-safe. The returned type is the type of the expression
        `(elem1 + elem2 + ...) / cast(int, ...)` or `TDefault`. Runtime errors are raised if the
        expression is unsupported.
        '''

    @overload
    def average2(self,
        selector: Callable[[TSource_co], Any],
        default: TDefault,
    ) -> Union[Any, TDefault]:
        '''
        Computes the average value of the sequence using the selector. Returns `default`
        if there is no value.

        Not type-safe. The returned type is the type of the expression
        `(selector(elem1) + selector(elem2) + ...) / cast(int, ...)` or `TDefault`. Runtime errors
        are raised if the expression is unsupported.
        '''

    def cast(self, t_result: Type[TResult]) -> Enumerable[TResult]:
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
    def contains(self, value: TOther, comparer: Callable[[TSource_co, TOther], bool]) -> bool:
        '''
        Tests whether the sequence contains the specified element using the provided comparer.
        '''

    @overload
    def count(self) -> int:
        '''
        Returns the number of elements in the sequence.
        '''

    @overload
    def count(self, predicate: Callable[[TSource_co], bool]) -> int:
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
        Returns the element at specified index in the sequence. `IndexError` is raised if no such
        element exists.
        '''

    @overload
    def element_at(self, index: int, default: TDefault) -> Union[TSource_co, TDefault]:
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
        Returns the first element of the sequence. Raises `ValueError` if there is no first
        element.
        '''

    @overload
    def first(self, predicate: Callable[[TSource_co], bool]) -> TSource_co:
        '''
        Returns the first element of the sequence that satisfies the condition. Raises `ValueError`
        if no such element exists.
        '''

    @overload
    def first2(self, default: TDefault) -> Union[TSource_co, TDefault]:
        '''
        Returns the first element of the sequence or a default value if there is no such
        element.
        '''

    @overload
    def first2(self,
        predicate: Callable[[TSource_co], bool],
        default: TDefault,
    ) -> Union[TSource_co, TDefault]:
        '''
        Returns the first element of the sequence that satisfies the condition or a default value if
        no such element exists.
        '''

    @overload
    def group_by(self,
        key_selector: Callable[[TSource_co], TKey],
        value_selector: Callable[[TSource_co], TValue],
        result_selector: Callable[[TKey, Enumerable[TValue]], TResult],
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
        result_selector: Callable[[TKey, Enumerable[TSource_co]], TResult],
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

    # @@@ TODO

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
        result_selector: Callable[[TSource_co, TCollection], TResult],
    ) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence into an iterable, flattens the resulting sequence
        into one sequence, then calls result_selector on each element therein.
        '''

    @overload
    def select_many(self,
        selector: Callable[[TSource_co], Iterable[TResult]],
    ) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence to an iterable and flattens the resultant sequences.
        '''

    @overload
    def select_many2(self,
        collection_selector: Callable[[TSource_co, int], Iterable[TCollection]],
        result_selector: Callable[[TSource_co, TCollection], TResult],
    ) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence into an iterable, flattens the resulting sequence
        into one sequence, then calls result_selector on each element therein. The indices of
        source elements are used.
        '''

    @overload
    def select_many2(self,
        selector: Callable[[TSource_co, int], Iterable[TResult]],
    ) -> Enumerable[TResult]:
        '''
        Projects each element of the sequence to an iterable and flattens the resultant sequences.
        The indices of source elements are used.
        '''

    # @@@ TODO

    def skip(self, count: int) -> Enumerable[TSource_co]:
        '''
        Bypasses a specified number of elements in the sequence and then returns the remaining.
        '''

    # @@@ TODO

    def take(self, count: int) -> Enumerable[TSource_co]:
        '''
        Returns a specified number of contiguous elements from the start of the sequence.
        '''

    # @@@ TODO

    @overload
    def to_dict(self,
        key_selector: Callable[[TSource_co], TKey],
        value_selector: Callable[[TSource_co], TValue],
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
        value_selector: Callable[[TSource_co], TValue],
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

    # @@@ TODO

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
        second: Iterable[TOther],
        result_selector: Callable[[TSource_co, TOther], TResult],
    ) -> Enumerable[TResult]:
        '''
        Applies a specified function to the corresponding elements of two sequences, producing a
        sequence of the results.
        '''

    @overload
    def zip(self,
        second: Iterable[TOther],
    ) -> Enumerable[Tuple[TSource_co, TOther]]:
        '''
        Produces a sequence of 2-element tuples from the two sequences.
        '''
