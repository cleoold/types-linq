from __future__ import annotations
from typing import Any, Callable, Container, Dict, Iterable, Iterator, List, NoReturn, Optional, Reversible, Sequence, Set, Sized, TYPE_CHECKING, Tuple, Type, TypeVar, Generic, Union

if TYPE_CHECKING:
    from .lookup import Lookup


TSource_co = TypeVar('TSource_co', covariant=True)
TResult = TypeVar('TResult')
TDefault = TypeVar('TDefault')
TOther = TypeVar('TOther')
TKey = TypeVar('TKey')
TValue = TypeVar('TValue')
TCollection = TypeVar('TCollection')


class Enumerable(Sequence[TSource_co], Generic[TSource_co]):

    _iter_factory: Callable[[], Iterable[TSource_co]]
    _configured_repeatable: bool = False

    def __init__(self,
        it: Union[Iterable[TSource_co], Callable[[], Iterable[TSource_co]]]
    ):
        if callable(it):
            self._iter_factory = lambda it_=it: it_()
        else:
            self._iter_factory = lambda it_=it: it_

    def __contains__(self, value: object) -> bool:
        iterable = self._iter_factory()
        # prefer calling __contains__(), otherwise fallback to for loop
        if isinstance(iterable, Container):
            return value in iterable
        for elem in iterable:
            if elem == value:
                return True
        return False

    def _every(self, step: int) -> Enumerable[TSource_co]:
        return self.where2(lambda _, i: i % step == 0)

    def __getitem__(self,
        index: Union[int, slice],
    ) -> Union[TSource_co, Enumerable[TSource_co]]:
        iterable = self._iter_factory()
        if isinstance(index, int):
            # prefer calling __getitem__(), otherwise fallback to for loop
            # Sequence is an abstract base class without @runtime_checkable
            if isinstance(iterable, Sequence):
                # an appropriate implementation should raise IndexError
                return iterable[index]
            iterator = iter(iterable)
            try:
                for _ in range(index):
                    next(iterator)
                return next(iterator)
            except StopIteration:
                raise IndexError('Not enough elements in the sequence')

        else:  # isinstance(index, slice)
            # prefer calling __getitem__(), otherwise fallback
            if isinstance(iterable, Sequence):
                res = iterable[index]
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
                    if s.stop >= 0:
                        if step > 0:
                            yield from en.take(s.stop)._every(step)
                        else:
                            yield from en.skip(s.stop + 1).reverse()._every(-step)
                        return
                    yield from en.to_list()[s]
                elif s.start <= s.stop:
                    en = en.skip(s.start).take(s.stop - s.start)
                    if step > 0:
                        yield from en._every(step)
                    else:
                        yield from en.reverse()._every(-step)
                elif step <= 0:
                    yield from en.skip(s.stop + 1).take(s.start - s.stop) \
                        .reverse()._every(-step)
            return Enumerable(inner)

    def __iter__(self) -> Iterator[TSource_co]:
        return iter(self._iter_factory())

    def __len__(self) -> int:
        iterable = self._iter_factory()
        # prefer calling __len__(), otherwise fallback to for loop
        if isinstance(iterable, Sized):
            return len(iterable)
        count = 0
        for _ in iterable: count += 1
        return count

    def __reversed__(self) -> Iterator[TSource_co]:
        iterable = self._iter_factory()
        # prefer calling __reversed__(), otherwise enumerate all items
        # Sequence is an abstract base class without @runtime_checkable
        if isinstance(iterable, (Sequence, Reversible)):
            return reversed(iterable)
        return reversed([elem for elem in iterable])

    @staticmethod
    def _raise_empty_sequence() -> NoReturn:
        raise TypeError('Sequence is empty')

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
        return self

    def concat(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        def inner():
            yield from self
            yield from second
        return Enumerable(inner)

    def configure_repeatable(self) -> Enumerable[TSource_co]:
        if self._configured_repeatable:
            raise TypeError('Already configured')

        iterator = iter(self)
        enumerated_values: List[TSource_co] = []
        def closure():
            i = 0
            while True:
                while i < len(enumerated_values):
                    res = enumerated_values[i]
                    i += 1
                    yield res
                try:
                    res = next(iterator)
                    enumerated_values.append(res)
                    i += 1
                    yield res
                except StopIteration:
                    break

        self._iter_factory = closure
        self._configured_repeatable = True
        return self

    def contains(self, value: object, *args: Callable[..., bool]):
        if len(args) == 0:
            return value in self

        else:  # len(args) == 1
            comparer = args[0]
            for elem in self:
                if comparer(elem, value):
                    return True
            return False

    def count(self, *args: Callable[[TSource_co], bool]) -> int:
        if len(args) == 0:
            return len(self)

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
        return Enumerable(inner)

    def distinct(self) -> Enumerable[TSource_co]:
        def inner():
            s = set()
            for elem in self:
                if elem in s:
                    continue
                s.add(elem)
                yield elem
        return Enumerable(inner)

    def element_at(self, index: int, *args: TDefault) -> Union[TSource_co, TDefault]:
        if len(args) == 0:
            return self[index]  # type: ignore
        else:  # len(args) == 1
            default = args[0]
            try:
                return self[index]  # type: ignore
            except IndexError:
                return default

    @staticmethod
    def empty() -> Enumerable[TSource_co]:
        return Enumerable(())

    def except1(self, second: Iterable[TSource_co]) -> Enumerable[TSource_co]:
        def inner():
            s = {*second}
            for elem in self:
                if elem in s:
                    continue
                s.add(elem)
                yield elem
        return Enumerable(inner)

    def first(self, *args: Callable[[TSource_co], bool]) -> TSource_co:
        if len(args) == 0:
            try:
                return self[0]  # type: ignore
            except IndexError as e:
                raise ValueError(*e.args)

        else:  # len(args) == 1
            predicate = args[0]
            for elem in self:
                if predicate(elem):
                    return elem
            raise ValueError('No element satisfying condition')

    def first2(self, *args):
        if len(args) == 1:
            default = args[0]
            try:
                return self[0]
            except IndexError:
                return default

        else:  # len(args) == 2
            predicate, default = args
            for elem in self:
                if predicate(elem):
                    return elem
            return default

    def reverse(self) -> Enumerable[TSource_co]:
        return Enumerable(lambda: reversed(self))

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

    def take(self, count: int) -> Enumerable[TSource_co]:
        def inner():
            iterator = iter(self)
            try:
                for _ in range(count):
                    yield next(iterator)
            except StopIteration:
                return
        return Enumerable(inner)

    def to_dict(self,
        key_selector: Callable[[TSource_co], TKey],
        *args: Callable[[TSource_co], TValue],
    ) -> Union[Dict[TKey, TValue], Dict[TKey, TSource_co]]:
        if len(args) == 0:
            value_selector: Any = lambda x: x
        else:  # len(args) == 1
            value_selector = args[0]
        return dict((key_selector(e), value_selector(e)) for e in self)

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

    def zip(self,
        second: Iterable[TOther],
        *args: Callable[[TSource_co, TOther], TResult],
    ) -> Union[Enumerable[TResult], Enumerable[Tuple[TSource_co, TOther]]]:
        if len(args) == 0:
            result_selector: Any = lambda x, y: (x, y)
        else:  # len(args) == 1
            result_selector = args[0]
        def inner():
            for x, y in zip(self, second):
                yield result_selector(x, y)
        return Enumerable(inner)
