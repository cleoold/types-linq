from __future__ import annotations
from typing import Any, Callable, Container, Deque, Dict, Iterable, Iterator, List, NoReturn, Optional, Reversible, Sequence, Set, Sized, TYPE_CHECKING, Tuple, Type, Generic, Union

if TYPE_CHECKING:
    from .lookup import Lookup
    from .grouping import Grouping
    from .ordered_enumerable import OrderedEnumerable
    from .cached_enumerable import CachedEnumerable
    from .more import MoreEnumerable

from .types_linq_error import InvalidOperationError, IndexOutOfRangeError
from .util import ComposeSet
from .more_typing import (
    TCollection,
    TDefault,
    TInner,
    TKey,
    TResult,
    TSource_co,
    TValue,
)


# do not use this value!!!
_signal: Any = object()


class Enumerable(Sequence[TSource_co], Generic[TSource_co]):

    _iter_factory: Callable[[], Iterable[TSource_co]]

    def __init__(self,
        it: Union[Iterable[TSource_co], Callable[[], Iterable[TSource_co]]]
    ):
        if isinstance(it, Iterable):
            self._iter_factory = lambda it_=it: it_
        else:
            self._iter_factory = lambda it_=it: it_()

    def _get_iterable(self) -> Iterable[TSource_co]:
        return self._iter_factory()

    # 'fallback = F' -> calls dunder methods if available
    #                  -> otherwise calls own implementation
    # 'fallback = T'-> calls own implementation
    def _contains_impl(self, value: object, fallback: bool) -> bool:
        iterable = self._get_iterable()
        if not fallback and isinstance(iterable, Container):
            return value in iterable  # type: ignore
        for elem in iterable:
            if elem == value:
                return True
        return False

    def __contains__(self, value: object) -> bool:
        return self._contains_impl(value, fallback=False)

    def _every(self, step: int) -> Enumerable[TSource_co]:
        return self.where2(lambda _, i: i % step == 0)

    def _getitem_impl(self,
        index: Union[int, slice],
        fallback: bool,
    ) -> Union[TSource_co, Enumerable[TSource_co]]:
        iterable = self._get_iterable()
        if isinstance(index, int):
            # Sequence is an abstract base class without @runtime_checkable
            if not fallback and isinstance(iterable, Sequence):
                # an appropriate implementation should raise IndexError, or IndexOutOfRangeError
                try:
                    return iterable[index]
                except IndexError as e:
                    raise IndexOutOfRangeError from e
            iterator = iter(iterable)
            try:
                for _ in range(index):
                    next(iterator)
                return next(iterator)
            except StopIteration:
                raise IndexOutOfRangeError('Not enough elements in the sequence')

        else:  # isinstance(index, slice)
            if not fallback and isinstance(iterable, Sequence):
                try:
                    res = iterable[index]
                except IndexError as e:
                    raise IndexOutOfRangeError(e)
                return res if isinstance(res, Enumerable) else Enumerable(res)
            # we do not enumerate all values if the begin and the end only involve
            # nonnegative indices since in which case the sliced part can be obtained
            # without reversing.
            # otherwise have to enumerate all with using list's slice operator.
            # (don't enumerate right away in this function, of course)
            def inner(s: slice = index):
                en = iterable if isinstance(iterable, Enumerable) else Enumerable(iterable)
                start_is_none = s.start is None
                stop_is_none = s.stop is None
                step = s.step if s.step is not None else 1
                if (start_is_none and stop_is_none) or (not start_is_none and s.start < 0) \
                    or (not stop_is_none and s.stop < 0) or (stop_is_none):
                    yield from en.to_list()[s]
                    return
                elif start_is_none:
                    if step > 0:
                        yield from en.take(s.stop)._every(step)
                    else:
                        yield from en.skip(s.stop + 1).reverse()._every(-step)
                    return
                elif s.start <= s.stop and step > 0:
                    yield from en.skip(s.start).take(s.stop - s.start)._every(step)
                    return
                elif step <= 0:
                    yield from en.skip(s.stop + 1).take(s.start - s.stop) \
                        .reverse()._every(-step)
            return Enumerable(inner)

    def __getitem__(self,  # type: ignore[override]
        index: Union[int, slice],
    ) -> Union[TSource_co, Enumerable[TSource_co]]:
        return self._getitem_impl(index, fallback=False)

    def __iter__(self) -> Iterator[TSource_co]:
        return iter(self._get_iterable())

    def _len_impl(self, fallback: bool) -> int:
        iterable = self._get_iterable()
        if not fallback and isinstance(iterable, Sized):
            return len(iterable)
        count = 0
        for _ in iterable: count += 1
        return count

    def __len__(self) -> int:
        return self._len_impl(fallback=False)

    def _reversed_impl(self, fallback: bool) -> Iterator[TSource_co]:
        iterable = self._get_iterable()
        # Sequence is an abstract base class without @runtime_checkable
        if not fallback and isinstance(iterable, (Sequence, Reversible)):
            return reversed(iterable)
        return reversed([elem for elem in iterable])

    def __reversed__(self) -> Iterator[TSource_co]:
        return self._reversed_impl(fallback=False)

    @staticmethod
    def _raise_empty_sequence() -> NoReturn:
        raise InvalidOperationError('Sequence is empty')

    def aggregate(self, *args) -> Any:
        if len(args) == 3:
            seed, func, result_selector = args
            for elem in self:
                seed = func(seed, elem)
            return result_selector(seed)

        elif len(args) == 2:
            seed, func = args
            for elem in self:
                seed = func(seed, elem)
            return seed

        else:  # len(args) == 1
            func = args[0]
            iterator = iter(self)
            try:
                seed = next(iterator)
            except StopIteration:
                self._raise_empty_sequence()
            for elem in iterator:
                seed = func(seed, elem)
            return seed

    def all(self, predicate: Callable[[TSource_co], bool]) -> bool:
        for elem in self:
            if not predicate(elem):
                return False
        return True

    def any(self, *args: Callable[[TSource_co], bool]) -> bool:
        if len(args) == 0:
            for _ in self:
                return True
            return False

        else:  # len(args) == 1:
            predicate = args[0]
            for elem in self:
                if predicate(elem):
                    return True
            return False

    def append(self, element: TSource_co) -> Enumerable[TSource_co]:  # type: ignore
        # this method does not mutate the current container
        def inner():
            yield from self
            yield element
        return Enumerable(inner)

    def as_cached(self, *, cache_capacity: Optional[int] = None) -> CachedEnumerable[TSource_co]:
        from .cached_enumerable import CachedEnumerable
        return CachedEnumerable(self, cache_capacity)

    def as_more(self) -> MoreEnumerable[TSource_co]:
        from .more import MoreEnumerable
        return MoreEnumerable(self)

    def _average_helper(self, selector, when_empty):
        count = 0
        iterator = iter(self)

        try:
            sum_ = selector(next(iterator))
            count += 1
        except StopIteration:
            return when_empty()

        for elem in iterator:
            sum_ += selector(elem)
            count += 1
        return sum_ / count

    def average(self, *args: Callable[[TSource_co], Any]) -> Any:
        if len(args) == 0:
            selector = lambda x: x
        else: # len(args) == 1
            selector = args[0]
        return self._average_helper(selector, self._raise_empty_sequence)

    def average2(self, *args):
        if len(args) == 1:
            selector, default = lambda x: x, args[0]
        else: # len(args) == 2
            selector, default = args
        return self._average_helper(selector, lambda: default)

    def cast(self, _: Type[TResult]) -> Enumerable[TResult]:
        return self  # type: ignore

    def concat(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        def inner():
            yield from self
            yield from second
        return Enumerable(inner)

    def contains(self, value: object, *args: Callable[..., bool]):
        if len(args) == 0:
            return self._contains_impl(value, fallback=True)

        else:  # len(args) == 1
            comparer = args[0]
            for elem in self:
                if comparer(elem, value):
                    return True
            return False

    def count(self, *args: Callable[[TSource_co], bool]) -> int:
        if len(args) == 0:
            return self._len_impl(fallback=True)

        else:  # len(args) == 1
            predicate = args[0]
            count = 0
            for elem in self:
                if predicate(elem):
                    count += 1
            return count

    def default_if_empty(self,
        default: TDefault,
    ) -> Union[Enumerable[TSource_co], Enumerable[TDefault]]:
        def inner():
            iterator = iter(self)
            try:
                yield next(iterator)
            except StopIteration:
                yield default
                return
            yield from iterator
        return Enumerable(inner)  # type: ignore

    def distinct(self) -> Enumerable[TSource_co]:
        return self.except1(())

    def element_at(self, index: int, *args: TDefault) -> Union[TSource_co, TDefault]:
        if len(args) == 0:
            return self._getitem_impl(index, fallback=True)  # type: ignore
        else:  # len(args) == 1
            default = args[0]
            try:
                return self._getitem_impl(index, fallback=True)  # type: ignore
            except IndexOutOfRangeError:
                return default

    @staticmethod
    def empty() -> Enumerable[TSource_co]:
        return Enumerable(())

    def except1(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        def inner():
            s = ComposeSet(second)
            for elem in self:
                if elem in s:
                    continue
                s.add(elem)
                yield elem
        return Enumerable(inner)

    @staticmethod
    def _raise_no_such_element() -> NoReturn:
        raise InvalidOperationError('No element satisfying condition')

    def first(self, *args: Callable[[TSource_co], bool]) -> TSource_co:
        if len(args) == 0:
            try:
                return self.element_at(0)  # type: ignore
            except IndexOutOfRangeError as e:
                raise InvalidOperationError(e)

        else:  # len(args) == 1
            predicate = args[0]
            for elem in self:
                if predicate(elem):
                    return elem
            self._raise_no_such_element()

    def first2(self, *args):
        if len(args) == 1:
            default = args[0]
            try:
                return self.element_at(0)  # type: ignore
            except IndexOutOfRangeError:
                return default

        else:  # len(args) == 2
            predicate, default = args
            for elem in self:
                if predicate(elem):
                    return elem
            return default

    def group_by(self,
        key_selector: Callable[[TSource_co], TKey],
        value_selector: Callable[[TSource_co], TValue],
        *args: Callable[[TKey, Enumerable[TValue]], TResult],
    ) -> Union[Enumerable[TResult], Enumerable[Grouping[TKey, TValue]]]:
        from .lookup import Lookup
        if len(args) == 1:
            result_selector = args[0]
            inner = lambda: Lookup(self, key_selector, value_selector) \
                .apply_result_selector(result_selector)  # type: ignore
        else:  # len(args) == 0:
            inner = lambda: Lookup(self, key_selector, value_selector)
        return Enumerable(inner)

    def group_by2(self,
        key_selector: Callable[[TSource_co], TKey],
        *args: Callable[[TKey, Enumerable[TSource_co]], TResult],
    ) -> Union[Enumerable[TResult], Enumerable[Grouping[TKey, TSource_co]]]:
        from .lookup import Lookup
        if len(args) == 1:
            result_selector = args[0]
            inner = lambda: Lookup(self, key_selector, lambda x: x) \
                .apply_result_selector(result_selector)  # type: ignore
        else:  # len(args) == 0:
            inner = lambda: Lookup(self, key_selector, lambda x: x)
        return Enumerable(inner)

    def group_join(self,
        inner: Iterable[TInner],
        outer_key_selector: Callable[[TSource_co], TKey],
        inner_key_selector: Callable[[TInner], TKey],
        result_selector: Callable[[TSource_co, Enumerable[TInner]], TResult],
    ) -> Enumerable[TResult]:
        from .lookup import Lookup
        def inner_gen():
            lookup = Lookup(inner, inner_key_selector, lambda x: x)
            for outer_item in self:
                group = lookup[outer_key_selector(outer_item)]
                yield result_selector(outer_item, group)  # type: ignore
        return Enumerable(inner_gen)

    def intersect(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        def inner():
            s = ComposeSet(second)
            for elem in self:
                if elem not in s:
                    continue
                s.remove(elem)
                yield elem
        return Enumerable(inner)

    def join(self,
        inner: Iterable[TInner],
        outer_key_selector: Callable[[TSource_co], TKey],
        inner_key_selector: Callable[[TInner], TKey],
        result_selector: Callable[[TSource_co, TInner], TResult],
    ) -> Enumerable[TResult]:
        from .lookup import Lookup
        def inner_gen():
            lookup = Lookup(inner, inner_key_selector, lambda x: x)
            for outer_item in self:
                for inner_item in lookup[outer_key_selector(outer_item)]:
                    yield result_selector(outer_item, inner_item)
        return Enumerable(inner_gen)

    def last(self, *args: Callable[[TSource_co], bool]) -> TSource_co:
        ret: Any = _signal
        if len(args) == 0:
            for elem in self:
                ret = elem
            if ret is _signal:
                self._raise_empty_sequence()

        else:  # len(args) == 1
            predicate = args[0]
            for elem in self:
                if predicate(elem):
                    ret = elem
            if ret is _signal:
                self._raise_no_such_element()
        return ret

    def last2(self, *args):
        if len(args) == 1:
            default = args[0]
            for elem in self:
                default = elem

        else:  # len(args) == 2
            predicate, default = args
            for elem in self:
                if predicate(elem):
                    default = elem
        return default

    def _minmax_helper(self, result_selector, op, when_empty) -> Any:
        iterator = iter(self)
        try:
            curr = result_selector(next(iterator))
        except StopIteration:
            return when_empty()
        for elem in iterator:
            mapped = result_selector(elem)
            curr = mapped if op(curr, mapped) else curr
        return curr

    def max(self, *args: Callable[[TSource_co], Any]) -> Any:
        if len(args) == 0:
            result_selector: Any = lambda x: x
        else:  # len(args) == 1
            result_selector = args[0]
        return self._minmax_helper(
            result_selector,
            lambda l, r: l < r,
            self._raise_empty_sequence,
        )

    def max2(self, *args) -> Any:
        if len(args) == 1:
            result_selector, default = lambda x: x, args[0]
        else:  # len(args) == 2
            result_selector, default = args
        return self._minmax_helper(
            result_selector,
            lambda l, r: l < r,
            lambda: default,
        )

    def min(self, *args: Callable[[TSource_co], Any]) -> Any:
        if len(args) == 0:
            result_selector: Any = lambda x: x
        else:  # len(args) == 1
            result_selector = args[0]
        return self._minmax_helper(
            result_selector,
            lambda l, r: r < l,
            self._raise_empty_sequence,
        )

    def min2(self, *args) -> Any:
        if len(args) == 1:
            result_selector, default = lambda x: x, args[0]
        else:  # len(args) == 2
            result_selector, default = args
        return self._minmax_helper(
            result_selector,
            lambda l, r: r < l,
            lambda: default,
        )

    def of_type(self, t_result: Type[TResult]) -> Enumerable[TResult]:
        return self.where(lambda e: isinstance(e, t_result)).cast(t_result)

    def order_by(self,
        key_selector: Callable[[TSource_co], TKey],
        *args: Callable[[TKey, TKey], int],
    ) -> OrderedEnumerable[TSource_co, TKey]:
        from .ordered_enumerable import OrderedEnumerable
        if len(args) == 1:
            comparer = args[0]
        else:  # len(args) == 2:
            comparer = None
        return OrderedEnumerable(
            self._get_iterable,
            None,
            key_selector,
            comparer,
            False,
        )

    def order_by_descending(self,
        key_selector: Callable[[TSource_co], TKey],
        *args: Callable[[TKey, TKey], int],
    ) -> OrderedEnumerable[TSource_co, TKey]:
        from .ordered_enumerable import OrderedEnumerable
        if len(args) == 1:
            comparer = args[0]
        else:  # len(args) == 2:
            comparer = None
        return OrderedEnumerable(
            self._get_iterable,
            None,
            key_selector,
            comparer,
            True,
        )

    def prepend(self, element: TSource_co) -> Enumerable[TSource_co]:  # type: ignore
        # see self.append()
        def inner():
            yield element
            yield from self
        return Enumerable(inner)

    @staticmethod
    def _raise_count_negative() -> NoReturn:
        raise InvalidOperationError('count must be nonnegative')

    @staticmethod
    def range(start: int, count: Optional[int]) -> Enumerable[int]:
        if count is not None:
            if count < 0:
                Enumerable._raise_count_negative()
            def inner(curr=start, cnt=count):  # type: ignore[misc]
                while cnt > 0:
                    yield curr
                    curr += 1
                    cnt -= 1
        else:
            def inner(curr=start):  # type: ignore[misc]
                while True:
                    yield curr
                    curr += 1
        return Enumerable(inner)

    @staticmethod
    def repeat(value: TResult, count: Optional[int] = None) -> Enumerable[TResult]:
        if count is not None:
            if count < 0:
                Enumerable._raise_count_negative()
            def inner(val=value, cnt=count):  # type: ignore[misc]
                while cnt > 0:
                    yield val
                    cnt -= 1
        else:
            def inner(val=value):  # type: ignore[misc]
                while True:
                    yield val
        return Enumerable(inner)

    def reverse(self) -> Enumerable[TSource_co]:
        return Enumerable(lambda: self._reversed_impl(fallback=True))

    def select(self, selector: Callable[[TSource_co], TResult]) -> Enumerable[TResult]:
        def inner():
            for elem in self:
                yield selector(elem)
        return Enumerable(inner)

    def select2(self, selector: Callable[[TSource_co, int], TResult]) -> Enumerable[TResult]:
        def inner():
            for i, elem in enumerate(self):
                yield selector(elem, i)
        return Enumerable(inner)

    def select_many(self,
        collection_selector: Callable[[TSource_co], Iterable[TCollection]],
        *args: Callable[[TSource_co, TCollection], TResult],
    ) -> Union[Enumerable[TCollection], Enumerable[TResult]]:
        if len(args) == 0:
            result_selector: Any = lambda _, x: x
        else:  # len(args) == 1
            result_selector = args[0]
        def inner():
            for elem in self:
                for sub in collection_selector(elem):
                    yield result_selector(elem, sub)
        return Enumerable(inner)

    def select_many2(self,
        collection_selector: Callable[[TSource_co, int], Iterable[TCollection]],
        *args: Callable[[TSource_co, TCollection], TResult],
    ) -> Union[Enumerable[TCollection], Enumerable[TResult]]:
        if len(args) == 0:
            result_selector: Any = lambda _, x: x
        else:  # len(args) == 1
            result_selector = args[0]
        def inner():
            for i, elem in enumerate(self):
                for sub in collection_selector(elem, i):
                    yield result_selector(elem, sub)
        return Enumerable(inner)

    def sequence_equal(self,
        second: Iterable[TSource_co],
        *args: Callable[..., bool],
    ) -> bool:
        if len(args) == 0:
            comparer = lambda x, y: x == y
        else:  # len(args) == 1
            comparer = args[0]

        me, she = iter(self), iter(second)
        while True:
            try:
                lhs = next(me)
            except StopIteration:
                try:
                    next(she)
                    return False
                except StopIteration:
                    return True
            try:
                rhs = next(she)
            except StopIteration:
                return False
            if not comparer(lhs, rhs):
                return False

    def _find_single(self, res):
        for elem in self:
            if res is not _signal:
                raise InvalidOperationError('Sequence does not contain exactly one element')
            res = elem
        return res

    def _find_single_with_predicate(self, res, predicate):
        for elem in self:
            if predicate(elem):
                if res is not _signal:
                    raise InvalidOperationError(
                        'There are multiple elements that satisfy condition: '
                        f'{res} vs. {elem}'
                    )
                res = elem
        return res

    def single(self, *args: Callable[[TSource_co], bool]) -> TSource_co:
        res: Any = _signal
        if len(args) == 0:
            res = self._find_single(res)
            if res is _signal:
                self._raise_empty_sequence()

        else:  # len(args) == 1
            predicate = args[0]
            res = self._find_single_with_predicate(res, predicate)
            if res is _signal:
                self._raise_no_such_element()
        return res

    def single2(self, *args):
        res: Any = _signal
        if len(args) == 1:
            default = args[0]
            res = self._find_single(res)

        else:  # len(args) == 2
            predicate, default = args
            res = self._find_single_with_predicate(res, predicate)
        if res is _signal:
            return default
        return res


    def skip(self, count: int) -> Enumerable[TSource_co]:
        def inner():
            iterator = iter(self)
            try:
                for _ in range(count):
                    next(iterator)
            except StopIteration:
                return
            yield from iterator
        return Enumerable(inner)

    def skip_last(self, count: int) -> Enumerable[TSource_co]:
        if count <= 0:
            return self.skip(0)
        def inner():
            iterator = iter(self)
            q = Deque()
            for elem in iterator:
                if len(q) == count:
                    while True:
                        yield q.pop()
                        q.appendleft(elem)
                        try:
                            elem = next(iterator)
                        except StopIteration:
                            break
                else:
                    q.appendleft(elem)
        return Enumerable(inner)

    def skip_while(self, predicate: Callable[[TSource_co], bool]) -> Enumerable[TSource_co]:
        def inner():
            iterator = iter(self)
            for elem in iterator:
                if not predicate(elem):
                    yield elem
                    break
            yield from iterator
        return Enumerable(inner)

    def skip_while2(self, predicate: Callable[[TSource_co, int], bool]) -> Enumerable[TSource_co]:
        def inner():
            iterator = iter(self)
            for i, elem in enumerate(iterator):
                if not predicate(elem, i):
                    yield elem
                    break
            yield from iterator
        return Enumerable(inner)

    def _sum_helper(self, selector, when_empty):
        iterator = iter(self)
        try:
            sum_ = selector(next(iterator))
        except StopIteration:
            return when_empty()

        for elem in iterator:
            sum_ += selector(elem)
        return sum_

    def sum(self, *args) -> Any:
        if len(args) == 0:
            selector: Any = lambda x: x
        else:  # len(args) == 1
            selector = args[0]
        return self._sum_helper(selector, lambda: 0)

    def sum2(self, *args) -> Any:
        if len(args) == 1:
            selector, default = lambda x: x, args[0]
        else: # len(args) == 2
            selector, default = args
        return self._sum_helper(selector, lambda: default)

    def take(self, count: int) -> Enumerable[TSource_co]:
        def inner():
            iterator = iter(self)
            try:
                for _ in range(count):
                    yield next(iterator)
            except StopIteration:
                return
        return Enumerable(inner)

    def take_last(self, count: int) -> Enumerable[TSource_co]:
        if count <= 0:
            return self.empty()
        def inner():
            iterator = iter(self)
            try:
                q = Deque((next(iterator),))
            except StopIteration:
                return
            for elem in iterator:
                if len(q) == count:
                    while True:
                        q.popleft()
                        q.append(elem)
                        try:
                            elem = next(iterator)
                        except StopIteration:
                            break
                else:
                    q.append(elem)
            yield from q
        return Enumerable(inner)

    def take_while(self, predicate: Callable[[TSource_co], bool]) -> Enumerable[TSource_co]:
        def inner():
            for elem in self:
                if not predicate(elem):
                    break
                yield elem
        return Enumerable(inner)

    def take_while2(self, predicate: Callable[[TSource_co, int], bool]) -> Enumerable[TSource_co]:
        def inner():
            for i, elem in enumerate(self):
                if not predicate(elem, i):
                    break
                yield elem
        return Enumerable(inner)

    def to_dict(self,
        key_selector: Callable[[TSource_co], TKey],
        *args: Callable[[TSource_co], TValue],
    ) -> Union[Dict[TKey, TValue], Dict[TKey, TSource_co]]:
        if len(args) == 0:
            value_selector: Any = lambda x: x
        else:  # len(args) == 1
            value_selector = args[0]
        return {key_selector(e): value_selector(e) for e in self}

    def to_set(self) -> Set[TSource_co]:
        return {e for e in self}

    def to_list(self) -> List[TSource_co]:
        return [e for e in self]

    def to_lookup(self,
        key_selector: Callable[[TSource_co], TKey],
        *args: Callable[[TSource_co], TValue],
    ) -> Union[Lookup[TKey, TValue], Lookup[TKey, TSource_co]]:
        from .lookup import Lookup
        if len(args) == 0:
            value_selector: Any = lambda x: x
        else:  # len(args) == 1
            value_selector = args[0]
        res = Lookup(self, key_selector, value_selector)
        return res

    def union(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        def inner():
            # TODO: optimise chained .union() call to reuse s
            s = ComposeSet()
            for elem in self.concat(second):
                if elem in s:
                    continue
                s.add(elem)
                yield elem
        return Enumerable(inner)

    def where(self, predicate: Callable[[TSource_co], bool]) -> Enumerable[TSource_co]:
        def inner():
            for elem in self:
                if predicate(elem):
                    yield elem
        return Enumerable(inner)

    def where2(self, predicate: Callable[[TSource_co, int], bool]) -> Enumerable[TSource_co]:
        def inner():
            for i, elem in enumerate(self):
                if predicate(elem, i):
                    yield elem
        return Enumerable(inner)

    def zip(self, *iters: Iterable[Any]) -> Enumerable[Any]:
        def inner():
            yield from zip(self, *iters)
        return Enumerable(inner)

    def zip2(self, *iters_and_result_selector: Any) -> Enumerable[Any]:
        iters = iters_and_result_selector[:-1]
        result_selector = iters_and_result_selector[-1]
        def inner():
            for tup in zip(self, *iters):
                yield result_selector(*tup)
        return Enumerable(inner)

    def elements_in(self, *args) -> Enumerable[TSource_co]:
        if len(args) == 1:
            index = args[0]
            return self._getitem_impl(index, fallback=True)  # type: ignore
        elif len(args) == 2:
            start, stop = args
            return self.elements_in(start, stop, 1)
        else:  # len(args) == 3
            return self.elements_in(slice(*args))

    def to_tuple(self) -> Tuple[TSource_co, ...]:
        return tuple(e for e in self)
