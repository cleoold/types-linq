from collections.abc import Container, Iterable, Reversible, Sequence, Sized

import pytest

from types_linq import Enumerable


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


class TestConfigureRepeatableMethod:
    def test_enumerate_same_generator(self):
        gen = (i for i in range(6))
        en = Enumerable(gen).configure_repeatable()
        assert en.to_list() == [0, 1, 2, 3, 4, 5]
        assert en.count() == 6
        assert en.to_list() == [0, 1, 2, 3, 4, 5]

    def test_generator_empty(self):
        gen = (i for i in range(0))
        en = Enumerable(gen).configure_repeatable()
        assert en.to_list() == []
        assert en.to_list() == []

    def test_multiple_query_race(self):
        en = Enumerable(naturals()).configure_repeatable()
        assert en.take(1).to_list() == [0]
        assert en.take(1).to_list() == [0]
        assert en.take(3).to_list() == [0, 1, 2]
        assert en.take(1).to_list() == [0]
        assert en.take(3).to_list() == [0, 1, 2]
        assert en.take(5).to_list() == [0, 1, 2, 3, 4]
        assert en.take(7).to_list() == [0, 1, 2, 3, 4, 5, 6]
        assert en.take(2).to_list() == [0, 1]

    def test_dont_configure_twice(self):
        gen = (i for i in range(0))
        en = Enumerable(gen).configure_repeatable()
        with pytest.raises(TypeError):
            en.configure_repeatable()
