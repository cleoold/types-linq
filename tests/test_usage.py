import math
from typing import Generic, Iterable, List, NamedTuple, Sequence, Tuple, TypeVar, cast

import pytest

from types_linq import Enumerable, InvalidOperationError, IndexOutOfRangeError


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

    def test_to_tuple(self):
        gen = (chr(i) for i in range(120, 123))
        en = Enumerable(gen)
        assert en.to_tuple() == ('x', 'y', 'z')

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
        with pytest.raises(InvalidOperationError, match='Sequence is empty'):
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
        with pytest.raises(InvalidOperationError):
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


class TestChunkMethod:
    def test_infinite_exact(self):
        def source(i):
            while True:
                yield i
                i *= 3
        en = Enumerable(source(1)).chunk(4).take(3)
        assert en.to_list() == [
            [1, 3, 9, 27], [81, 243, 729, 2187], [6561, 19683, 59049, 177147],
        ]

    def test_sized_last_not_full(self):
        ints = [1, 3, 9, 27, 81, 243, 729]
        en = Enumerable(ints).chunk(3)
        assert en.to_list() == [[1, 3, 9], [27, 81, 243], [729]]

    def test_elements_less_than_size(self):
        ints = [1, 3, 9, 27]
        en = Enumerable(ints).chunk(5)
        assert en.to_list() == [[1, 3, 9, 27]]

    def test_empty(self):
        en = Enumerable([])
        assert en.chunk(3).to_list() == []

    def test_mutate_source_before_iteration(self):
        ints = [1, 3, 9, 27, 81, 243, 729]
        en = Enumerable(ints).chunk(2)
        it = iter(en)
        assert next(it) == [1, 3]
        ints.remove(27)
        assert next(it) == [9, 81]
        assert next(it) == [243, 729]

    def test_invalid_size(self):
        en = Enumerable([0])
        with pytest.raises(InvalidOperationError):
            en.chunk(0)
        with pytest.raises(InvalidOperationError):
            en.chunk(-1)


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

    def test_fallingback(self):
        class OnlyHasIn(BasicIterable[TSource_co]):
            def __contains__(self, _: object):
                return True
        en = Enumerable(OnlyHasIn([]))
        assert en.contains(1) is en.contains(89) is en.contains('') is False
        assert (1 in en) is (89 in en) is ('' in en) is True
        en2 = Enumerable(BasicIterable([]))
        assert en2.contains(1) is en2.contains(89) is en2.contains('') is False
        assert (1 in en2) is (89 in en2) is ('' in en2) is False


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

    def test_fallback(self):
        class OnlyHasLen(BasicIterable[TSource_co]):
            def __len__(self):
                return 179
        en = Enumerable(OnlyHasLen([]))
        assert en.count() == 0
        assert len(en) == 179
        en2 = Enumerable(BasicIterable([]))
        assert en2.count() == 0
        assert len(en2) == 0


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

    def test_fallback(self):
        class OnlyHasReversed(BasicIterable[TSource_co]):
            def __reversed__(self):
                yield from [5, 9]
        en = Enumerable(OnlyHasReversed([1, 2]))
        assert en.reverse().to_list() == [2, 1]
        assert [i for i in reversed(en)] == [5, 9]
        en2 = Enumerable(BasicIterable([1, 2]))
        assert en2.reverse().to_list() == [2, 1]
        assert [i for i in reversed(en2)] == [2, 1]


class TestElementAtMethod:
    def test_overload1_0(self):
        gen = lambda: (i for i in range(7, 12))
        en = Enumerable(gen)
        assert en.element_at(0) == 7
        assert en.element_at(-5) == 7

    def test_overload1_end(self):
        gen = lambda: (i for i in range(7, 12))
        en = Enumerable(gen)
        assert en.element_at(4) == 11
        assert en.element_at(-1) == 11

    def test_overload1_out(self):
        gen = lambda: (i for i in range(7, 12))
        en = Enumerable(gen)
        with pytest.raises(IndexOutOfRangeError):
            en.element_at(5)
        with pytest.raises(IndexOutOfRangeError):
            en.element_at(-6)

    def test_overload2_within(self):
        gen = lambda: (i for i in range(7, 12))
        en = Enumerable(gen)
        assert en.element_at(2, 0) == 9
        assert en.element_at(-3, 0) == 9

    def test_overload2_out(self):
        gen = lambda: (i for i in range(7, 12))
        en = Enumerable(gen)
        assert en.element_at(5, float) == float

    def test_fallback(self):
        en = Enumerable(self.OnlyHasGetItem([]))
        with pytest.raises(IndexOutOfRangeError):
            en.element_at(142512)
        assert en[142512] == 'haha'
        en2 = Enumerable(BasicIterable([]))
        with pytest.raises(IndexOutOfRangeError):
            en2.element_at(142512)
        with pytest.raises(IndexOutOfRangeError):
            en2[142512]
        en3 = Enumerable([])
        with pytest.raises(IndexOutOfRangeError):
            en.element_at(1)
        with pytest.raises(IndexOutOfRangeError):
            en3[1]

    def test_not_fallback_and_with_default(self):
        en = Enumerable([1])
        assert en[0, 'haha'] == 1
        assert en[1, 'haha'] == 'haha'


    class OnlyHasGetItem(BasicIterable[TSource_co], Sequence[TSource_co]):
        # note: we get into troubles if Sequence is the first superclass
        # since its __iter__ method would be chosen over that of BasicIterable
        def __len__(self):
            return 0
        def __getitem__(self, _):
            return 'haha'


class TestEmptyMethod:
    def test_empty(self):
        assert Enumerable.empty().to_list() == []


