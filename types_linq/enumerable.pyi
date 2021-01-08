from typing import Callable, Generic, Iterable, Iterator, List, TypeVar, overload


TSource_co = TypeVar('TSource_co', covariant=True)
TAccumulate = TypeVar('TAccumulate')
TResult = TypeVar('TResult')


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
        Applies an accumulator function over the sequence.
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

    def to_list(self) -> List[TSource_co]:
        '''
        Enumerates all values and returns a list containing them.
        '''
