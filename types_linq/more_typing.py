import sys
from typing import Any, runtime_checkable

if sys.version_info >= (3, 8, 0):
    from typing import Protocol
else:
    from typing_extensions import Protocol


@runtime_checkable
class SupportsAddAndDiv(Protocol):
    def __add__(self, o: Any) -> Any: ...
    def __truediv__(self, o: Any) -> Any: ...