class TestExceptMethod:
    def test_except1(self):
        ints = [4, 88, 21, -5, 25, 12, 77, 79, 0, 0]
        en = Enumerable(ints)
        exc = en.except1([88, 77, 21, 66, 79, 77])
        assert exc.to_list() == [4, -5, 25, 12, 0]

    def test_except1_unhashable(self):
        lst = [[1, 2, 3], [4, 5], [6, 7], [6, 7]]
        en = Enumerable(lst)
        exc = en.except1([[4, 5], [1, 2, 3]])
        assert exc.to_list() == [[6, 7]]

    def test_remove_nothing(self):
        ints = [4, -5, 25, 12, 0]
        en = Enumerable(ints)
        exc = en.except1(Enumerable.empty().cast(int))
        assert exc.to_list() == ints


class TestFirstMethod:
    def test_first_overload1_yes(self):
        lst = ('a', 'b', 5, 'c')
        en = Enumerable(lst)
        assert en.first() is 'a'

    def test_first_overload1_no(self):
        with pytest.raises(InvalidOperationError):
            Enumerable({}).first()

    def test_first_overload2_yes(self):
        lst = ('a', 'b', 5, 'c', 6, 'd')
        en = Enumerable(lst)
        assert en.first(lambda e: isinstance(e, int)) == 5

    def test_first_overload2_no(self):
        lst = ('a', 'b', 5, 'c', 6, 'd')
        en = Enumerable(lst)
        with pytest.raises(InvalidOperationError):
            assert en.first(lambda e: isinstance(e, tuple))

    def test_first2_overload1_yes(self):
        lst = ('a', 'b', 5, 'c')
        en = Enumerable(lst)
        assert en.first2(set) is 'a'

    def test_first2_overload1_no(self):
        assert Enumerable({}).first2(set) == set

    def test_first2_overload2_yes(self):
        lst = ('a', 'b', 5, 'c', 6, 'd')
        en = Enumerable(lst)
        assert en.first2(lambda e: isinstance(e, int), 'A') == 5

    def test_first2_overload2_no(self):
        lst = ('a', 'b', 5, 'c', 6, 'd')
        en = Enumerable(lst)
        assert en.first2(lambda e: isinstance(e, tuple), 'A') == 'A'


class TestGroupByMethod:
    pets_list: List[Tuple[str, float]] = [
        ('Barley', 8.3), ('Boots', 4.9), ('Whiskers', 1.5), ('Daisy', 4.3),
        ('Roman', 8.6), ('Fangus', 8.6), ('Roam', 2.2), ('Roll', 1.4),
    ]

    def test_group_by_overload1(self):
        en = Enumerable(TestGroupByMethod.pets_list)
        q = en.group_by(
            lambda pet: math.floor(pet[1]),
            lambda pet: pet[0],
            lambda age_floored, names: (age_floored, names.to_list()),
        )
        assert q.to_list() == [
            (8, ['Barley', 'Roman', 'Fangus']),
            (4, ['Boots', 'Daisy']),
            (1, ['Whiskers', 'Roll']),
            (2, ['Roam']),
        ]

    def test_group_by_overload2(self):
        en = Enumerable(TestGroupByMethod.pets_list)
        q = en.group_by(
            lambda pet: math.floor(pet[1]),
            lambda pet: pet[0],
        )
        # simulate for loop
        it = iter(q)
        g1 = next(it)
        assert g1.key == 8
        assert g1.to_list() == ['Barley', 'Roman', 'Fangus']
        next(it); next(it); next(it)
        with pytest.raises(StopIteration):
            next(it)

    def test_group_by2_overload1(self):
        en = Enumerable(TestGroupByMethod.pets_list)
        q = en.group_by2(
            lambda pet: math.floor(pet[1]),
            lambda age_floored, names: (age_floored, names.to_list()),
        )
        assert q.to_list() == [
            (8, [('Barley', 8.3), ('Roman', 8.6), ('Fangus', 8.6)]),
            (4, [('Boots', 4.9), ('Daisy', 4.3)]),
            (1, [('Whiskers', 1.5), ('Roll', 1.4)]),
            (2, [('Roam', 2.2)]),
        ]

    def test_group_by2_overload2(self):
        en = Enumerable(TestGroupByMethod.pets_list)
        q = en.group_by2(lambda pet: math.floor(pet[1]))
        # simulate for loop
        it = iter(q)
        g1 = next(it)
        assert g1.key == 8
        assert g1.to_list() == [('Barley', 8.3), ('Roman', 8.6), ('Fangus', 8.6)]
        next(it); next(it); next(it)
        with pytest.raises(StopIteration):
            next(it)


class TestGroupJoinMethod:
    def test_group_join(self):
        class Person(NamedTuple):
            name: str
        class Pet(NamedTuple):
            name: str
            owner: Person
        magnus = Person('Hedlund, Magnus')
        terry = Person('Adams, Terry')
        charlotte = Person('Weiss, Charlotte')
        poor = Person('Animal, No')
        barley = Pet('Barley', owner=terry)
        boots = Pet('Boots', owner=terry)
        whiskers = Pet('Whiskers', owner=charlotte)
        daisy = Pet('Daisy', owner=magnus)
        roman = Pet('Roman', owner=terry)
        people = [magnus, terry, charlotte, poor]
        pets = [barley, boots, whiskers, daisy, roman]
        en = Enumerable(people)
        q = en.group_join(
            pets,
            lambda person: person,
            lambda pet: pet.owner,
            lambda person, pet_collection: (
                person.name,
                pet_collection.select(lambda pet: pet.name).to_list(),
            ),
        )
        assert q.to_list() == [
            ('Hedlund, Magnus', ['Daisy']),
            ('Adams, Terry', ['Barley', 'Boots', 'Roman']),
            ('Weiss, Charlotte', ['Whiskers']),
            ('Animal, No', []),  # empty match still shown
        ]

    def test_outer_same_key_twice(self):
        outer: List[Tuple[str, int]] = [
            ('Tim', 1234), ('Bob', 9865), ('Robert', 9865)
        ]
        inner: List[Tuple[int, int, int]] = [
            (98765, 1234, 9865), (34390, 9865, 19),
        ]
        en = Enumerable(outer)
        q = en.group_join(
            inner,
            lambda e: e[1],
            lambda e: e[1],
            lambda o, ic: (
                o[0],
                ic.select(lambda c: c[0]).to_list(),
                ic.select(lambda c: c[2]).to_list()
            ),
        )
        assert q.to_list() == [
            ('Tim', [98765], [9865]), ('Bob', [34390], [19]), ('Robert', [34390], [19]),
        ]

    def test_inner_empty(self):
        outer = [16, 17, 15]
        en = Enumerable(outer)
        q = en.group_join([], lambda e: e, lambda e: e, lambda o, ic: (o, ic.to_list()))
        assert q.to_list() == [(16, []), (17, []), (15, [])]


