import sys, os
from typing import Generic, Iterable, List, Sequence, TypeVar, cast

import pytest


sys.path = [os.path.abspath('..')]  # run in tests folder
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


class TestIterMethod2:
    def test_to_set(self):
        gen = (i % 5 if i != 77 else i for i in range(0, 100))
        en = Enumerable(gen)
        assert en.to_set() == {0, 1, 2, 3, 4, 77}

    def test_to_dict_overload1(self):
        gen = ((i, chr(i)) for i in range(120, 123))
        en = Enumerable(gen)
        dict_ = en.to_dict(lambda e: e[0], lambda e: e[1])
        assert dict_ == {120: 'x', 121: 'y', 122: 'z'}

    def test_to_dict_overload2(self):
        gen = ((i, chr(i)) for i in range(120, 121))
        en = Enumerable(gen)
        dict_ = en.to_dict(lambda e: e[0])
        assert dict_ == {120: (120, 'x')}


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


class TestDistinctMethod:
    def test_distinct(self):
        lst = [1, 4, 5, 6, 4, 3, 1, 99]
        en = Enumerable(lst)
        distinct = en.distinct().to_list()
        assert distinct == [1, 4, 5, 6, 3, 99]


class TestReverseMethod:
    def test_delayed(self):
        gen = (i for i in range(5))
        en = Enumerable(gen).reverse()
        assert gen.gi_frame is not None
        assert en.to_list() == [4, 3, 2, 1, 0]
        assert gen.gi_frame is None

    def test_call_reversed(self):
        class OnlyHasReversed(BasicIterable[TSource_co]):
            def __reversed__(self):
                yield from [5, 9]
        en = Enumerable(OnlyHasReversed([]))
        assert en.reverse().to_list() == [5, 9]


