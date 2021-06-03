from collections.abc import Container, Iterable, Reversible, Sequence, Sized

import pytest

from types_linq import Enumerable, InvalidOperationError
from types_linq.util import ComposeSet, ComposeMap

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



class TestComposeMapAandSet:
    def __set_equal(self, iter1, iter2) -> bool:
        lst1 = [*iter1]
        lst2 = [*iter2]
        if len(lst1) != len(lst2):
            return False
        for e in iter1:
            if e not in lst2:
                return False
            lst2.remove(e)
        return len(lst2) == 0

    
    def test_set(self):
        set = ComposeSet([[1, 2, 4], (5, 6), 7, [], [9]])
        assert len(set) == 5
        assert self.__set_equal(set, [[1, 2, 4], (5, 6), 7, [], [9]])
        
        # add element
        set.add((5, 6))
        assert self.__set_equal(set, [[1, 2, 4], (5, 6), 7, [], [9]])
        set.add([1, 2, 4])
        assert self.__set_equal(set, [[1, 2, 4], (5, 6), 7, [], [9]])
        set.add([10, 11])
        assert self.__set_equal(set, [[1, 2, 4], (5, 6), 7, [], [9], [10, 11]])

        # remove element
        set.discard([1, 2, 4])
        set.discard(7)
        assert self.__set_equal(set, [(5, 6), [], [9], [10, 11]])

        # remove non-exist element
        # discard shouldn't throw KeyError
        set.discard([1, 2, 4])
        with pytest.raises(KeyError):
            set.remove([1, 2, 4])
        

    def test_map(self):
        map = ComposeMap([([1, 2, 4], 1), ((4, 6), 3), ([], 3)])
        assert self.__set_equal(map, [[1, 2, 4], (4, 6), []])
        assert self.__set_equal(map.items(), [([1, 2, 4], 1), ((4, 6), 3), ([], 3)])
        
        # modify map values
        map[[1, 2, 4]] = 3
        assert map[[1, 2, 4]] == 3
        map[(4, 6)] = 1
        assert map[(4, 6)] == 1
        
        # delete element
        del map[[]]
        assert [] not in map
        del map[(4, 6)]
        assert (4, 6) not in map
        with pytest.raises(KeyError):
            del map[[]]
        assert self.__set_equal(map.items(), [([1, 2, 4], 3)])