class TestIntersectMethod:
    def test_intersect(self):
        ints = [4, 88, 21, -5, 25, 12, 77, 77, 79, 77, 0, 0]
        en = Enumerable(ints)
        intersect = en.intersect([88, 34, 21, 66, 79, 77])
        assert intersect.to_list() == [88, 21, 77, 79]

    def test_unhashable(self):
        lsts = [[4], [88], [21], [-5], [25], [12], [77]]
        en = Enumerable(lsts)
        intersect = en.intersect([[88], [34], [21], [66], [77]])
        assert intersect.to_list() == [[88], [21], [77]]

    def test_showup_multiple(self):
        ints = [6, 6, 6, 6]
        en = Enumerable(ints)
        intersect = en.intersect([6, 6, 6])
        assert intersect.to_list() == [6]

    def test_keep_nothing(self):
        ints = [4, -5, 25, 12, 0]
        en = Enumerable(ints)
        intersect = en.intersect(Enumerable.empty().cast(int))
        assert intersect.to_list() == []


class TestJoinMethod:
    def test_join(self):
        class Person(NamedTuple):
            name: str
        class Pet(NamedTuple):
            name: str
            owner: Person
        magnus = Person('Hedlund, Magnus')
        terry = Person('Adams, Terry')
        charlotte = Person('Weiss, Charlotte')
        poor = Person('Animal, No')
        barley = Pet('Barley', owner=terry)
        boots = Pet('Boots', owner=terry)
        whiskers = Pet('Whiskers', owner=charlotte)
        daisy = Pet('Daisy', owner=magnus)
        roman = Pet('Roman', owner=terry)
        people = [magnus, terry, charlotte, poor]
        pets = [barley, boots, whiskers, daisy, roman]
        en = Enumerable(people)
        q = en.join(
            pets,
            lambda person: person,
            lambda pet: pet.owner,
            lambda person, pet: (person.name, pet.name),
        )
        assert q.to_list() == [
            ('Hedlund, Magnus', 'Daisy'),
            ('Adams, Terry', 'Barley'),
            ('Adams, Terry', 'Boots'),
            ('Adams, Terry', 'Roman'),
            ('Weiss, Charlotte', 'Whiskers'),
        ]

    def test_inner_empty(self):
        outer = [16, 17, 15]
        en = Enumerable(outer)
        q = en.join([], lambda e: e, lambda e: e, lambda o, ic: (o, ic.to_list()))
        assert q.to_list() == []


class TestLastMethod:
    def test_last_overload1_yes(self):
        lst = ('a', object(), 'b', 5, 'c')
        en = Enumerable(lst)
        assert en.last() == 'c'

    def test_last_overload1_no(self):
        with pytest.raises(InvalidOperationError):
            Enumerable({}).last()

    def test_last_overload2_yes(self):
        lst = ('a', 'b', 5, object(), 'c', 6, 'd')
        en = Enumerable(lst)
        assert en.last(lambda e: isinstance(e, int)) == 6

    def test_last_overload2_no(self):
        lst = ('a', 'b', 5, object(), 'c', 6, 'd')
        en = Enumerable(lst)
        with pytest.raises(InvalidOperationError):
            assert en.last(lambda e: isinstance(e, tuple))

    def test_last2_overload1_yes(self):
        lst = ('a', 'b', object(), 5, 'c')
        en = Enumerable(lst)
        assert en.last2(set) == 'c'

    def test_last2_overload1_no(self):
        assert Enumerable({}).last2(set) == set

    def test_last2_overload2_yes(self):
        lst = ('a', 'b', 5, object(), 'c', 6, 'd')
        en = Enumerable(lst)
        assert en.last2(lambda e: isinstance(e, int), 'A') == 6

    def test_last2_overload2_no(self):
        lst = ('a', 'b', 5, object(), 'c', 6, 'd')
        en = Enumerable(lst)
        assert en.last2(lambda e: isinstance(e, tuple), 'A') == 'A'


class TestMaxMethod:
    def test_max_overload1(self):
        nums = (1, 5, 2.2, 5, 1, 2)
        en = Enumerable(nums)
        assert en.max() == 5

    def test_max_overload1_empty(self):
        nums: List[int] = []
        en = Enumerable(nums)
        with pytest.raises(InvalidOperationError):
            en.max()

    def test_max_1(self):
        nums = [8]
        en = Enumerable(nums)
        assert en.max() == 8

    def test_max_first_one(self):
        nums = (100, 5, 2.2, 5, 1, 2, 2)
        en = Enumerable(nums)
        assert en.max() == 100

    def test_max_overload2(self):
        # ok. list objects have __lt__() so use another type.
        # hover mouse over 'max' to see that first overload is missing
        class MyType:
            def __init__(self, x: int): self.x = x
        lst = [MyType(2), MyType(7), MyType(-1), MyType(9), MyType(1)]
        en = Enumerable(lst)
        assert en.max(lambda x: x.x) == 9

    def test_max2_overload1(self):
        nums = (1, 5, 2.2, 5, 1, 2, 2)
        en = Enumerable(nums)
        assert en.max2(tuple) == 5

    def test_max2_overload1_empty(self):
        nums: List[int] = []
        en = Enumerable(nums)
        assert en.max2(tuple) == tuple

    def test_max2_overload2(self):
        lst = [[0], [1], [-9], [4], [4], [4]]
        en = Enumerable(lst)
        assert en.max2(lambda x: x[0], object) == 4


