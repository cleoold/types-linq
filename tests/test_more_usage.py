from dataclasses import dataclass
from typing import Any, Callable, List, Optional, cast

import pytest

from types_linq import Enumerable, InvalidOperationError
from types_linq.more import MoreEnumerable, DirectedGraphNotAcyclicError


class Node:
    def __init__(self, val: int) -> None:
        self.val = val


@dataclass
class Tree:
    val: int
    left: 'Optional[Tree]' = None
    right: 'Optional[Tree]' = None


class TestAsMore:
    def test_ret_type(self):
        en = Enumerable([1, 2]).as_more()
        assert isinstance(en, MoreEnumerable)
        assert en.to_list() == [1, 2]

    def test_ret_self(self):
        en = MoreEnumerable([1, 2])
        assert en is en.as_more()


class TestAggregateRightMethod:
    def test_overload1(self):
        fruits = ['apple', 'mango', 'orange', 'passionfruit', 'grape']
        en = MoreEnumerable(fruits)
        st = en.aggregate_right('banana', lambda e, rr: f'({e}/{rr})', str.upper)
        assert st == '(APPLE/(MANGO/(ORANGE/(PASSIONFRUIT/(GRAPE/BANANA)))))'

    def test_overload1_empty(self):
        fruits: List[str] = []
        en = MoreEnumerable(fruits)
        st = en.aggregate_right('banana', lambda e, rr: f'({e}/{rr})', str.upper)
        assert st == 'BANANA'

    def test_overload2(self):
        en = MoreEnumerable([9, 4, 2])
        expr = en.aggregate_right('null', lambda e, rr: f'(cons {e} {rr})')
        assert expr == '(cons 9 (cons 4 (cons 2 null)))'

    def test_overload3(self):
        en = MoreEnumerable(['9', '4', '2', '5'])
        expr = en.aggregate_right(lambda e, rr: f'({e}+{rr})')
        assert expr == '(9+(4+(2+5)))'

    def test_overload3_empty(self):
        ints: List[int] = []
        en = MoreEnumerable(ints)
        with pytest.raises(InvalidOperationError, match='Sequence is empty'):
            en.aggregate_right(lambda e, rr: e - rr)

    def test_overload3_1(self):
        ints = [87]
        en = MoreEnumerable(ints)
        sole = en.aggregate_right(lambda e, rr: e - rr)
        assert sole == 87


class TestConsumeMethod:
    def test_consume(self):
        counter = 0
        def gen():
            nonlocal counter
            for _ in range(5):
                counter += 1
                yield None
        en = MoreEnumerable(gen())
        en.consume()
        assert counter == 5


class TestEnumerateMethod:
    def test_enumerate(self):
        en = MoreEnumerable(['2', '4', '6'])
        assert en.enumerate().to_list() == [(0, '2'), (1, '4'), (2, '6')]

    def test_enumerate_start(self):
        en = MoreEnumerable(['2', '4', '6'])
        assert en.enumerate(1).to_list() == [(1, '2'), (2, '4'), (3, '6')]


class TestExceptBy2Method:
    def test_except_by2(self):
        en = MoreEnumerable(['aaa', 'bb', 'c', 'dddd'])
        assert en.except_by2(['xx', 'y'], len).to_list() == ['aaa', 'dddd']

    def test_unhashable(self):
        en = MoreEnumerable([['aaa'], ['bb'], ['c'], ['dddd']])
        q = en.except_by2([['xx'], ['y']], lambda x: len(x[0]))
        assert q.to_list() == [['aaa'], ['dddd']]

    def test_no_repeat(self):
        en = MoreEnumerable(['aaa', 'bb', 'c', 'dddd', 'aaa'])
        assert en.except_by2(['xx', 'y'], len).to_list() == ['aaa', 'dddd']

    def test_remove_nothing(self):
        i = -1
        def selector(_):
            nonlocal i; i += 1
            return i
        strs = ['aaa', 'bb', 'c', 'dddd', 'dddd']
        en = MoreEnumerable(strs)
        assert en.except_by2((), selector).to_list() == strs


