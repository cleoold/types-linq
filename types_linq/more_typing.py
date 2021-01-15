import sys
from typing import Any

if sys.version_info >= (3, 8, 0):
    from typing import Protocol, runtime_checkable
else:
    from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class SupportsAddAndDiv(Protocol):
    def __add__(self, o: Any) -> Any: ...
    def __truediv__(self, o: Any) -> Any: ...


# a type like 'Hashable' is rn useless because a subclass of a hashable class may not
# be hashable (object -> list)
