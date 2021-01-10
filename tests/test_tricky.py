import sys, os
from collections.abc import Container, Iterable, Reversible, Sequence, Sized


sys.path = [os.path.abspath('..')]  # run in tests folder
sys.path.append(os.path.abspath('.'))  # run in root folder
from types_linq import Enumerable


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
        def gen():
            i = 0
            while True:
                yield i
                i += 1
        en = Enumerable(gen()).select(lambda i: i * 2)
        assert en.take(2).to_list() == [0, 2]
        assert en.take(3).to_list() == [4, 6, 8]
        en2 = Enumerable(gen).select(lambda i: i * 2)
        assert en2.take(2).to_list() == [0, 2]
        assert en2.take(2).to_list() == [0, 2]
