import sys, os
from typing import Generic, Iterable, List, TypeVar, cast

import pytest


sys.path.append(os.path.abspath('..'))  # run in tests folder
sys.path.append(os.path.abspath('.'))  # run in root folder
from types_linq import Enumerable


TSource_co = TypeVar('TSource_co', covariant=True)


class BasicIterable(Generic[TSource_co]):
    def __init__(self, it: Iterable[TSource_co]):
        self._it = it
    def __iter__(self):
        yield from self._it


class TestIterMethod:
    def test_list(self):
        'repeatable iterable.'
        lst = ['x', 'y', 'z']
        en = Enumerable(lst)
        assert en.to_list() == ['x', 'y', 'z']
        assert en.to_list() == ['x', 'y', 'z']

    def test_generator_object(self):
        'non-repeatable generator object'
        gen = (chr(i) for i in range(120, 123))
        en = Enumerable(gen)
        assert en.to_list() == ['x', 'y', 'z']
        assert en.to_list() == []

    def test_list_factory(self):
        'function that returns a repeatable iterable (this use case is kind of useless)'
        lst_func = lambda: ['x', 'y', 'z']
        en = Enumerable(lst_func)
        assert en.to_list() == ['x', 'y', 'z']
        assert en.to_list() == ['x', 'y', 'z']

    def test_generator_function(self):
        'function that returns non-repeatable generator object'
        gen_func = lambda: (chr(i) for i in range(120, 123))
        en = Enumerable(gen_func)
        assert en.to_list() == ['x', 'y', 'z']
        assert en.to_list() == ['x', 'y', 'z']


class TestAggregateMethod:
    def test_overload1(self):
        fruits = ['apple', 'mango', 'orange', 'passionfruit', 'grape']
        en = Enumerable(fruits)
        longest = en.aggregate('banana', lambda acc, e: e if len(e) > len(acc) else acc, str.upper)
        assert longest == 'PASSIONFRUIT'

    def test_overload1_empty(self):
        fruits: List[str] = []
        en = Enumerable(fruits)
        longest = en.aggregate('banana', lambda acc, e: e if len(e) > len(acc) else acc, str.upper)
        assert longest == 'BANANA'

    def test_overload1_1(self):
        fruits = ['appleell']
        en = Enumerable(fruits)
        longest = en.aggregate('banana', lambda acc, e: e if len(e) > len(acc) else acc, lambda r: f'__{r}__')
        assert longest == '__appleell__'

    def test_overload2(self):
        'implementation same as overload1'
        fruits = ['apple', 'mango', 'orange', 'passionfruit', 'grape']
        en = Enumerable(fruits)
        longest = en.aggregate('banana', lambda acc, e: e if len(e) > len(acc) else acc)
        assert longest == 'passionfruit'

    def test_overload3(self):
        words = 'the quick brown fox jumps over the lazy dog'.split(' ')
        en = Enumerable(words)
        reversed_ = en.aggregate(lambda acc, e: f'{e} {acc}')
        assert reversed_ == 'dog lazy the over jumps fox brown quick the'

    def test_overload3_empty(self):
        ints: List[int] = []
        en = Enumerable(ints)
        with pytest.raises(TypeError):
            en.aggregate(lambda acc, e: cast(int, acc + e))

    def test_overload3_1(self):
        ints = [87]
        en = Enumerable(ints)
        sole = en.aggregate(lambda acc, e: cast(int, acc + e))
        assert sole == 87


class TestAllMethod:
    def test_all(self):
        ints = [1, 3, 5, 7, 9]
        en = Enumerable(ints)
        all_odd = en.all(lambda e: e % 2 == 1)
        assert all_odd is True

    def test_not_all(self):
        ints = [1, 2, 3, 5, 7, 9]
        en = Enumerable(ints)
        all_odd = en.all(lambda e: e % 2 == 1)
        assert all_odd is False

    def test_empty(self):
        ints: List[int] = []
        en = Enumerable(ints)
        all_odd = en.all(lambda e: e % 2 == 1)
        assert all_odd is True


