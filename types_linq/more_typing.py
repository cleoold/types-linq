import sys
from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar

if sys.version_info >= (3, 8, 0):
    from typing import Protocol, runtime_checkable
else:
    from typing_extensions import Protocol, runtime_checkable  # type: ignore


TAccumulate = TypeVar('TAccumulate')
TAverage_co = TypeVar('TAverage_co', covariant=True)
TCollection = TypeVar('TCollection')
TDefault = TypeVar('TDefault')
TInner = TypeVar('TInner')
TKey = TypeVar('TKey')
TKey2 = TypeVar('TKey2')
TKey_co = TypeVar('TKey_co', covariant=True)
TOther = TypeVar('TOther')
TOther2 = TypeVar('TOther2')
TOther3 = TypeVar('TOther3')
TOther4 = TypeVar('TOther4')
TResult = TypeVar('TResult')
TSelf = TypeVar('TSelf')
TSource = TypeVar('TSource')
TSource_co = TypeVar('TSource_co', covariant=True)
TValue = TypeVar('TValue')
TValue_co = TypeVar('TValue_co', covariant=True)


@runtime_checkable
class SupportsAverage(Protocol[TAverage_co]):
    @abstractmethod
    def __add__(self: TSelf, __o: TSelf) -> TSelf: ...
    @abstractmethod
    def __truediv__(self, __o: int) -> TAverage_co: ...


@runtime_checkable
class SupportsLessThan(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, __o: Any) -> bool: ...

@runtime_checkable
class SupportsAdd(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __add__(self: TSelf, __o: TSelf) -> TSelf: ...


# a type like 'Hashable' is rn useless because a subclass of a hashable class may not
# be hashable (object -> list)

TSupportsLessThan = TypeVar('TSupportsLessThan', bound=SupportsLessThan)
TSupportsAdd = TypeVar('TSupportsAdd', bound=SupportsAdd)