class TestFlattenMethod:
    def test_flatten_overload1(self):
        en = MoreEnumerable(
        [
            1, 2, 3,
            [
                4, 5, 'orange', b'sequence',
                [
                    6, [7],
                ],
                8,
            ],
            'foo',
            [],
            MoreEnumerable(
            [
                9, 10, (11, 12),
            ]),
        ])
        assert en.flatten().to_list() == [
            1, 2, 3, 4, 5, 'orange', b'sequence', 6, 7, 8, 'foo', 9, 10, 11, 12,
        ]

    def test_flatten_overload2(self):
        en = MoreEnumerable([
            1, 2, 3, [4, 5], [6, 7, 8], [9, 10, [11, 12], 13],
        ])
        assert en.flatten(lambda x: len(cast(List[Any], x)) != 2).to_list() == [
            1, 2, 3, [4, 5], 6, 7, 8, 9, 10, [11, 12], 13,
        ]

    def test_flatten_overload2_false(self):
        lst = [1, 2, 3, [4, 5, [6]]]
        en = MoreEnumerable(lst)
        assert en.flatten(lambda x: False).to_list() == lst

    def test_flatten2_tree(self):
        t = Tree \
        (
            left=Tree
            (
                left=Tree(0),
                val=1,
                right=Tree(2),
            ),
            val=3,
            right=Tree
            (
                left=Tree(4),
                val=5,
                right=Tree(6),
            )
        )
        en = MoreEnumerable((t, 'ignore_me'))

        def pred(x):
            if isinstance(x, int):
                return None
            elif isinstance(x, Tree):
                return (x.left, x.val, x.right)
            elif isinstance(x, str):
                return ()
            elif isinstance(x, tuple):
                return x
            elif x is None:
                return ()
            raise Exception

        assert en.flatten2(pred).to_list() == [*range(7)]

    def test_flatten2_empty(self):
        en = MoreEnumerable(())
        assert en.flatten2(lambda x: x).to_list() == []


class TestForEachMethod:
    def test_for_each(self):
        side_effects = []
        en = MoreEnumerable([7, 9, 11])
        en.for_each(lambda x: side_effects.append(str(x)))
        assert side_effects == ['7', '9', '11']

    def test_for_each2(self):
        side_effects = []
        en = MoreEnumerable([7, 9, 11])
        en.for_each2(lambda x, i: side_effects.append(f'{x}/{i}'))
        assert side_effects == ['7/0', '9/1', '11/2']


class TestInterleaveMethod:
    def test_interleave_one(self):
        en = MoreEnumerable([1, 2, 4]).interleave(*[])
        assert en.to_list() == [1, 2, 4]

    def test_interleave_two(self):
        en = MoreEnumerable([1, 2, 3]).interleave([4, 5, 6])
        assert en.to_list() == [1, 4, 2, 5, 3, 6]

    def test_interleave_three(self):
        en = MoreEnumerable([1, 2]).interleave([4, 5], [11, 12])
        assert en.to_list() == [1, 4, 11, 2, 5, 12]

    def test_skip_consumed_me(self):
        en = MoreEnumerable(['1', '2']).interleave(['4', '5', '6'], ['7', '8', '9'])
        assert en.to_list() == ['1', '4', '7', '2', '5', '8', '6', '9']

    def test_skip_consumed_them(self):
        en = MoreEnumerable([4, 5, 6]).interleave([9], [12, 17], [44, 45, 46])
        assert en.to_list() == [4, 9, 12, 44, 5, 17, 45, 6, 46]


class TestMaximaByMethod:
    strings = ['foo', 'bar', 'cheese', 'orange', 'baz', 'spam', 'egg', 'toasts', 'dish']

    def test_overload1(self):
        en = MoreEnumerable(self.strings).maxima_by(len)
        assert en.to_list() == ['cheese', 'orange', 'toasts']

    def test_overload1_empty(self):
        en = MoreEnumerable([]).maxima_by(len)
        assert en.to_list() == []

    def test_overload2(self):
        s = [[[x]] for x in self.strings]
        en = MoreEnumerable(s).maxima_by(lambda x: x[0], lambda x, y: len(x[0]) - len(y[0]))
        assert en.to_list() == [[['cheese']], [['orange']], [['toasts']]]