class TestMaxByMethod:
    def test_overload1(self):
        strings = ['aaa', 'bb', 'c', 'dddd']
        en = Enumerable(strings)
        assert en.max_by(len) == 'dddd'

    def test_overload1_empty(self):
        strings: List[str] = []
        en = Enumerable(strings)
        with pytest.raises(InvalidOperationError):
            en.max_by(len)

    def test_dup_choose_first(self):
        strings = ['foo', 'cheese', 'baz', 'spam', 'orange', 'string']
        en = Enumerable(strings)
        assert en.max_by(len) == 'cheese'

    def test_overload2(self):
        lst = [['foo'], ['cheese'], ['baz'], ['spam'], ['string']]
        en = Enumerable(lst)
        assert en.max_by(lambda x: x[0], lambda x, y: len(x) - len(y)) == ['cheese']


class TestMinMethod:
    def test_min_overload1(self):
        nums = (1, 0.4, 2.2, 5, 1, 2)
        en = Enumerable(nums)
        assert en.min() == 0.4

    def test_min_overload1_empty(self):
        nums: List[int] = []
        en = Enumerable(nums)
        with pytest.raises(InvalidOperationError):
            en.min()

    def test_min_1(self):
        nums = [8]
        en = Enumerable(nums)
        assert en.min() == 8

    def test_min_first_one(self):
        nums = (0.9, 5, 2.2, 5, 1, 2, 2)
        en = Enumerable(nums)
        assert en.min() == 0.9

    def test_min_overload2(self):
        class MyType:
            def __init__(self, x: int): self.x = x
        lst = [MyType(2), MyType(7), MyType(19), MyType(1), MyType(9)]
        en = Enumerable(lst)
        assert en.min(lambda x: x.x) == 1

    def test_min2_overload1(self):
        nums = (1, 0.4, 2.2, 5, 1, 2, 2)
        en = Enumerable(nums)
        assert en.min2(tuple) == 0.4

    def test_min2_overload1_empty(self):
        nums: List[int] = []
        en = Enumerable(nums)
        assert en.min2(tuple) == tuple

    def test_min2_overload2(self):
        lst = [[0], [1], [-9], [4], [4], [-11]]
        en = Enumerable(lst)
        assert en.min2(lambda x: x[0], object) == -11


class TestMinByMethod:
    def test_overload1(self):
        strings = ['aaa', 'bb', 'c', 'dddd']
        en = Enumerable(strings)
        assert en.min_by(len) == 'c'

    def test_overload1_empty(self):
        strings: List[str] = []
        en = Enumerable(strings)
        with pytest.raises(InvalidOperationError):
            en.min_by(len)

    def test_dup_choose_first(self):
        class MyType:
            def __init__(self, x: int): self.x = x
        lst = [MyType(2), MyType(7), MyType(19), MyType(1), MyType(7), MyType(1)]
        en = Enumerable(lst)
        assert en.min_by(lambda x: x.x) == lst[3]
        assert en.min_by(lambda x: x.x) != lst[-1]

    def test_overload2(self):
        lst = [['foo'], ['cheese'], ['baz'], ['spam'], ['string']]
        en = Enumerable(lst)
        assert en.min_by(lambda x: x[0], lambda x, y: len(x) - len(y)) == ['foo']


class TestOfTypeMethod:
    def test_of_type(self):
        lst = [1, 5, 4.4, object(), 5.6, -12.2, [], 2.2, False]
        en = Enumerable(lst)
        assert en.of_type(float).to_list() == [4.4, 5.6, -12.2, 2.2]

    def test_inheritance(self):
        class A: pass
        class B(A): pass
        lst = [A(), A(), B()]
        en = Enumerable(lst)
        assert en.of_type(A).count() == 3
        assert en.of_type(B).count() == 1


class TestOrderByMethod:
    class Pet(NamedTuple):
        name: str
        age: int

    def pets(self):
        yield self.Pet('Barley', 8)
        yield self.Pet('Boots', 4)
        yield self.Pet('Whiskers', 1)
        yield self.Pet('Daisy', 4)
        yield self.Pet('Roman', 5)

    def test_order_by_overload1(self):
        en = Enumerable(self.pets())
        q = en.order_by(lambda p: p.age)
        assert q.to_list() == [
            self.Pet('Whiskers', 1),
            self.Pet('Boots', 4),
            self.Pet('Daisy', 4),
            self.Pet('Roman', 5),
            self.Pet('Barley', 8),
        ]

    def test_order_by_overload2(self):
        en = Enumerable(self.pets())
        q = en.order_by(
            lambda p: (999, p.age, p.name),
            lambda t_lhs, t_rhs: t_lhs[1] - t_rhs[1],
        ).select(lambda p: p.name)
        assert q.to_list() == [
            'Whiskers', 'Boots', 'Daisy', 'Roman', 'Barley',
        ]

    def test_order_by_descending_overload1(self):
        en = Enumerable(self.pets())
        q = en.order_by_descending(lambda p: p.age)
        assert q.to_list() == [
            self.Pet('Barley', 8),
            self.Pet('Roman', 5),
            self.Pet('Boots', 4),
            self.Pet('Daisy', 4),
            self.Pet('Whiskers', 1),
        ]

    def test_order_by_descending_overload2(self):
        en = Enumerable(self.pets())
        q = en.order_by_descending(
            lambda p: (999, p.age, p.name),
            lambda t_lhs, t_rhs: t_lhs[1] - t_rhs[1],
        ).select(lambda p: p.name)
        assert q.to_list() == [
            'Barley', 'Roman', 'Boots', 'Daisy', 'Whiskers', 
        ]


class TestPrependMethod:
    def test_no_mutate(self):
        ints = [10]
        en = Enumerable(ints)
        en2 = en.prepend(7).prepend(8)
        assert ints == [10]
        assert en.to_list() == [10]
        assert en2.to_list() == [8, 7, 10]