class TestElementAtMethod:
    def test_overload1_0(self):
        gen = lambda: (i for i in range(7, 12))
        en = Enumerable(gen)
        assert en.element_at(0) == 7

    def test_overload1_end(self):
        gen = lambda: (i for i in range(7, 12))
        en = Enumerable(gen)
        assert en.element_at(4) == 11

    def test_overload1_out(self):
        gen = lambda: (i for i in range(7, 12))
        en = Enumerable(gen)
        with pytest.raises(IndexError):
            en.element_at(5)

    def test_overload2_out(self):
        gen = lambda: (i for i in range(7, 12))
        en = Enumerable(gen)
        assert en.element_at(5, float) == float

    def test_call_getitem(self):
        en = Enumerable(self.OnlyHasGetItem([]))
        assert en.element_at(142512) == 'haha'

    class OnlyHasGetItem(Sequence[TSource_co], BasicIterable[TSource_co]):
        def __len__(self):
            return 0
        def __getitem__(self, _):
            return 'haha'

    class TestGetItem:
        'element_at() does not cover all of the __getitem__() content. do them here.'
        def test_no_arg(self):
            gen = lambda: (i for i in range(5))
            q = Enumerable(gen)[:]
            assert q.to_list() == [0, 1, 2, 3, 4]

        @pytest.mark.parametrize('slicing,expected', [
            (slice(None, None, 1), [*range(15)][::1]),
            (slice(None, None, 2), [*range(15)][::2]),
            (slice(None, None, 3), [*range(15)][::3]),
            (slice(None, None, 4), [*range(15)][::4]),
            (slice(None, None, 5), [*range(15)][::5]),
            (slice(None, None, 6), [*range(15)][::6]),
            (slice(None, None, 14), [*range(15)][::14]),
            (slice(None, None, 15), [*range(15)][::15]),  # [0]
            (slice(None, None, 16), [*range(15)][::16]),  # [0]
            (slice(None, None, 17), [*range(15)][::17]),  # [0]
            (slice(None, None, -1), [*range(15)][::-1]),
            (slice(None, None, -2), [*range(15)][::-2]),
            (slice(None, None, -3), [*range(15)][::-3]),
            (slice(None, None, -4), [*range(15)][::-4]),
            (slice(None, None, -5), [*range(15)][::-5]),
            (slice(None, None, -14), [*range(15)][::-14]),
            (slice(None, None, -15), [*range(15)][::-15]),  # [14]
            (slice(None, None, -16), [*range(15)][::-16]),  # [14]
        ])
        def test_steps(self, slicing: slice, expected: List[int]):
            gen = lambda: (i for i in range(15))
            q = Enumerable(gen)[slicing]
            assert q.to_list() == expected

        @pytest.mark.parametrize('slicing,expected', [
            (slice(None, 7), list(range(0, 7))),
            (slice(0, 0), []),
            (slice(1, 1), []),
            (slice(0, 7), list(range(0, 7))),
            (slice(1, 7), list(range(1, 7))),
            (slice(2, 7), list(range(2, 7))),
            (slice(7, 7), list(range(7, 7))),  # []
            (slice(8, 7), list(range(8, 7))),  # []
            (slice(2, 8), list(range(2, 8))),
            (slice(2, 7, 1), list(range(2, 7))),
            (slice(2, 7, 2), list(range(2, 7, 2))),
            (slice(2, 7, 3), list(range(2, 7, 3))),
            (slice(3, 23, 2), list(range(3, 23, 2))),
            (slice(3, 23, 3), list(range(3, 23, 3))),
            (slice(7, 2, -1), list(range(7, 2, -1))),
            (slice(7, 2, -2), list(range(7, 2, -2))),
            (slice(7, 2, -3), list(range(7, 2, -3))),
            (slice(23, 3, -2), list(range(23, 3, -2))),
            (slice(23, 3, -3), list(range(23, 3, -3))),
        ])
        def test_within_inf_generator(self, slicing: slice, expected: List[int]):
            def gen():
                i = 0
                while True:
                    yield i
                    i += 1
            q = Enumerable(gen)[slicing]
            assert q.to_list() == expected

        @pytest.mark.parametrize('slicing,expected', [
            (slice(None, 15, 1), [*range(30)][:15:1]),
            (slice(None, 15, 2), [*range(30)][:15:2]),
            (slice(None, 15, 3), [*range(30)][:15:3]),
            (slice(None, 15, -1), [*range(30)][:15:-1]),
            (slice(None, 15, -2), [*range(30)][:15:-2]),
            (slice(None, 15, -3), [*range(30)][:15:-3]),
        ])
        def test_missing_start(self, slicing: slice, expected: List[int]):
            gen = lambda: (i for i in range(30))
            q = Enumerable(gen)[slicing]
            assert q.to_list() == expected

        @pytest.mark.parametrize('slicing,expected', [
            (slice(23, None, 1), [*range(30)][23::1]),
            (slice(23, None, 2), [*range(30)][23::2]),
            (slice(23, None, 3), [*range(30)][23::3]),
            (slice(23, None, -2), [*range(30)][23::-2]),
            (slice(23, None, -3), [*range(30)][23::-3]),
        ])
        def test_missing_stop(self, slicing: slice, expected: List[int]):
            gen = lambda: (i for i in range(30))
            q = Enumerable(gen)[slicing]
            assert q.to_list() == expected

        @pytest.mark.parametrize('slicing,expected', [
            (slice(-3, 23, -1),[*range(30)][-3:23:-1]),
            (slice(23, -23, 1), [*range(30)][23:-23:1]),
        ])
        def test_negative_idx(self, slicing: slice, expected: List[int]):
            gen = lambda: (i for i in range(30))
            q = Enumerable(gen)[slicing]
            assert q.to_list() == expected

        def test_call_getitem(self):
            en = Enumerable(TestElementAtMethod.OnlyHasGetItem([]))
            assert en[slice(None)].to_list() == ['h', 'a', 'h', 'a']



class TestEmptyMethod:
    def test_empty(self):
        assert Enumerable.empty().to_list() == []


class TestExceptMethod:
    def test_except1(self):
        ints = [4, 88, 21, -5, 25, 12, 77, 79, 0, 0]
        en = Enumerable(ints)
        exc = en.except1([88, 77, 21, 79, 77])
        assert exc.to_list() == [4, -5, 25, 12, 0]

    def test_remove_nothing(self):
        ints = [4, -5, 25, 12, 0]
        en = Enumerable(ints)
        exc = en.except1(Enumerable.empty().cast(int))
        assert exc.to_list() == ints


class TestSelectMethod:
    def test_select(self):
        gen_func = lambda: (i for i in range(4))
        en = Enumerable(gen_func)
        doubled = en.select(lambda e: e * 2)
        assert doubled.to_list() == [0, 2, 4, 6]

    def test_select2(self):
        gen_func = lambda: (i for i in range(4))
        en = Enumerable(gen_func)
        doubled = en.select2(lambda e, i: e * i)
        assert doubled.to_list() == [0, 1, 4, 9]


