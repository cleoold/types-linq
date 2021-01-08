from __future__ import annotations
from typing import Callable, Iterable, Iterator, List, TypeVar, Generic, Union


TSource_co = TypeVar('TSource_co', covariant=True)


class Enumerable(Generic[TSource_co]):

    _iter_factory: Callable[[], Iterator[TSource_co]]

    def __init__(self,
        it: Union[Iterable[TSource_co], Callable[[], Iterable[TSource_co]]]
    ):
        if callable(it):
            self._iter_factory = lambda it_=it: iter(it_())
        else:
            self._iter_factory = lambda it_=it: iter(it_)

    def __iter__(self) -> Iterator[TSource_co]:
        return self._iter_factory()

    def aggregate(self, *args):
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
                raise TypeError('Sequence is empty')
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

    def to_list(self) -> List[TSource_co]:
        return list(iter(self))

