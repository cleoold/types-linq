from __future__ import annotations
from typing import Generic, List

from .enumerable import Enumerable

from .more_typing import (
    TKey_co,
    TValue_co,
)


# kind of respect IGrouping's covariant type parameters if the method _append()
# is really treated as an internal method
class Grouping(Enumerable[TValue_co], Generic[TKey_co, TValue_co]):
    '''
    .. code-block:: python

        from types_linq.grouping import Grouping

    Represents a collection of objects that have a common key.

    Users should not construct instances of this class directly. Use ``Enumerable.group_by()`` instead.
    '''

    _key: TKey_co
    _values: List[TValue_co]

    def __init__(self, key: TKey_co):  # type: ignore
        self._values = []
        super().__init__(self._values)
        self._key = key

    @property
    def key(self) -> TKey_co:
        '''
        Gets the key of the grouping.
        '''
        return self._key

    def _append(self, value: TValue_co) -> None:  # type: ignore
        self._values.append(value)