class TestSelectManyMethod:
    def test_selectmany_overload1(self):
        pet_owners = [
            {'name': 'Higa', 'pets': ['Scruffy', 'Sam']},
            {'name': 'Ashkenazi', 'pets': ['Walker', 'Sugar']},
            {'name': 'Hines',  'pets': ['Dusty']},
        ]
        en = Enumerable(pet_owners)
        pets = en.select_many(
            lambda owner: owner['pets'],
            lambda owner, name: (name, owner['name']),
        )
        assert pets.to_list() == [
            ('Scruffy', 'Higa'), ('Sam', 'Higa'),
            ('Walker', 'Ashkenazi'), ('Sugar', 'Ashkenazi'),
            ('Dusty', 'Hines'),
        ]

    def test_selectmany_overload2(self):
        dinner = ['ramen', 'pork']
        en = Enumerable(dinner)
        letters = en.select_many(lambda e: e)
        assert letters.to_list() == ['r', 'a', 'm', 'e', 'n', 'p', 'o', 'r', 'k']

    def test_selectmany2_overload1(self):
        'test case does not make sense practically.. but i cannot think of any more.'
        dinner = [(533, ['ramen', 'rice']), (16, ['pork'])]
        en = Enumerable(dinner)
        q = en.select_many2(
            lambda tup, i: [i] + tup[1],
            lambda src, c: f'{src[0]}.{c}',
        )
        assert q.to_list() == ['533.0', '533.ramen', '533.rice', '16.1', '16.pork']

    def test_selectmany2_overload2(self):
        dinner = ['Ramen with Egg and Beef', 'Gyoza', 'Fried Chicken']
        en = Enumerable(dinner)
        q = en.select_many2(
            lambda e, i: Enumerable(e.split(' '))
                .where(lambda w: w[0] == w[0].upper())
                .select(lambda w: f'{i}.{w}')
        )
        assert q.to_list() == [
            '0.Ramen', '0.Egg', '0.Beef', '1.Gyoza', '2.Fried', '2.Chicken',
        ]


class TestSkipMethod:
    def test_some(self):
        lst = [1, 4, 6, 9, 10]
        en = Enumerable(lst)
        assert en.skip(1).to_list() == [4, 6, 9, 10]
        assert en.skip(3).to_list() == [9, 10]
        assert en.skip(5).to_list() == []

    def test_elems_fewer(self):
        lst = [1, 4, 6, 9, 10]
        en = Enumerable(lst)
        assert en.skip(6).to_list() == []
        assert en.skip(6).skip(2).to_list() == []

    def test_count_zero_or_negative(self):
        lst = [1, 4, 6, 9, 10]
        en = Enumerable(lst)
        assert en.skip(0).to_list() == lst
        assert en.skip(-1).to_list() == lst


class TestTakeMethod:
    def test_some(self):
        lst = [1, 4, 6, 9, 10]
        en = Enumerable(lst)
        assert en.take(3).to_list() == [1, 4, 6]
        assert en.take(5).to_list() == lst

    def test_more(self):
        lst = [1, 4, 6, 9, 10]
        en = Enumerable(lst)
        assert en.take(6).to_list() == lst

    def test_count_zero_or_negative(self):
        lst = [1, 4, 6, 9, 10]
        en = Enumerable(lst)
        assert en.take(0).to_list() == []
        assert en.take(-1).to_list() == []

    def test_id(self):
        lst = [1, 4, 6, 9, 10]
        en = Enumerable(lst)
        assert en.take(4).concat(en.skip(4)).to_list() == lst


class TestWhereMethod:
    def test_where(self):
        gen_func = lambda: (i for i in range(0, 10))
        en = Enumerable(gen_func)
        evens = en.where(lambda e: e % 2 == 0)
        assert evens.to_list() == [0, 2, 4, 6, 8]

    def test_where2(self):
        gen_func = lambda: (i for i in range(0, 10))
        en = Enumerable(gen_func)
        wholes = en.where2(lambda e, i: e % 2 == i % 3 == 0)
        assert wholes.to_list() == [0, 6]


class TestZipMethod:
    def test_overload1(self):
        lst = [1, 2, 3, 4]
        other_lst = ['x', 'y', 'z', 't']
        en = Enumerable(lst)
        zipped = en.zip(other_lst, lambda x, y: f'{x}{y}')
        assert zipped.to_list() == ['1x', '2y', '3z', '4t']

    def test_overload2(self):
        lst = [1, 2, 3, 4]
        other_lst = ['x', 'y', 'z', 't']
        en = Enumerable(lst)
        zipped = en.zip(Enumerable(other_lst))
        assert zipped.to_list() == [(1, 'x'), (2, 'y'), (3, 'z'), (4, 't')]

    def test_different_len(self):
        'take shorter'
        lst = [1, 2, 3, 4]
        other_lst = ['x', 'y', 'z', 't']
        en = Enumerable(lst).append(5)
        zipped = en.zip(Enumerable(other_lst).append('u').append('v'))
        assert zipped.to_list() == [(1, 'x'), (2, 'y'), (3, 'z'), (4, 't'), (5, 'u')]
