from types_linq import Enumerable, MoreEnumerable


class TestAsMore:
    def test_ret_type(self):
        en = Enumerable([1, 2]).as_more()
        assert isinstance(en, MoreEnumerable)
        assert en.to_list() == [1, 2]
