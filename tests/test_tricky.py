import sys, os


sys.path = [os.path.abspath('..')]  # run in tests folder
sys.path.append(os.path.abspath('.'))  # run in root folder
from types_linq import Enumerable


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
