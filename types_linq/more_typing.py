'''
Typing utilities used by methods's declarations across the library. For more details, see
[`typing`](https://docs.python.org/3/library/typing.html).
```{note} Definitions in this module are for documenting purposes only.
```
'''
import sys
from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar

if sys.version_info >= (3, 8, 0):
    from typing import Protocol, runtime_checkable
else:
    from typing_extensions import Protocol, runtime_checkable  # type: ignore


TAccumulate = TypeVar('TAccumulate')
'A generic type parameter.'

TAverage_co = TypeVar('TAverage_co', covariant=True)
'A generic covariant type parameter.'

TCollection = TypeVar('TCollection')
'A generic type parameter.'

TDefault = TypeVar('TDefault')
'A generic type parameter.'

TInner = TypeVar('TInner')
'A generic type parameter.'

TKey = TypeVar('TKey')
'A generic type parameter.'

TKey2 = TypeVar('TKey2')
'A generic type parameter.'

TKey_co = TypeVar('TKey_co', covariant=True)
'A generic covariant type parameter.'

TOther = TypeVar('TOther')
'A generic type parameter.'

TOther2 = TypeVar('TOther2')
'A generic type parameter.'

TOther3 = TypeVar('TOther3')
'A generic type parameter.'

TOther4 = TypeVar('TOther4')
'A generic type parameter.'

TResult = TypeVar('TResult')
'A generic type parameter.'

TSelf = TypeVar('TSelf')
'A generic type parameter.'

TSource = TypeVar('TSource')
'A generic type parameter.'

TSource_co = TypeVar('TSource_co', covariant=True)
'A generic covariant type parameter.'

TValue = TypeVar('TValue')
'A generic type parameter.'

TValue_co = TypeVar('TValue_co', covariant=True)
'A generic covariant type parameter.'


@runtime_checkable
class SupportsAverage(Protocol[TAverage_co]):
    '''
    Instances of this protocol supports the averaging operation. that is, if `x` is such an instance,
    and `N` is an integer, then `(x + x + ...) / N` is allowed, and has the type `TAverage_co`.
    '''
    @abstractmethod
    def __add__(self: TSelf, __o: TSelf) -> TSelf: ...
    @abstractmethod
    def __truediv__(self, __o: int) -> TAverage_co: ...


@runtime_checkable
class SupportsLessThan(Protocol, metaclass=ABCMeta):
    '''
    Instances of this protocol supports the `<` operation.

    Even though they may be unimplemented, the existence of `<` implies the existence of `>`,
    and probably `==`, `!=`, `<=` and `>=`.
    '''
    @abstractmethod
    def __lt__(self, __o: Any) -> bool: ...

@runtime_checkable
class SupportsAdd(Protocol, metaclass=ABCMeta):
    '''
    Instances of this protocol supports the homogeneous `+` operation.
    '''
    @abstractmethod
    def __add__(self: TSelf, __o: TSelf) -> TSelf: ...


# a type like 'Hashable' is rn useless because a subclass of a hashable class may not
# be hashable (object -> list)

TSupportsLessThan = TypeVar('TSupportsLessThan', bound=SupportsLessThan)
'A generic type parameter that represents a type that `SupportsLessThan`.'

TSupportsAdd = TypeVar('TSupportsAdd', bound=SupportsAdd)
'A generic type parameter that represents a type that `SupportsAdd`.'