class TestMinimaByMethod:
    def test_overload1(self):
        en = MoreEnumerable(TestMaximaByMethod.strings).minima_by(len)
        assert en.to_list() == ['foo', 'bar', 'baz', 'egg']

    def test_overload1_empty(self):
        en = MoreEnumerable([]).minima_by(len)
        assert en.to_list() == []

    def test_overload2(self):
        s = [[[x]] for x in TestMaximaByMethod.strings]
        en = MoreEnumerable(s).minima_by(lambda x: x[0], lambda x, y: len(x[0]) - len(y[0]))
        assert en.to_list() == [[['foo']], [['bar']], [['baz']], [['egg']]]


# no extensive testing because similar things are already tested in Enumerable
class TestExtremaEnumerableFirstMethod:
    def test_first_overload1(self):
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len)
        assert en.first() == 'cheese'

    def test_first_overload1_empty(self):
        en = MoreEnumerable([]).maxima_by(len)
        with pytest.raises(InvalidOperationError):
            en.first()

    def test_first_call_parent_overload2(self):
        'properly delegates the with-predicate overload to base class implementation'
        # don't crash
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len)
        assert en.first(lambda x: 'o' in x) == 'orange'

    def test_first2_overload1(self):
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len)
        assert en.first2('mmmmmm') == 'cheese'

    def test_first2_overload1_empty(self):
        en = MoreEnumerable([]).maxima_by(len)
        assert en.first2('mmmmmm') == 'mmmmmm'

    def test_first2_call_parent_overload2(self):
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len)
        assert en.first2(lambda x: False, 'mmmmmm') == 'mmmmmm'


class TestExtremaEnumerableLastMethod:
    def test_last_overload1(self):
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len)
        assert en.last() == 'toasts'

    def test_last_overload1_empty(self):
        en = MoreEnumerable([]).maxima_by(len)
        with pytest.raises(InvalidOperationError):
            en.last()

    def test_last_call_parent_overload2(self):
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len)
        assert en.last(lambda x: 'g' in x) == 'orange'

    def test_last2_overload1(self):
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len)
        assert en.last2('mmmmmm') == 'toasts'

    def test_last2_overload1_empty(self):
        en = MoreEnumerable([]).maxima_by(len)
        assert en.last2('mmmmmm') == 'mmmmmm'

    def test_last2_call_parent_overload2(self):
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len)
        assert en.last2(lambda x: False, 'mmmmmm') == 'mmmmmm'


class TestExtremaEnumerableSingleMethod:
    strings = ['foo', 'bar', 'cheese']

    def test_single_overload1(self):
        en = MoreEnumerable(self.strings).maxima_by(len)
        assert en.single() == 'cheese'

    def test_single_overload1_more(self):
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len)
        with pytest.raises(InvalidOperationError):
            en.single()

    def test_single_call_parent_overload2(self):
        en = MoreEnumerable(self.strings).maxima_by(len)
        with pytest.raises(InvalidOperationError):
            en.single(lambda x: False)

    def test_single2_overload1(self):
        en = MoreEnumerable(self.strings).maxima_by(len)
        assert en.single2('mmmmmm') == 'cheese'

    def test_single2_overload1_empty(self):
        en = MoreEnumerable([]).maxima_by(len)
        assert en.single2('mmmmmm') == 'mmmmmm'

    def test_single2_call_parent_overload2(self):
        en = MoreEnumerable(self.strings).maxima_by(len)
        assert en.single2(lambda x: False, 'mmmmmm') == 'mmmmmm'


class TestExtremaEnumerableTakeMethod:
    @pytest.mark.parametrize('count,expected', [
        (-1, []),
        (0, []),
        (1, ['cheese']),
        (2, ['cheese', 'orange']),
        (3, ['cheese', 'orange', 'toasts']),
        (4, ['cheese', 'orange', 'toasts']),
    ])
    def test_take_overload1(self, count: int, expected: List[str]):
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len).take(count)
        assert en.to_list() == expected

    def test_take_call_parent_overload2(self):
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len)
        assert en.take(slice(1, None)).to_list() == ['orange', 'toasts']


class TestExtremaEnumerableTakeLastMethod:
    @pytest.mark.parametrize('count,expected', [
        (-1, []),
        (0, []),
        (1, ['toasts']),
        (2, ['orange', 'toasts']),
        (3, ['cheese', 'orange', 'toasts']),
        (4, ['cheese', 'orange', 'toasts']),
    ])
    def test_take_last(self, count: int, expected: List[str]):
        en = MoreEnumerable(TestMaximaByMethod.strings).maxima_by(len).take_last(count)
        assert en.to_list() == expected


