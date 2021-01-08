from typing import Any, Callable, Generic, Iterable, Iterator, List, Type, TypeVar, Union, overload


TSource_co = TypeVar('TSource_co', covariant=True)
TAccumulate = TypeVar('TAccumulate')
TResult = TypeVar('TResult')
TDefault = TypeVar('TDefault')


class Enumerable(Generic[TSource_co]):

    @overload
    def __init__(self, iterable: Iterable[TSource_co]): ...

    @overload
    def __init__(self, iterable_factory: Callable[[], Iterable[TSource_co]]): ...

    def __iter__(self) -> Iterator[TSource_co]: ...

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

    def to_list(self) -> List[TSource_co]:
        '''
        Enumerates all values and returns a list containing them.
        '''