class TestRangeMethod:
    def test_range(self):
        ints = Enumerable.range(0, 6)
        assert ints.to_list() == [0, 1, 2, 3, 4, 5]
        ints2 = Enumerable.range(1, 10).select(lambda x: x * x)
        assert ints2.to_list() == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

    def test_no_elem(self):
        ints = Enumerable.range(5, 0)
        assert ints.to_list() == []

    def test_1_elem(self):
        ints = Enumerable.range(9, 1)
        assert ints.to_list() == [9]

    def test_invalid(self):
        with pytest.raises(InvalidOperationError):
            Enumerable.range(99, -1)

    def test_no_end(self):
        ints = Enumerable.range(77, None)
        lst = ints.take(100).to_list()
        assert lst == [*range(77, 177)]


class TestRepeatMethod:
    def test_repeat(self):
        en = Enumerable.repeat('a', 5)
        assert en.to_list() == ['a'] * 5

    def test_no_elem(self):
        en = Enumerable.repeat('g', 0)
        assert en.to_list() == []

    def test_1_elem(self):
        en = Enumerable.repeat('x', 1)
        assert en.to_list() == ['x']

    def test_invalid(self):
        with pytest.raises(InvalidOperationError):
            Enumerable.repeat(99, -1)

    def test_no_end(self):
        hellos = Enumerable.repeat((), None).take(107)
        assert hellos.to_list() == [()] * 107


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
            lambda tup, i: [i] + tup[1],  # type: ignore
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


class TestSequenceEqualMethod:
    def test_overload1(self):
        lst = [['a'], ['x'], ['y'], [16], [17]]
        en1 = Enumerable(lst)
        en2 = Enumerable((['a'], ['x'], ['y'], [16], [17]))
        assert en1.sequence_equal(en2) is True
        assert en2.sequence_equal(en1) is True
        assert en2.sequence_equal(lst) is True

    def test_overload1_1_elem(self):
        en1 = Enumerable(['a'])
        en2 = Enumerable('a')
        assert en1.sequence_equal(en2)
        assert en2.sequence_equal(en1)

    def test_overload1_both_empty(self):
        assert Enumerable.empty().sequence_equal([]) is True

    def test_overload1_one_empty(self):
        en1 = Enumerable.empty().cast(str)
        en2 = Enumerable(['a', 'x'])
        assert en1.sequence_equal(en2) is False
        assert en2.sequence_equal(en1) is False

    def test_overload1_one_more(self):
        en1 = Enumerable(['a', 'x', 'y'])
        en2 = Enumerable(['a', 'x', 'y', 't'])
        assert en1.sequence_equal(en2) is False
        assert en2.sequence_equal(en1) is False

    def test_overload1_first_off(self):
        en1 = Enumerable(['a', 'x', 'y'])
        en2 = Enumerable(['b', 'x', 'y'])
        assert en1.sequence_equal(en2) is False
        assert en2.sequence_equal(en1) is False

    def test_overload1_last_off(self):
        en1 = Enumerable(['a', 'x', 'y'])
        en2 = Enumerable(['a', 'x', 'z'])
        assert en1.sequence_equal(en2) is False
        assert en2.sequence_equal(en1) is False

    def test_overload1_middle_off(self):
        en1 = Enumerable(['a', 'x', 'y', 'z', 'u'])
        en2 = Enumerable(['b', 'x', 'k', 'z', 'u'])
        assert en1.sequence_equal(en2) is False
        assert en2.sequence_equal(en1) is False

    def test_overload2_yes(self):
        ints = [1, 3, 5, 7, 9]
        en = Enumerable(ints)
        strs = ['1', '3', '5', '7', '9']
        assert en.sequence_equal(strs, lambda x, y: str(x) == y) is True

    def test_overload2_no(self):
        ints = [1, 3, 5, 7, 9]
        en = Enumerable(ints)
        strs = ['1', '3', '5', '7', 'z']
        assert en.sequence_equal(strs, lambda x, y: str(x) == y) is False


class TestSingleMethod:
    def test_single_overload1_yes(self):
        en = Enumerable([7])
        assert en.single() == 7

    def test_single_overload1_more(self):
        en = Enumerable([7, 8])
        with pytest.raises(InvalidOperationError):
            en.single()

    def test_single_overload1_empty(self):
        en = Enumerable(())
        with pytest.raises(InvalidOperationError):
            en.single()

    def test_single_overload2_at_first(self):
        ints = [1, 4, 6, 9, 10]
        en = Enumerable(ints)
        assert en.single(lambda x: x == 1) == 1

    def test_single_overload2_at_back(self):
        ints = [1, 4, 6, 9, 10]
        en = Enumerable(ints)
        assert en.single(lambda x: x == 10) == 10

    def test_single_overload2_middle(self):
        ints = [1, 4, 6, 9, 10]
        en = Enumerable(ints)
        assert en.single(lambda x: x == 6) == 6

    def test_single_overload2_dup(self):
        ints = [1, 4, 6, 9, 10]
        en = Enumerable(ints)
        with pytest.raises(InvalidOperationError):
            en.single(lambda x: x == 4 or x == 6)

    def test_single_overload2_dup_non_adjacent(self):
        ints = [1, 4, 6, 9, 10]
        en = Enumerable(ints)
        with pytest.raises(InvalidOperationError):
            en.single(lambda x: x == 4 or x == 10)

    def test_single_overload2_no(self):
        ints = [1, 4, 6, 9, 10]
        en = Enumerable(ints)
        with pytest.raises(InvalidOperationError):
            en.single(lambda x: x == 100)

    def test_single_overload2_empty(self):
        en = Enumerable(())
        with pytest.raises(InvalidOperationError):
            en.single(lambda x: x == 7)

    def test_single2_overload1_yes(self):
        en = Enumerable([7])
        assert en.single2(tuple) == 7

    def test_single2_overload1_more(self):
        en = Enumerable([7, 8])
        with pytest.raises(InvalidOperationError):
            en.single2(tuple)

    def test_single2_overload1_empty(self):
        en = Enumerable(())
        assert en.single2(tuple) == tuple

    def test_single2_overload2_yes(self):
        ints = [1, 4, 6, 9, 10]
        en = Enumerable(ints)
        assert en.single2(lambda x: x == 6, list) == 6

    def test_single2_overload2_dup(self):
        ints = [1, 4, 6, 9, 10]
        en = Enumerable(ints)
        with pytest.raises(InvalidOperationError):
            en.single2(lambda x: x == 4 or x == 6, list)

    def test_single2_overload2_no(self):
        ints = [1, 4, 6, 9, 10]
        en = Enumerable(ints)
        assert en.single2(lambda x: x == 100, list) == list

    def test_single2_overload2_empty(self):
        en = Enumerable(())
        assert en.single2(lambda x: x == 7, list) == list


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