class TestPipeMethod:
    def test_pipe(self):
        store = []
        ints = [1, 2]
        en = MoreEnumerable(ints)
        assert en.pipe(store.append).to_list() == ints
        assert store == ints

    def test_action_then_yield(self):
        en = MoreEnumerable([[], []])
        q = en.pipe(lambda x: x.append(1)).where(lambda x: len(x) == 0)
        assert q.to_list() == []


class TestPreScanMethod:
    def test_pre_scan(self):
        ints = [9, 4, 2, 5, 7]
        en = MoreEnumerable(ints)
        sums = en.pre_scan(0, lambda acc, e: acc + e)
        assert sums.to_list() == [0, 9, 13, 15, 20]
        exprs = en.pre_scan('', lambda acc, e: f'{acc}+{e}')
        assert exprs.to_list() == ['', '+9', '+9+4', '+9+4+2', '+9+4+2+5']

    def test_one_elem(self):
        ints = [9]
        en = MoreEnumerable(ints)
        q = en.pre_scan(10, lambda acc, e: acc + e)
        assert q.to_list() == [10]

    def test_empty(self):
        q = MoreEnumerable([]).pre_scan(0, lambda acc, e: acc + e)
        assert q.to_list() == []


class TestRankMethod:
    def test_overload1(self):
        def gen():
            yield from [1, 4, 77, 23, 23, 4, 9, 0, -7, 101, 23]
        en = MoreEnumerable(gen())
        assert en.rank().to_list() == [6, 5, 2, 3, 3, 5, 4, 7, 8, 1, 3]

    def test_overload1_empty(self):
        assert MoreEnumerable([]).rank().to_list() == []

    def test_overload1_sorted(self):
        ints = [444, 190, 129, 122, 100]
        assert MoreEnumerable(ints).rank().to_list() == [1, 2, 3, 4, 5]
        assert MoreEnumerable(reversed(ints)).rank().to_list() == [5, 4, 3, 2, 1]

    def test_overload1_same(self):
        en = MoreEnumerable([8, 8, 8])
        assert en.rank().to_list() == [1, 1, 1]

    def test_overload2(self):
        en = MoreEnumerable([(1, ''), (1, ''), (4, ''), (4, ''), (3, '')])
        assert en.rank(lambda lhs, rhs: lhs[0] - rhs[0]).to_list() == [3, 3, 1, 1, 2]

    def test_overload2_default_obj_eq_dont_use(self):
        en = MoreEnumerable([Node(1), Node(1), Node(4), Node(4), Node(3), Node(4)])
        assert en.rank(lambda lhs, rhs: lhs.val - rhs.val).to_list() \
            == [3, 3, 1, 1, 2, 1]


# majority is already tested by rank test
class TestRankByMethod:
    def test_overload1(self):
        def gen():
            yield from ['aaa', 'xyz', 'carbon', 'emission', 'statistics', 'somany']
        en = MoreEnumerable(gen())
        assert en.rank_by(len).to_list() == [4, 4, 3, 2, 1, 3]

    def test_overload2(self):
        en = MoreEnumerable([
            ['aaa'], ['xyz'], ['carbon'], ['emission'], ['statistics'], ['somany']
        ])
        assert en.rank_by(lambda x: x[0], lambda lhs, rhs: len(lhs) - len(rhs)) \
            .to_list() == [4, 4, 3, 2, 1, 3]

    def test_overload2_empty(self):
        en = MoreEnumerable([])
        assert en.rank_by(lambda x: x[0], lambda lhs, rhs: len(lhs) - len(rhs)) \
            .to_list() == []


