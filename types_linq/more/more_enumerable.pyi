from typing import Any, Callable, Iterable, Optional, Tuple, overload

from ..enumerable import Enumerable
from .extrema_enumerable import ExtremaEnumerable
from ..more_typing import (
    TAccumulate,
    TKey,
    TResult,
    TSource,
    TSource_co,
    TSupportsLessThan,
)


class MoreEnumerable(Enumerable[TSource_co]):
    '''
    .. code-block:: python

        from types_linq.more import MoreEnumerable

    MoreEnumerable provides more query methods. Instances of this class can be created by directly
    constructing, using as_more(), or invoking MoreEnumerable methods that return MoreEnumerable
    instead of Enumerable.

    These APIs may have breaking changes more frequently than those in Enumerable class because updates
    in .NET are happening and sometimes ones of these APIs could be moved to Enumerable with modification,
    or changed to accommodate changes to Enumerable.

    Revisions:
        - v0.2.0: New.
    '''

    @overload
    def aggregate_right(self,
        __seed: TAccumulate,
        __func: Callable[[TSource_co, TAccumulate], TAccumulate],
        __result_selector: Callable[[TAccumulate], TResult],
    ) -> TResult:
        '''
        Applies a right-associative accumulator function over the sequence. The seed is used as
        the initial accumulator value, and the result_selector is used to select the result value.

        Revisions:
            - main: Fixed annotation for __func.
        '''

    @overload
    def aggregate_right(self,
        __seed: TAccumulate,
        __func: Callable[[TSource_co, TAccumulate], TAccumulate],
    ) -> TAccumulate:
        '''
        Applies a right-associative accumulator function over the sequence. The seed is used as the
        initial accumulator value.

        Example:
            >>> values = [9, 4, 2]
            >>> MoreEnumerable(values).aggregate_right('null', lambda e, rr: f'(cons {e} {rr})')
            '(cons 9 (cons 4 (cons 2 null)))'

        Revisions:
            - main: Fixed annotation for __func.
        '''

    @overload
    def aggregate_right(self,
        __func: Callable[[TSource_co, TSource_co], TSource_co],
    ) -> TSource_co:
        '''
        Applies a right-associative accumulator function over the sequence. Raises `InvalidOperationError`
        if there is no value in the sequence.

        Example
            >>> values = ['9', '4', '2', '5']
            >>> MoreEnumerable(values).aggregate_right(lambda e, rr: f'({e}+{rr})')
            '(9+(4+(2+5)))'

        Revisions:
            - main: Fixed annotation for __func.
        '''

    def as_more(self) -> MoreEnumerable[TSource_co]:
        '''
        Returns the original MoreEnumerable reference.
        '''

    def consume(self) -> None:
        '''
        Consumes the sequence completely. This method iterates the sequence immediately and does not save
        any intermediate data.

        Revisions:
            - v1.1.0: New.
        '''

    def cycle(self, count: Optional[int] = None) -> MoreEnumerable[TSource_co]:
        '''
        Repeats the sequence `count` times.

        If `count` is `None`, the sequence is infinite. Raises `InvalidOperationError` if `count`
        is negative.

        Example
            >>> MoreEnumerable([1, 2, 3]).cycle(3).to_list()
            [1, 2, 3, 1, 2, 3, 1, 2, 3]

        Revisions:
            - v1.1.0: New.
        '''

    def enumerate(self, start: int = 0) -> MoreEnumerable[Tuple[int, TSource_co]]:
        '''
        Returns a sequence of tuples containing the index and the value from the source sequence. `start`
        is used to specify the starting index.

        Example
            >>> ints = [2, 4, 6]
            >>> MoreEnumerable(ints).enumerate().to_list()
            [(0, 2), (1, 4), (2, 6)]

        Revisions:
            - v1.0.0: New.
        '''

    def except_by2(self,
        second: Iterable[TSource_co],
        key_selector: Callable[[TSource_co], object],
    ) -> MoreEnumerable[TSource_co]:
        '''
        Produces the set difference of two sequences: self - second, according to a key selector that
        determines "distinctness". Note the second iterable is homogenous to self.

        Example
            >>> first = [(16, 'x'), (9, 'y'), (12, 'd'), (16, 't')]
            >>> second = [(24, 'd'), (77, 'y')]
            >>> MoreEnumerable(first).except_by2(second, lambda x: x[1]).to_list()
            [(16, 'x'), (16, 't')]

        Revisions:
            - v1.0.0: Renamed from ``except_by()`` to this name to accommodate the update to Enumerable class.
            - v0.2.1: Added preliminary support for unhashable keys.
        '''

    @overload
    def flatten(self) -> MoreEnumerable[Any]:
        '''
        Flattens the sequence containing arbitrarily-nested subsequences.

        Note: the nested objects must be Iterable to be flatten.
        Instances of `str` or `bytes` are not flattened.

        Example
            >>> lst = ['apple', ['orange', ['juice', 'mango'], 'delta function']]
            >>> MoreEnumerable(lst).flatten().to_list()
            ['apple', 'orange', 'juice', 'mango', 'delta function']
        '''

    @overload
    def flatten(self, __predicate: Callable[[Iterable[Any]], bool]) -> MoreEnumerable[Any]:
        '''
        Flattens the sequence containing arbitrarily-nested subsequences. A predicate function determines
        whether a nested iterable should be flattened or not.

        Note: the nested objects must be Iterable to be flatten.
        '''

    def flatten2(self, selector: Callable[[Any], Optional[Iterable[object]]]) -> MoreEnumerable[Any]:
        '''
        Flattens the sequence containing arbitrarily-nested subsequences. A selector is used to select a
        subsequence based on the object's properties. If the selector returns None, then the object is
        considered a leaf.
        '''

    def for_each(self, action: Callable[[TSource_co], object]) -> None:
        '''
        Executes the given function on each element in the source sequence. The return values are discarded.

        Example
            .. code-block:: python

                >>> def gen():
                ...     yield 116; yield 35; yield -9

                >>> Enumerable(gen()).where(lambda x: x > 0).as_more().for_each(print)
                116
                35
        '''

    def for_each2(self, action: Callable[[TSource_co, int], object]) -> None:
        '''
        Executes the given function on each element in the source sequence. Each element's index is used in
        the logic of the function. The return values are discarded.
        '''

    def interleave(self, *iters: Iterable[TSource_co]) -> MoreEnumerable[TSource_co]:
        '''
        Interleaves the elements of two or more sequences into a single sequence, skipping sequences if they
        are consumed.

        Example
            >>> MoreEnumerable(['1', '2']).interleave(['4', '5', '6'], ['7', '8', '9']).to_list()
            ['1', '4', '7', '2', '5', '8', '6', '9']
        '''

    @overload
    def maxima_by(self,
        selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> ExtremaEnumerable[TSource_co, TSupportsLessThan]:
        '''
        Returns the maximal elements of the sequence based on the given selector.

        Example
            >>> strings = ['foo', 'bar', 'cheese', 'orange', 'baz', 'spam', 'egg', 'toasts', 'dish']
            >>> MoreEnumerable(strings).maxima_by(len).to_list()
            ['cheese', 'orange', 'toasts']
            >>> MoreEnumerable(strings).maxima_by(lambda x: x.count('e')).first()
            'cheese'
        '''

    @overload
    def maxima_by(self,
        selector: Callable[[TSource_co], TKey],
        __comparer: Callable[[TKey, TKey], int],
    ) -> ExtremaEnumerable[TSource_co, TKey]:
        '''
        Returns the maximal elements of the sequence based on the given selector and the comparer.

        Such comparer takes two values and return positive ints when lhs > rhs, negative ints
        if lhs < rhs, and 0 if they are equal.
        '''

    @overload
    def minima_by(self,
        selector: Callable[[TSource_co], TSupportsLessThan],
    ) -> ExtremaEnumerable[TSource_co, TSupportsLessThan]:
        '''
        Returns the minimal elements of the sequence based on the given selector.
        '''

    @overload
    def minima_by(self,
        selector: Callable[[TSource_co], TKey],
        __comparer: Callable[[TKey, TKey], int],
    ) -> ExtremaEnumerable[TSource_co, TKey]:
        '''
        Returns the minimal elements of the sequence based on the given selector and the comparer.

        Such comparer takes two values and return positive ints when lhs > rhs, negative ints
        if lhs < rhs, and 0 if they are equal.
        '''

    def pipe(self, action: Callable[[TSource_co], object]) -> MoreEnumerable[TSource_co]:
        '''
        Executes the given action on each element in the sequence and yields it. Return values of
        action are discarded.

        Example
            >>> store = set()
            >>> MoreEnumerable([1, 2, 2, 1]).pipe(store.add).where(lambda x: x % 2 == 0).to_list()
            [2, 2]
            >>> store
            {1, 2}

        Revisions:
            - v0.2.1: New.
        '''

    # note: diffrent from morelinq: identity is first parameter
    def pre_scan(self,
        identity: TAccumulate,
        transformation: Callable[[TAccumulate, TSource_co], TAccumulate],
    ) -> MoreEnumerable[TAccumulate]:
        '''
        Performs a pre-scan (exclusive prefix sum) over the sequence. Such scan returns an
        equal-length sequence where the first element is the identity, and i-th element (i>1) is
        the sum of the first i-1 (and identity) elements in the original sequence.

        Example
            >>> values = [9, 4, 2, 5, 7]
            >>> MoreEnumerable(values).pre_scan(0, lambda acc, e: acc + e).to_list()
            [0, 9, 13, 15, 20]
            >>> MoreEnumerable([]).pre_scan(0, lambda acc, e: acc + e).to_list()
            []

        Revisions:
            - main: New.
        '''

    @overload
    def rank(self: MoreEnumerable[TSupportsLessThan]) -> MoreEnumerable[int]:
        '''
        Ranks each item in the sequence in descending order.

        Example
            >>> scores = [1, 4, 77, 23, 23, 4, 9, 0, -7, 101, 23]
            >>> MoreEnumerable(scores).rank().to_list()
            [6, 5, 2, 3, 3, 5, 4, 7, 8, 1, 3]  # 101 is largest, so has rank of 1

        Revisions:
            - v1.0.0: New.
        '''

    @overload
    def rank(self, __comparer: Callable[[TSource_co, TSource_co], int]) -> MoreEnumerable[int]:
        '''
        Ranks each item in the sequence in descending order using the given comparer.

        Such comparer takes two values and return positive ints when lhs > rhs, negative ints
        if lhs < rhs, and 0 if they are equal.

        Revisions:
            - v1.0.0: New.
        '''

    @overload
    def rank_by(self, key_selector: Callable[[TSource_co], TSupportsLessThan]) -> MoreEnumerable[int]:
        '''
        Ranks each item in the sequence in descending order using the given selector.

        Example
            .. code-block:: python

                >>> scores = [
                ...     {'name': 'Frank', 'score': 75},
                ...     {'name': 'Alica', 'score': 90},
                ...     {'name': 'Erika', 'score': 99},
                ...     {'name': 'Rogers', 'score': 90},
                ... ]

                >>> MoreEnumerable(scores).rank_by(lambda x: x['score']) \\
                ...     .zip(scores) \\
                ...     .group_by(lambda t: t[0], lambda t: t[1]['name']) \\
                ...     .to_dict(lambda g: g.key, lambda g: g.to_list())
                {3: ['Frank'], 2: ['Alica', 'Rogers'], 1: ['Erika']}

        Revisions:
            - v1.0.0: New.
        '''

    @overload
    def rank_by(self,
        key_selector: Callable[[TSource_co], TKey],
        __comparer: Callable[[TKey, TKey], int],
    ) -> MoreEnumerable[int]:
        '''
        Ranks each item in the sequence in descending order using the given selector and comparer.

        Such comparer takes two values and return positive ints when lhs > rhs, negative ints
        if lhs < rhs, and 0 if they are equal.

        Revisions:
            - v1.0.0: New.
        '''

    @overload
    def run_length_encode(self) -> MoreEnumerable[Tuple[TSource_co, int]]:
        '''
        Run-length encodes the sequence into a sequence of tuples where each tuple contains an
        (the first) element and its number of contingent occurrences, where equality is based on
        `==`.

        Example
            >>> MoreEnumerable('abbcaeeeaa').run_length_encode().to_list()
            [('a', 1), ('b', 2), ('c', 1), ('a', 1), ('e', 3), ('a', 2)]

        Revisions:
            - v1.1.0: New.
        '''

    @overload
    def run_length_encode(self,
        __comparer: Callable[[TSource_co, TSource_co], bool],
    ) -> MoreEnumerable[Tuple[TSource_co, int]]:
        '''
        Run-length encodes the sequence into a sequence of tuples where each tuple contains an
        (the first) element and its number of contingent occurrences, where equality is determined by
        the comparer.

        Example
            >>> MoreEnumerable('abBBbcaEeeff') \\
            >>>     .run_length_encode(lambda x, y: x.lower() == y.lower()).to_list()
            [('a', 1), ('b', 4), ('c', 1), ('a', 1), ('E', 3), ('f', 2)]

        Revisions:
            - v1.1.0: New.
        '''

    @overload
    def scan(self,
        __transformation: Callable[[TSource_co, TSource_co], TSource_co],
    ) -> MoreEnumerable[TSource_co]:
        '''
        Performs a inclusive prefix sum over the sequence. Such scan returns an equal-length sequence
        where the i-th element is the sum of the first i elements in the original sequence.

        Example
            >>> values = [9, 4, 2, 5, 7]
            >>> MoreEnumerable(values).scan(lambda acc, e: acc + e).to_list()
            [9, 13, 15, 20, 27]
            >>> MoreEnumerable([]).scan(lambda acc, e: acc + e).to_list()
            []

        Example
            >>> # running max
            >>> fruits = ['apple', 'mango', 'orange', 'passionfruit', 'grape']
            >>> MoreEnumerable(fruits).scan(lambda acc, e: e if len(e) > len(acc) else acc).to_list()
            ['apple', 'apple', 'orange', 'passionfruit', 'passionfruit']

        Revisions:
            - main: New.
        '''

    @overload
    def scan(self,
        __seed: TAccumulate,
        __transformation: Callable[[TAccumulate, TSource_co], TAccumulate],
    ) -> MoreEnumerable[TAccumulate]:
        '''
        Like Enumerable.aggregate(seed, transformation) except that the intermediate results are
        included in the result sequence.

        Example
            >>> Enumerable.range(1, 5).as_more().scan(-1, lambda acc, e: acc * e).to_list()
            [-1, -1, -2, -6, -24, -120]

        Revisions:
            - main: New.
        '''

    @overload
    def scan_right(self,
        __func: Callable[[TSource_co, TSource_co], TSource_co],
    ) -> MoreEnumerable[TSource_co]:
        '''
        Performs a right-associative inclusive prefix sum over the sequence. This is the
        right-associative version of MoreEnumerable.scan(func).

        Example
            >>> values = ['9', '4', '2', '5']
            >>> MoreEnumerable(values).scan_right(lambda e, rr: f'({e}+{rr})').to_list()
            ['(9+(4+(2+5)))', '(4+(2+5))', '(2+5)', '5']
            >>> MoreEnumerable([]).scan_right(lambda e, rr: e + rr).to_list()
            []

        Revisions:
            - main: New.
        '''

    @overload
    def scan_right(self,
        __seed: TAccumulate,
        __func: Callable[[TSource_co, TAccumulate], TAccumulate],
    ) -> MoreEnumerable[TAccumulate]:
        '''
        The right-associative version of MoreEnumerable.scan(seed, func).

        Example
            >>> values = [9, 4, 2]
            >>> MoreEnumerable(values).scan_right('null', lambda e, rr: f'(cons {e} {rr})').to_list()
            ['(cons 9 (cons 4 (cons 2 null)))', '(cons 4 (cons 2 null))', '(cons 2 null)', 'null']

        Revisions:
            - main: New.
        '''

    def segment(self,
        new_segment_predicate: Callable[[TSource_co], bool],
    ) -> MoreEnumerable[MoreEnumerable[TSource_co]]:
        '''
        Splits the sequence into segments by using a detector function that returns True to signal a
        new segment.

        Example
            >>> values = [0, 1, 2, 4, -4, -2, 6, 2, -2]
            >>> MoreEnumerable(values).segment(lambda x: x < 0).select(lambda x: x.to_list()).to_list()
            [[0, 1, 2, 4], [-4], [-2, 6, 2], [-2]]

        Revisions:
            - main: New.
        '''

    def segment2(self,
        new_segment_predicate: Callable[[TSource_co, int], bool],
    ) -> MoreEnumerable[MoreEnumerable[TSource_co]]:
        '''
        Splits the sequence into segments by using a detector function that returns True to signal a
        new segment. The element's index is used in the detector function.

        Example
            >>> values = [0, 1, 2, 4, -4, -2, 6, 2, -2]
            >>> MoreEnumerable(values).segment2(lambda x, i: x < 0 or i % 3 == 0) \\
            ...     .select(lambda x: x.to_list()) \\
            ...     .to_list()
            [[0, 1, 2], [4], [-4], [-2], [6, 2], [-2]]

        Revisions:
            - main: New.
        '''

    def segment3(self,
        new_segment_predicate: Callable[[TSource_co, TSource_co, int], bool],
    ) -> MoreEnumerable[MoreEnumerable[TSource_co]]:
        '''
        Splits the sequence into segments by using a detector function that returns True to signal a
        new segment. The last element and the current element's index are used in the detector
        function.

        Example
            >>> values = [0, 1, 2, 4, -4, -2, 6, 2, -2]
            >>> MoreEnumerable(values).segment3(lambda curr, prev, i: curr * prev < 0) \\
            ...     .select(lambda x: x.to_list()) \\
            ...     .to_list()
            [[0, 1, 2, 4], [-4, -2], [6, 2], [-2]]

        Revisions:
            - main: New.
        '''

    @staticmethod
    def traverse_breath_first(
        root: TSource,
        children_selector: Callable[[TSource], Iterable[TSource]],
    ) -> MoreEnumerable[TSource]:
        '''
        Traverses the tree (graph) from the root node in a breath-first fashion. A selector is used to
        select children of each node.

        Graphs are not checked for cycles. If the resulting sequence needs to be finite then it is the
        responsibility of children_selector to ensure that duplicate nodes are not visited.
        '''

    @staticmethod
    def traverse_depth_first(
        root: TSource,
        children_selector: Callable[[TSource], Iterable[TSource]],
    ) -> MoreEnumerable[TSource]:
        '''
        Traverses the tree (graph) from the root node in a depth-first fashion. A selector is used to
        select children of each node.

        Graphs are not checked for cycles. If the resulting sequence needs to be finite then it is the
        responsibility of children_selector to ensure that duplicate nodes are not visited.
        '''