class TestSkipLastMethod:
    def test_some(self):
        gen_func = lambda: (i for i in range(1, 8))
        en = Enumerable(gen_func)
        assert en.skip_last(1).to_list() == [1, 2, 3, 4, 5, 6]
        assert en.skip_last(3).to_list() == [1, 2, 3, 4]

    def test_all_skipped(self):
        gen = (i for i in range(1, 8))
        en = Enumerable(gen)
        assert en.skip_last(7).to_list() == []
        assert en.skip_last(8).to_list() == []

    def test_count_zero_or_negative(self):
        lst = [1, 2, 3]
        en = Enumerable(lst)
        assert en.skip_last(0).to_list() == lst
        assert en.skip_last(-1).to_list() == lst

    def test_enumerate(self):
        'test no more than count items are ever evaluated a head of current position'
        stored = []
        def gen_func():
            for i in range(6):
                stored.append(i)
                yield i
        en = Enumerable(gen_func()).skip_last(3)
        count = 0
        # if all elements were enumerated at once inside the skip_last(), then stored would be filled
        # at once, not like this
        for elem in en:
            assert elem == count
            assert stored == [0, 1, 2, *range(3, 3 + count + 1)]
            count += 1


class TestSkipWhileMethod:
    def test_skip_while_some(self):
        lst = [1, 1, 1, 1, 2, 3, 6, 7, 1]
        en = Enumerable(lst)
        assert en.skip_while(lambda x: x <= 2).to_list() == [3, 6, 7, 1]

    def test_skip_while_none(self):
        lst = [1, 1, 1, 1, 2, 3, 6, 7, 1]
        en = Enumerable(lst)
        assert en.skip_while(lambda x: x == 20).to_list() == lst

    def test_skip_while_all(self):
        lst = [1, 1, 1, 1, 2, 3, 6, 7, 1]
        en = Enumerable(lst)
        assert en.skip_while(lambda x: x < 20).to_list() == []

    def test_skip_while_empty(self):
        en = Enumerable([])
        assert en.skip_while(lambda x: x == 9).to_list() == []

    def test_skip_while2_some(self):
        # coverage py (5.4.1 with C) failed to identify code as covered in this test
        lst = [1, 1, 1, 1, 2, 3, 6, 7, 1]
        en = Enumerable(lst)
        q = en.skip_while2(lambda x, i: x <= 2 and i < 4)
        assert q.to_list() == [2, 3, 6, 7, 1]
        # equivalent:
        # q = en.zip(en.range(0, None)) \
        #     .skip_while(lambda t: t[0] <= 2 and t[1] < 4) \
        #     .select(lambda t: t[0])

    def test_skip_while2_none(self):
        lst = [1, 1, 1, 1, 2, 3, 6, 7, 1]
        en = Enumerable(lst)
        q = en.skip_while2(lambda x, i: x <= 2 and i > 40)
        assert q.to_list() == lst

    def test_skip_while2_all(self):
        lst = [1, 1, 1, 1, 2, 3, 6, 7, 1]
        en = Enumerable(lst)
        q = en.skip_while2(lambda x, i: x < 20 and i < 40)
        assert q.to_list() == []


class TestSumMethod:
    def test_sum_overload1(self):
        floats = [.1, .3, .5, .9, 1.1]
        s = Enumerable(floats).sum()
        assert s > 2.9 - 1e3 and s < 2.9 + 1e3

    def test_sum_overload1_1(self):
        ints = [44]
        s = Enumerable(ints).sum()
        assert s == 44

    def test_sum_overload1_empty(self):
        ints: List[float] = []
        s = Enumerable(ints).sum()
        assert s == 0

    def test_sum_overload2(self):
        lst = [[1], [3], [5], [9], [11]]
        en = Enumerable(lst)
        s = en.sum(lambda e: e[0])
        assert s == 29

    def test_sum2_overload1(self):
        ints = [1, 3, 5, 9, 11]
        s = Enumerable(ints).sum2(33)
        assert s == 29

    def test_sum2_overload1_empty(self):
        ints: List[int] = []
        s = Enumerable(ints).sum2(880)
        assert s == 880

    def test_sum2_overload2(self):
        lst = [[1], [3], [5], [9], [11]]
        en = Enumerable(lst)
        s = en.sum2(lambda e: e[0], -2)
        assert s == 29


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


class TestTakeLastMethod:
    def test_some(self):
        gen_func = lambda: (i for i in range(7))
        en = Enumerable(gen_func)
        assert en.take_last(1).to_list() == [6]
        assert en.take_last(2).to_list() == [5, 6]
        assert en.take_last(4).to_list() == [3, 4, 5, 6]

    def test_take_all(self):
        gen_func = lambda: (i for i in range(7))
        en = Enumerable(gen_func)
        assert en.take_last(7).to_list() == list(gen_func())
        assert en.take_last(8).to_list() == list(gen_func())

    def test_1_elem(self):
        en = Enumerable([5])
        assert en.take_last(1).to_list() == [5]
        assert en.take_last(2).to_list() == [5]

    def test_empty(self):
        en = Enumerable(())
        assert en.take_last(1).to_list() == []
        assert en.take_last(2).to_list() == []

    def test_count_zero_or_negative(self):
        lst = [1, 2, 3]
        en = Enumerable(lst)
        assert en.take_last(0).to_list() == []
        assert en.take_last(-1).to_list() == []


