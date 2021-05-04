import pytest

from typing import List
from types_linq import Enumerable, MoreEnumerable, InvalidOperationError


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