class TestRunLengthEncodeMethod:
    def test_overload1(self):
        en = MoreEnumerable('abbcaeeeaa')
        assert en.run_length_encode().to_list() \
            == [('a', 1), ('b', 2), ('c', 1), ('a', 1), ('e', 3), ('a', 2)]

    def test_overload1_empty(self):
        en = MoreEnumerable(())
        assert en.run_length_encode().to_list() == []

    def test_overload1_one_run(self):
        en = MoreEnumerable('AAAAA')
        assert en.run_length_encode().to_list() == [('A', 5)]

    def test_overload1_one_elem(self):
        en = MoreEnumerable('A')
        assert en.run_length_encode().to_list() == [('A', 1)]

    def test_overload1_no_run(self):
        en = MoreEnumerable('abcdefghijklmnopqrstuvwxyz')
        assert en.run_length_encode().to_list() == \
            en.select(lambda x: (x, 1)).to_list()

    def test_overload2(self):
        en = MoreEnumerable('abBBbcaEeeff')
        assert en.run_length_encode(lambda x, y: x.lower() == y.lower()).to_list() \
            == [('a', 1), ('b', 4), ('c', 1), ('a', 1), ('E', 3), ('f', 2)]


class TestScanMethod:
    def test_overload1(self):
        ints = [9, 4, 2, 5, 7]
        en = MoreEnumerable(ints)
        sums = en.scan(lambda acc, e: acc + e)
        assert sums.to_list() == [9, 13, 15, 20, 27]

    def test_overload1_one_elem(self):
        ints = [9]
        en = MoreEnumerable(ints)
        q = en.scan(lambda acc, e: acc + e)
        assert q.to_list() == [9]

    def test_overload1_empty(self):
        q = MoreEnumerable([]).scan(lambda acc, e: acc + e)
        assert q.to_list() == []

    def test_overload2(self):
        ints = [9, 4, 2, 5, 7]
        en = MoreEnumerable(ints)
        sums = en.scan('', lambda acc, e: f'{acc}+{e}')
        assert sums.to_list() == ['', '+9', '+9+4', '+9+4+2', '+9+4+2+5', '+9+4+2+5+7']

    def test_overload2_one_elem(self):
        ints = [9]
        en = MoreEnumerable(ints)
        q = en.scan(10, lambda acc, e: acc + e)
        assert q.to_list() == [10, 19]

    def test_overload2_empty(self):
        q = MoreEnumerable([]).scan(-1, lambda acc, e: acc + e)
        assert q.to_list() == [-1]


class TestScanRightMethod:
    def test_overload1(self):
        strs = ['9', '4', '2', '5']
        en = MoreEnumerable(strs)
        q = en.scan_right(lambda e, rr: f'({e}+{rr})')
        assert q.to_list() == ['(9+(4+(2+5)))', '(4+(2+5))', '(2+5)', '5']

    def test_overload1_one_elem(self):
        strs = ['-1']
        en = MoreEnumerable(strs)
        q = en.scan_right(lambda e, rr: f'({e}+{rr})')
        assert q.to_list() == ['-1']

    def test_overload1_empty(self):
        q = MoreEnumerable([]).scan_right(lambda e, rr: f'({e}+{rr})')
        assert q.to_list() == []

    def test_overload2(self):
        ints = [9, 4, 2]
        en = MoreEnumerable(ints)
        q = en.scan_right('null', lambda e, rr: f'(cons {e} {rr})')
        assert q.to_list() == [
            '(cons 9 (cons 4 (cons 2 null)))',
            '(cons 4 (cons 2 null))',
            '(cons 2 null)',
            'null',
        ]

    def test_overload2_one_elem(self):
        ints = [9]
        en = MoreEnumerable(ints)
        q = en.scan_right('nil', lambda e, rr: f'(cons {e} {rr})')
        assert q.to_list() == ['(cons 9 nil)', 'nil']

    def test_overload2_empty(self):
        en = MoreEnumerable([])
        q = en.scan_right('nil', lambda e, rr: f'(cons {e} {rr})')
        assert q.to_list() == ['nil']


