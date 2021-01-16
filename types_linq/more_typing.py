import sys
from abc import ABCMeta, abstractmethod
from typing import Any

if sys.version_info >= (3, 8, 0):
    from typing import Protocol, runtime_checkable
else:
    from typing_extensions import Protocol, runtime_checkable  # type: ignore


@runtime_checkable
class SupportsAddAndDiv(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __add__(self, __o: Any) -> Any: ...
    @abstractmethod
    def __truediv__(self, __o: Any) -> Any: ...


@runtime_checkable
class SupportsLessThan(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, __o: Any) -> bool: ...


# a type like 'Hashable' is rn useless because a subclass of a hashable class may not
# be hashable (object -> list)
