from dataclasses import dataclass
from typing import Any, List, Optional, cast

import pytest

from types_linq import Enumerable, InvalidOperationError
from types_linq.more import MoreEnumerable


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
        en = MoreEnumerable(range(0, 5))
        expr = en.aggregate_right('5', lambda e, rr: f'(cons {e} {rr})')
        assert expr == '(cons 0 (cons 1 (cons 2 (cons 3 (cons 4 5)))))'

    def test_overload3(self):
        en = MoreEnumerable(range(0, 5))
        expr = en.aggregate_right(lambda e, rr: f'(cons {e} {rr})')
        assert expr == '(cons 0 (cons 1 (cons 2 (cons 3 4))))'

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