class TestSegmentMethod:
    def test_segment(self):
        ints = [0, 1, 2, 4, -4, -2, 6, 2, -2]
        en = MoreEnumerable(ints)
        q = en.segment(lambda x: x < 0).select(lambda x: x.to_list())
        assert q.to_list() == [[0, 1, 2, 4], [-4], [-2, 6, 2], [-2]]

    def test_segment_empty(self):
        en = MoreEnumerable([])
        q = en.segment(lambda x: x < 0).select(lambda x: x.to_list())
        assert q.to_list() == []

    def test_segment_always_split(self):
        ints = [1, 2, 3]
        en = MoreEnumerable(ints)
        q = en.segment(lambda x: True).select(lambda x: x.to_list())
        assert q.to_list() == [[1], [2], [3]]

    def test_segment_no_splitting(self):
        ints = [1, 2, 3]
        en = MoreEnumerable(ints)
        q = en.segment(lambda x: False).select(lambda x: x.to_list())
        assert q.to_list() == [ints]

    def test_segment_one_elem(self):
        def pred(_: str): raise Exception
        en = MoreEnumerable([''])
        q = en.segment(pred).select(lambda x: x.to_list())
        assert q.to_list() == [['']]

    def test_segment_reiterate(self):
        ints = [1, 2, 3]
        en = MoreEnumerable(ints)
        q = en.segment(lambda x: True)
        for segment in q:
            assert segment.to_list() == segment.to_list()

    def test_segment2_split_on_first(self):
        ints = [0, 1, 2, 4, -4, -2, 6, 2, -2]
        en = MoreEnumerable(ints)
        q = en.segment2(lambda x, i: x < 0 or i % 3 == 0) \
            .select(Enumerable.to_list)
        assert q.to_list() == [[0, 1, 2], [4], [-4], [-2], [6, 2], [-2]]

    @pytest.mark.parametrize('func,expected', [
        (lambda curr, prev, _: curr * prev < 0,
            [[0, 1, 2, 4], [-4, -2], [6, 2], [-2]]),
        (lambda curr, prev, i: curr < 0 and prev >= 0 or i == 1,
            [[0], [1, 2, 4], [-4, -2, 6, 2], [-2]]),
    ])
    def test_segment3(self, func: Callable[[int, int, int], bool], expected: List[List[int]]):
        ints = [0, 1, 2, 4, -4, -2, 6, 2, -2]
        en = MoreEnumerable(ints)
        q = en.segment3(func).select(Enumerable.to_list)
        assert q.to_list() == expected


class TestCycleMethod:
    def test_repeat(self):
        en = MoreEnumerable([1, 2, 3])
        assert en.cycle(3).to_list() == [1, 2, 3] * 3

    def test_no_elem(self):
        en = MoreEnumerable([])
        assert en.cycle(3).to_list() == []

    def test_zero_count(self):
        en = MoreEnumerable([1, 2, 3])
        assert en.cycle(0).to_list() == []

    def test_one_count(self):
        en = MoreEnumerable([1, 2, 3])
        assert en.cycle(1).to_list() == en.to_list()

    def test_infinite_count(self):
        def gen():
            yield from [1, 2]
        en = MoreEnumerable(gen())
        assert en.cycle(None).take(11).to_list() == [1, 2] * 5 + [1]

    def test_invalid(self):
        en = MoreEnumerable([1, 2, 3])
        with pytest.raises(InvalidOperationError):
            en.cycle(-1)


class TestTraverseBreathFirstMethod:
    tree = Tree \
    (
        left=Tree
        (
            left=Tree(0),
            val=1,
            right=Tree(2),
        ),
        val=3,
        right=Tree
        (
            left=None,
            val=4,
            right=Tree(5),
        )
    )

    @staticmethod
    def selector(n: Tree):
        return [t for t in (n.left, n.right) if t is not None]

    def test_traverse_tree(self):
        en = MoreEnumerable.traverse_breath_first(self.tree, self.selector)
        assert en.select(lambda n: n.val).to_list() == [3, 1, 4, 0, 2, 5]

    def test_preserve_children_order(self):
        en = MoreEnumerable.traverse_breath_first(0, lambda i: [*range(1, 10)] if i == 0 else [])
        assert en.to_list() == [*range(10)]

    def test_single(self):
        en = MoreEnumerable.traverse_breath_first(0, lambda _: ())
        assert en.to_list() == [0]


class TestTraverseDepthFirstMethod:
    def test_traverse_tree(self):
        en = MoreEnumerable.traverse_depth_first(
            TestTraverseBreathFirstMethod.tree,
            TestTraverseBreathFirstMethod.selector,
        )
        assert en.select(lambda n: n.val).to_list() == [3, 1, 0, 2, 4, 5]

    def test_preserve_children_order(self):
        en = MoreEnumerable.traverse_depth_first(0, lambda i: [*range(1, 10)] if i == 0 else [])
        assert en.to_list() == [*range(10)]

    def test_single(self):
        en = MoreEnumerable.traverse_depth_first(0, lambda _: ())
        assert en.to_list() == [0]


