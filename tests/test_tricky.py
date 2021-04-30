from collections.abc import Container, Iterable, Reversible, Sequence, Sized

import pytest

from types_linq import Enumerable, InvalidOperationError


def naturals():
    i = 0
    while True:
        yield i
        i += 1


class TestAbc:
    def test_abc(self):
        en = Enumerable([])
        assert isinstance(en, Container)
        assert isinstance(en, Sequence)
        assert isinstance(en, Iterable)
        assert isinstance(en, Reversible)
        assert isinstance(en, Sized)

class TestIterMethod:
    def test_nest_generator(self):
        gen = (chr(i) for i in range(120, 123))
        en = Enumerable(Enumerable(gen))
        assert en.to_list() == ['x', 'y', 'z']


class TestInfinite:
    def test_take(self):
        en = Enumerable(naturals()).select(lambda i: i * 2)
        assert en.take(2).to_list() == [0, 2]
        assert en.take(3).to_list() == [4, 6, 8]
        en2 = Enumerable(naturals).select(lambda i: i * 2)
        assert en2.take(2).to_list() == [0, 2]
        assert en2.take(2).to_list() == [0, 2]


class TestAsCachedMethod:
    def test_enumerate_same_generator(self):
        gen = (i for i in range(6))
        en = Enumerable(gen).as_cached()
        assert en.to_list() == [0, 1, 2, 3, 4, 5]
        assert en.count() == 6
        assert en.to_list() == [0, 1, 2, 3, 4, 5]

    def test_generator_empty(self):
        gen = (i for i in range(0))
        en = Enumerable(gen).as_cached()
        assert en.to_list() == []
        assert en.to_list() == []

    def test_multiple_query_race(self):
        en = Enumerable(naturals()).as_cached()
        assert en.take(1).to_list() == [0]
        assert en.take(1).to_list() == [0]
        assert en.take(3).to_list() == [0, 1, 2]
        assert en.take(1).to_list() == [0]
        assert en.take(3).to_list() == [0, 1, 2]
        assert en.take(5).to_list() == [0, 1, 2, 3, 4]
        assert en.take(7).to_list() == [0, 1, 2, 3, 4, 5, 6]
        assert en.take(2).to_list() == [0, 1]

    def test_have_capacity(self):
        en = Enumerable(naturals()).as_cached(cache_capacity=100)
        assert en.take(100).to_list() == [*range(100)]
        assert en.take(100).to_list() == [*range(100)]
        assert en.take(101).to_list() == [*range(101)]
        assert en.take(100).to_list() == [*range(1, 101)]
        assert en.take(50).to_list() == [*range(1, 51)]
        assert en.take(102).to_list() == [*range(1, 103)]
        assert en.take(102).to_list() == [*range(3, 105)]
        assert en.take(0).to_list() == []
        assert en.take(110).to_list() == [*range(5, 115)]
        assert en.take(100).to_list() == [*range(15, 115)]

    def test_zero_capacity(self):
        en = Enumerable(naturals()).as_cached(cache_capacity=0)
        assert en.take(1).to_list() == [0]
        assert en.take(2).to_list() == [1, 2]

    def test_one_capacity(self):
        en = Enumerable(naturals()).as_cached(cache_capacity=1)
        assert en.take(1).to_list() == [0]
        assert en.take(3).to_list() == [0, 1, 2]
        assert en.take(3).to_list() == [2, 3, 4]
        assert en.take(1).to_list() == [4]
        assert en.take(2).to_list() == [4, 5]

    def test_capcity_grow_from_zero(self):
        en = Enumerable(naturals()).as_cached(cache_capacity=0)
        en.take(3).to_list()
        en.as_cached(cache_capacity=1)
        en.take(1).to_list() == [3]
        en.take(2).to_list() == [3, 4]

    def test_capacity_grow_from_one(self):
        en = Enumerable(naturals()).as_cached(cache_capacity=1)
        en.take(10).to_list()
        en.as_cached(cache_capacity=5)
        assert en.take(10).to_list() == [*range(9, 19)]
        assert en.take(10).to_list() == [*range(14, 24)]

    def test_capacity_grow_to_inf(self):
        en = Enumerable(naturals()).as_cached(cache_capacity=5)
        en.take(10).to_list()
        en.as_cached(cache_capacity=None)
        en.take(10).to_list()
        en.take(10).to_list()
        assert en.take(15).to_list() == [*range(5, 20)]

    def test_capacity_shrink(self):
        en = Enumerable(naturals()).as_cached(cache_capacity=10)
        en.take(10).to_list()
        en.as_cached(cache_capacity=9)
        assert en.take(10).to_list() == [*range(1, 11)]
        en.as_cached(cache_capacity=5)
        assert en.take(10).to_list() == [*range(6, 16)]

    def test_capacity_shrink_to_zero(self):
        en = Enumerable(naturals()).as_cached(cache_capacity=10)
        en.take(10).to_list()
        en.as_cached(cache_capacity=0)
        assert en.take(10).to_list() == [*range(10, 20)]

    def test_capacity_shrink_no_delete(self):
        en = Enumerable(naturals()).as_cached(cache_capacity=10)
        en.take(5).to_list()
        en.as_cached(cache_capacity=6)
        assert en.take(6).to_list() == [*range(0, 6)]
        en.take(7).to_list()
        assert en.take(6).to_list() == [*range(1, 7)]

    def test_errors(self):
        gen = (i for i in range(0))
        en = Enumerable(gen).as_cached()
        with pytest.raises(InvalidOperationError):
            en.as_cached(cache_capacity=-1)
        en2 = Enumerable(gen)
        with pytest.raises(InvalidOperationError):
            en2.as_cached(cache_capacity=-1)


class TestOrderedByThenIter:
    def test_orderby_index(self):
        en = Enumerable([1, 3, 2]).order_by(lambda x: x)
        assert en.element_at(1) == en[1] == 2
        assert en.element_at(2) == en[2] == 3

    def test_as_cached_then_orderby(self):
        en = Enumerable(naturals()).take(5).as_cached()
        en.take(3).to_list()
        assert en.order_by(lambda x: x).to_list() == [*range(5)]
