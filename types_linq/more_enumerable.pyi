from typing import Any, Callable, Iterable, overload

from .enumerable import Enumerable
from .extrema_enumerable import ExtremaEnumerable
from .more_typing import (
    TAccumulate,
    TResult,
    TSource_co,
    TSupportsLessThan,
)


class MoreEnumerable(Enumerable[TSource_co]):
    '''
    MoreEnumerable provides more query methods. Instances of this class can be created by directly
    constructing, using as_more(), or invoking MoreEnumerable methods that return MoreEnumerable
    instead of Enumerable.
    '''

    @overload
    def aggregate_right(self,
        __seed: TAccumulate,
        __func: Callable[[TAccumulate, TSource_co], TAccumulate],
        __result_selector: Callable[[TAccumulate], TResult],
    ) -> TResult:
        '''
        Applies a right-associative accumulator function over the sequence. The seed is used as
        the initial accumulator value, and the result_selector is used to select the result value.
        '''

    @overload
    def aggregate_right(self,
        __seed: TAccumulate,
        __func: Callable[[TAccumulate, TSource_co], TAccumulate],
    ) -> TAccumulate:
        '''
        Applies a right-associative accumulator function over the sequence. The seed is used as the
        initial accumulator value.
        '''

    @overload
    def aggregate_right(self,
        __func: Callable[[TAccumulate, TSource_co], TAccumulate],
    ) -> TAccumulate:
        '''
        Applies a right-associative accumulator function over the sequence. Raises `InvalidOperationError`
        if there is no value in the sequence.
        '''

    def as_more(self) -> MoreEnumerable[TSource_co]:
        '''
        Returns the original MoreEnumerable reference.
        '''

    def for_each(self, action: Callable[[TSource_co], Any]) -> None:
        '''
        Executes the given function on each element in the source sequence. The return values are discarded.
        '''

    def for_each2(self, action: Callable[[TSource_co, int], Any]) -> None:
        '''
        Executes the given function on each element in the source sequence. Each element's index is used in
        the logic of the function. The return values are discarded.
        '''

    def interleave(self, *iters: Iterable[TSource_co]) -> MoreEnumerable[TSource_co]:
        '''
        Interleaves the elements of two or more sequences into a single sequence, skipping sequences if they
        are consumed.
        '''

    def max_by(self,
        selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> ExtremaEnumerable[TSource_co, TSupportsLessThan]:
        '''
        Returns the maximal elements of the sequence based on the given selector.
        '''

    def min_by(self,
        selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> ExtremaEnumerable[TSource_co, TSupportsLessThan]:
        '''
        Returns the minimal elements of the sequence based on the given selector.
        '''
