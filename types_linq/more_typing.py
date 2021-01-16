import sys
from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar

if sys.version_info >= (3, 8, 0):
    from typing import Protocol, runtime_checkable
else:
    from typing_extensions import Protocol, runtime_checkable  # type: ignore


TSelf = TypeVar('TSelf')
TAverage_co = TypeVar('TAverage_co', covariant=True)


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


# a type like 'Hashable' is rn useless because a subclass of a hashable class may not
# be hashable (object -> list)