class TestTakeWhileMethod:
    def test_take_while_some(self):
        lst = ['1', '3', '5', '7', '', '1', '4', '5']
        en = Enumerable(lst)
        q = en.take_while(lambda x: x != '')
        assert q.to_list() == ['1', '3', '5', '7']

    def test_take_while_all(self):
        lst = ['1', '3', '5', '7', '', '1', '4', '5']
        en = Enumerable(lst)
        q = en.take_while(lambda x: x != '77')
        assert q.to_list() == lst

    def test_take_while_nothing(self):
        lst = ['1', '3', '5', '7', '', '1', '4', '5']
        en = Enumerable(lst)
        q = en.take_while(lambda x: not isinstance(x, str))
        assert q.to_list() == []

    def test_take_while2_some(self):
        lst = ['1', '3', '5', '7', '', '1', '4', '5']
        en = Enumerable(lst)
        q = en.take_while2(lambda x, i: isinstance(x, str) and i < 4)
        assert q.to_list() == ['1', '3', '5', '7']

    def test_take_while2_all(self):
        lst = ['1', '3', '5', '7', '', '1', '4', '5']
        en = Enumerable(lst)
        q = en.take_while2(lambda x, i: isinstance(x, str) and i < 8)
        assert q.to_list() == lst


class TestUnionMethod:
    def test_union(self):
        gen = (i for i in range(5))
        en = Enumerable(gen)
        q = en.union([15, 16, 17, 15, 18])
        assert q.to_list() == [0, 1, 2, 3, 4, 15, 16, 17, 18]

    def test_unhashable(self):
        gen = ([i, i] for i in range(5))
        en = Enumerable(gen)
        q = en.union([[15, 15], [16, 16], [17, 17], [15, 15], [18, 18]])
        assert q.to_list() == [
            [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [15, 15], [16, 16], [17, 17], [18, 18]
        ]

    def test_dedup(self):
        lst = [1, 2, 2, 7, -1, 8, -1]
        en = Enumerable(lst)
        q = en.union([])
        assert q.to_list() == [1, 2, 7, -1, 8]


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


class TestThenByMethod:
    par = TestOrderByMethod()

    def more_pets(self):
        yield from self.par.pets()
        yield self.par.Pet('Alfa', 4)
        yield self.par.Pet('Bowah', 8)

    def test_then_by_overload1(self):
        en = Enumerable(self.more_pets())
        q = en.order_by(lambda p: p.age) \
            .then_by(lambda p: p.name) \
            .select(lambda p: p.name)
        assert q.to_list() == [
            'Whiskers', 'Alfa', 'Boots', 'Daisy', 'Roman', 'Barley', 'Bowah'
        ]

    def test_then_by_overload2(self):
        en = Enumerable(self.more_pets())
        q = en.order_by(lambda p: p.age) \
            .then_by(
                lambda p: (999, 444, p[0]),
                lambda t_lhs, t_rhs: -1 if t_lhs[2] < t_rhs[2] else 0,
            ).select(lambda p: p.name)
        assert q.to_list() == [
            'Whiskers', 'Alfa', 'Boots', 'Daisy', 'Roman', 'Barley', 'Bowah'
        ]

    def test_then_by_descending_overload1(self):
        en = Enumerable(self.more_pets())
        q = en.order_by(lambda p: p.age) \
            .then_by_descending(lambda p: p.name)
        assert q.to_list() == [
            self.par.Pet('Whiskers', 1),
            self.par.Pet('Daisy', 4),
            self.par.Pet('Boots', 4),
            self.par.Pet('Alfa', 4),
            self.par.Pet('Roman', 5),
            self.par.Pet('Bowah', 8),
            self.par.Pet('Barley', 8),
        ]

    def test_then_by_descending_overload2(self):
        en = Enumerable(self.more_pets())
        q = en.order_by(lambda p: p.age) \
            .then_by_descending(
                lambda p: (999, 444, p[0]),
                lambda t_lhs, t_rhs: -1 if t_lhs[2] < t_rhs[2] else 0,
            )
        assert q.to_list() == [
            self.par.Pet('Whiskers', 1),
            self.par.Pet('Daisy', 4),
            self.par.Pet('Boots', 4),
            self.par.Pet('Alfa', 4),
            self.par.Pet('Roman', 5),
            self.par.Pet('Bowah', 8),
            self.par.Pet('Barley', 8),
        ]

    def test_delayed(self):
        def gen_func():
            yield 1, 2, 3, 4
            yield 9, 2, 3, 3
            yield 9, 2, 3, 4
            yield 1, 2, 2, 2
            yield 2, 3, 4, 7
            yield 9, 3, 2, 1
            yield 4, 5, 8, 0
            yield 9, 3, 3, 3
        gen = gen_func()
        en = Enumerable(gen)
        q = en.order_by(lambda t: t[0]) \
            .then_by(lambda t: t[1]) \
            .then_by(lambda t: t[2]) \
            .then_by(lambda t: t[3])
        assert gen.gi_frame is not None
        assert q.to_list() == [
            (1, 2, 2, 2), (1, 2, 3, 4), (2, 3, 4, 7), (4, 5, 8, 0),
            (9, 2, 3, 3), (9, 2, 3, 4), (9, 3, 2, 1), (9, 3, 3, 3),
        ]


class TestToLookupMethod:
    food: List[Tuple[str, str]] = [
        ('main', 'ramen'), ('main', 'noodles'), ('side', 'chicken'),
        ('main', 'spaghetti'), ('snack', 'popcorns'), ('side', 'apples'),
        ('side', 'orange'), ('drink', 'coke'), ('main', 'birthdaycake'),
    ]

    def test_overload1_and_basic_lookup_usage(self):
        en = Enumerable(self.food)
        lookup = en.to_lookup(lambda e: e[0], lambda e: e[1])
        assert lookup.count == 4
        assert lookup.contains('side') and not lookup.contains('ramen')
        assert lookup['main'].to_list() == [
            'ramen', 'noodles', 'spaghetti', 'birthdaycake'
        ]
        assert lookup['side'].to_list() == ['chicken', 'apples', 'orange']
        assert lookup['snack'].to_list() == ['popcorns']
        assert lookup['drink'].to_list() == ['coke']
        assert lookup['wtf'].to_list() == []

    def test_unhashable(self):
        en = Enumerable(([v0], v1) for v0, v1 in self.food)
        lookup = en.to_lookup(lambda e: e[0], lambda e: e[1])
        assert lookup.count == 4
        assert lookup[['side']].to_list() == ['chicken', 'apples', 'orange']

    def test_id(self):
        flat1 = Enumerable(self.food) \
            .to_lookup(lambda e: e[0], lambda e: e[1]) \
            .select_many(lambda e: e.to_list()) \
            .to_set()
        target = Enumerable(self.food).select(lambda e: e[1]).to_set()
        assert flat1 == target

    def test_overload2(self):
        en = Enumerable(self.food)
        lookup = en.to_lookup(lambda e: e[0])
        assert lookup['snack'].to_list() == [('snack', 'popcorns')]

    def test_empty(self):
        assert Enumerable.empty().to_lookup(lambda e: e).count == 0


class TestZipMethod:
    def test_zip(self):
        lst = [1, 2, 3, 4]
        other_lst = ['x', 'y', 'z', 't']
        en = Enumerable(lst)
        zipped = en.zip(Enumerable(other_lst))
        assert zipped.to_list() == [(1, 'x'), (2, 'y'), (3, 'z'), (4, 't')]
        zipped2 = en.zip(other_lst, lst)
        assert zipped2.to_list() == [
            (1, 'x', 1), (2, 'y', 2), (3, 'z', 3), (4, 't', 4),
        ]

    def test_zip2(self):
        lst = [1, 2, 3, 4]
        other_lst = ['x', 'y', 'z', 't']
        en = Enumerable(lst)
        zipped = en.zip2(other_lst, lambda x, y: f'{x}{y}')
        assert zipped.to_list() == ['1x', '2y', '3z', '4t']
        zipped2 = en.zip2(other_lst, lst, lambda x, y, z: f'{x}{y}{z}')
        assert zipped2.to_list() == ['1x1', '2y2', '3z3', '4t4']

    def test_zip_different_len(self):
        'take shorter'
        lst = [1, 2, 3, 4]
        other_lst = ['x', 'y', 'z', 't']
        en = Enumerable(lst).append(5)
        zipped = en.zip(Enumerable(other_lst).append('u').append('v'))
        assert zipped.to_list() == [(1, 'x'), (2, 'y'), (3, 'z'), (4, 't'), (5, 'u')]


class TestElementsInMethod:
    def test_overload1(self):
        lst = [0, 1, 2, 3, 4, 5, 6, 7]
        en = Enumerable(lst)
        sub = en.elements_in(slice(1, 6, 2))
        assert sub.to_list() == [1, 3, 5]

    def test_overload2_default(self):
        lst = [0, 1, 2, 3, 4, 5, 6, 7]
        en = Enumerable(lst)
        sub = en.elements_in(1, 6)
        assert sub.to_list() == [1, 2, 3, 4, 5]

    def test_overload2_full(self):
        lst = [0, 1, 2, 3, 4, 5, 6, 7]
        en = Enumerable(lst)
        sub = en.elements_in(1, 6, 2)
        assert sub.to_list() == [1, 3, 5]

    def test_no_arg(self):
        gen = lambda: (i for i in range(5))
        q = Enumerable(gen).elements_in(slice(None))
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
        q = Enumerable(gen).elements_in(slicing)
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
        (slice(2, 7, -1), []),
        (slice(2, 2, -1), []),
        (slice(0, 7, -2), []),
    ])
    def test_within_inf_generator(self, slicing: slice, expected: List[int]):
        def gen():
            i = 0
            while True:
                yield i
                i += 1
        q = Enumerable(gen).elements_in(slicing)
        assert q.to_list() == expected

    @pytest.mark.parametrize('slicing,expected', [
        (slice(None, 15, 1), [*range(30)][:15:1]),
        (slice(None, 15, 2), [*range(30)][:15:2]),
        (slice(None, 15, 3), [*range(30)][:15:3]),
        (slice(None, 15, -1), [*range(30)][:15:-1]),
        (slice(None, 15, -2), [*range(30)][:15:-2]),
        (slice(None, 15, -3), [*range(30)][:15:-3]),
        (slice(None, -15, -1), [*range(30)][:-15:-1]),
        (slice(None, -15, -2), [*range(30)][:-15:-2]),
    ])
    def test_missing_start(self, slicing: slice, expected: List[int]):
        gen = lambda: (i for i in range(30))
        q = Enumerable(gen).elements_in(slicing)
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
        q = Enumerable(gen).elements_in(slicing)
        assert q.to_list() == expected

    @pytest.mark.parametrize('slicing,expected', [
        (slice(-3, 23, -1),[*range(30)][-3:23:-1]),
        (slice(23, -23, 1), [*range(30)][23:-23:1]),
    ])
    def test_negative_idx(self, slicing: slice, expected: List[int]):
        gen = lambda: (i for i in range(30))
        q = Enumerable(gen).elements_in(slicing)
        assert q.to_list() == expected

    def test_fallback(self):
        en = Enumerable(TestElementAtMethod.OnlyHasGetItem(['x']))
        assert en[:7].to_list() == ['h', 'a', 'h', 'a']
        assert en.elements_in(slice(7)).to_list() == ['x']
        en2 = Enumerable(BasicIterable(['x']))
        assert en2[:7].to_list() == ['x']
        assert en2.elements_in(slice(7)).to_list() == ['x']
        en3 = Enumerable(self.OnlyHasGetItemRaises([]))
        with pytest.raises(IndexOutOfRangeError):
            en3[:7]

    class OnlyHasGetItemRaises(TestElementAtMethod.OnlyHasGetItem[TSource_co]):
        def __getitem__(self, _):  # type: ignore[override]
            raise IndexError('generic error')