class TestTraverseTopologicalMethod:
    def test_overload1_simple(self):
        adj = {
            5: [2, 0],
            4: [0, 1],
            2: [3],
            3: [1],
        }
        en = MoreEnumerable([5, 4]).traverse_topological(lambda x: adj.get(x, ()))
        assert en.to_list() == [5, 2, 3, 4, 0, 1]

    def test_overload1_linear_dfs(self):
        en = MoreEnumerable([TestTraverseBreathFirstMethod.tree]) \
            .traverse_topological(TestTraverseBreathFirstMethod.selector)
        assert en.select(lambda n: n.val).to_list() == [3, 1, 0, 2, 4, 5]

    def test_overload1_all_nodes(self):
        adj = [
            [1, 2, 3],
            [3],
            [1, 3],
            [],
        ]
        en = MoreEnumerable(range(4)).traverse_topological(adj.__getitem__)
        assert en.to_list() == [0, 2, 1, 3]

    def test_overload1_single(self):
        en = MoreEnumerable([0]).traverse_topological(lambda _: ())
        assert en.to_list() == [0]

    def test_overload1_cycle(self):
        adj = {
            5: [2, 0],
            4: [0, 1],
            2: [3],
            3: [1, 5],
        }
        en = MoreEnumerable([5, 4]).traverse_topological(lambda x: adj.get(x, ()))
        with pytest.raises(DirectedGraphNotAcyclicError) as excinfo:
            en.to_list()
        assert excinfo.value.cycle == (3, 5)

    def test_overload1_self_loop(self):
        adj = {
            1: [2, 3],
            3: [4],
            4: [5, 6, 4, 7],
        }
        en = MoreEnumerable([1]).traverse_topological(lambda x: adj.get(x, ()))
        with pytest.raises(DirectedGraphNotAcyclicError) as excinfo:
            en.to_list()
        assert excinfo.value.cycle == (4, 4)

    def test_overload2_big(self):
        adj = {
            0: [1, 2],
            3: [2],
            10: [12],
            11: [12],
            1: [5, 4],
            2: [4],
            12: [13],
            5: [6],
            4: [9],
            13: [4],
            6: [7, 8, 9],
        }
        roots = map(Node, [0, 3, 4, 10, 11])
        en = MoreEnumerable(roots).traverse_topological(
            lambda x: map(Node, adj.get(x.val, ())),
            lambda x: x.val,
        )
        assert en.select(lambda x: x.val).to_list() \
            == [0, 1, 5, 6, 7, 8, 3, 2, 10, 11, 12, 13, 4, 9]

    def test_overload2_diamond(self):
        adj = {
            0: [2],
            1: [2, 3, 8],
            2: [4, 5],
            3: [7],
            4: [6],
            5: [6],
            6: [],
            7: [8],
            8: [],
        }
        roots = map(Node, [0, 1])
        en = MoreEnumerable(roots).traverse_topological(
            lambda x: map(Node, adj[x.val]),
            lambda x: x.val,
        )
        assert en.select(lambda x: x.val).to_list() \
            == [0, 1, 2, 4, 5, 6, 3, 7, 8]

    def test_overload2_two_cycles_get_first(self):
        adj = {
            0: [1, 2],
            3: [2],
            10: [12],
            11: [12],
            1: [5, 4],
            2: [4],
            12: [13],
            5: [6],
            4: [9],
            13: [4, 12],
            6: [7, 9],
            9: [3],
        }
        roots = map(Node, [0, 3, 4, 10, 11])
        en = MoreEnumerable(roots).traverse_topological(
            lambda x: map(Node, adj.get(x.val, ())),
            lambda x: x.val,
        )
        count = set()
        with pytest.raises(DirectedGraphNotAcyclicError) as excinfo:
            for node in en:
                count.add(node.val)
        A, B = excinfo.value.cycle
        assert [A.val, B.val] == [2, 4]  # type: ignore
        assert len(count) < 14
