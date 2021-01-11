from typing import Generic, List, TypeVar

from .enumerable import Enumerable


TKey_co = TypeVar('TKey_co', covariant=True)
TValue_co = TypeVar('TValue_co', covariant=True)


# kind of respect IGrouping's covariant type parameters if the method _append()
# is really treated as an internal method
class Grouping(Enumerable[TValue_co], Generic[TKey_co, TValue_co]):

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