class TestAnyMethod:
    def test_overload1_has(self):
        ints = [1, 2]
        assert Enumerable(ints).any() is True

    def test_overload1_empty(self):
        ints: List[int] = []
        assert Enumerable(ints).any() is False

    def test_overload2_has(self):
        ints = [1, 3, 5, 8, 9, 11]
        en = Enumerable(ints)
        has_even = en.any(lambda e: e % 2 == 0)
        assert has_even is True

    def test_overload2_no(self):
        ints = [1, 3, 5, 9, 11]
        en = Enumerable(ints)
        has_even = en.any(lambda e: e % 2 == 0)
        assert has_even is False

    def test_overload2_empty(self):
        ints: List[int] = []
        en = Enumerable(ints)
        has_even = en.any(lambda e: e % 2 == 0)
        assert has_even is False


class TestAppendMethod:
    def test_no_mutate(self):
        ints: List[int] = []
        en = Enumerable(ints)
        en2 = en.append(7).append(8)
        assert ints == []
        assert en.to_list() == []
        assert en2.to_list() == [7, 8]


class TestAverageMethod:
    def test_average_overload1(self):
        ints = [1, 3, 5, 9, 11]
        avg = Enumerable(ints).average()
        assert avg == 5.8

    def test_average_overload1_1(self):
        ints = [44]
        avg = Enumerable(ints).average()
        assert avg == 44

    def test_average_overload1_empty(self):
        ints: List[int] = []
        with pytest.raises(TypeError):
            Enumerable(ints).average()

    def test_average_overload2(self):
        lst = [[1], [3], [5], [9], [11]]
        en = Enumerable(lst)
        avg = en.average(lambda e: e[0])
        assert avg == 5.8

    def test_average2_overload1(self):
        ints = [1, 3, 5, 9, 11]
        avg = Enumerable(ints).average2(69)
        assert avg == 5.8

    def test_average2_overload1_empty(self):
        ints: List[int] = []
        avg = Enumerable(ints).average2(False)
        assert avg == False

    def test_average2_overload2(self):
        lst = [[1], [3], [5], [9], [11]]
        en = Enumerable(lst)
        avg = en.average2(lambda e: e[0], 44)
        assert avg == 5.8


class TestConcatMethod:
    def test_concat(self):
        en1 = Enumerable([1, 2, 3])
        en2 = Enumerable([1, 2, 4])
        en3 = en1.concat(en2)
        assert en3.to_list() == [1, 2, 3, 1, 2, 4]
        en4 = en1.concat(en1).concat(en2).concat([]).concat([16])
        assert en4.to_list() == [1, 2, 3, 1, 2, 3, 1, 2, 4, 16]


class TestContainsMethod:
    def test_overload1(self):
        lst = BasicIterable(['x', 'y', 'z'])
        en = Enumerable(lst)
        assert en.contains('x') is en.contains('y') is en.contains('z') is True
        assert en.contains('t') is False
        assert en.contains(object()) is False

    def test_overload1_empty(self):
        lst: List[str] = []
        en = Enumerable(lst)
        assert en.contains('x') is False

    def test_overload2(self):
        lst = ['x', 'y', 'z']
        en = Enumerable(lst)
        assert en.contains(120, lambda lhs, rhs: lhs == chr(rhs)) is True
        assert en.contains(123, lambda lhs, rhs: lhs == chr(rhs)) is False

    def test_call_in(self):
        class OnlyHasIn(BasicIterable[TSource_co]):
            def __contains__(self, _: object):
                return True
        en = Enumerable(OnlyHasIn([]))
        assert en.contains(1) is en.contains(89) is en.contains('') is True


class TestCountMethod:
    def test_overload1(self):
        lst = BasicIterable(['x', 'y', 'z'])
        en = Enumerable(lst)
        assert en.count() == 3

    def test_overload2(self):
        lst = ('x', 'y', 120, 'z')
        en = Enumerable(lst)
        assert en.count(lambda e: isinstance(e, str)) == 3
        assert en.count(lambda e: isinstance(e, float)) == 0

    def test_call_len(self):
        class OnlyHasLen(BasicIterable[TSource_co]):
            def __len__(self):
                return 179
        en = Enumerable(OnlyHasLen([]))
        assert en.count() == 179


class TestDefaultIfEmptyMethod:
    def test_non_empty(self):
        lst = [44]
        en = Enumerable(lst)
        assert en.default_if_empty(17).to_list() == [44]

    def test_non_empty2(self):
        lst = [44, 45, 56]
        en = Enumerable(lst)
        assert en.default_if_empty(17).to_list() == [44, 45, 56]

    def test_empty(self):
        lst: List[int] = []
        en = Enumerable(lst)
        assert en.default_if_empty(17).to_list() == [17]
