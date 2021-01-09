from __future__ import annotations
from typing import Any, Callable, Container, Dict, Iterable, Iterator, List, NoReturn, Set, Sized, Tuple, Type, TypeVar, Generic, Union


TSource_co = TypeVar('TSource_co', covariant=True)
TResult = TypeVar('TResult')
TDefault = TypeVar('TDefault')
TOther = TypeVar('TOther')
TKey = TypeVar('TKey')
TValue = TypeVar('TValue')
TCollection = TypeVar('TCollection')


class Enumerable(Generic[TSource_co]):

    _iter_factory: Callable[[], Iterable[TSource_co]]

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

    def __iter__(self) -> Iterator[TSource_co]:
        return iter(self._iter_factory())

    def __len__(self) -> int:
        iterable = self._iter_factory()
        # prefer calling __len__(), otherwise fallback to for loop
        if isinstance(iterable, Sized):
            return len(iterable)
        count = 0
        for _ in self: count += 1
        return count

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
