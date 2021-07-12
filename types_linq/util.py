from __future__ import annotations
from typing import Tuple, Iterator, Hashable, List, Dict, Iterable, Set, Optional, MutableMapping, MutableSet

from .more_typing import (
    TKey,
    TValue
)

class _ListMap(MutableMapping[TKey, TValue]):

    def __init__(self) -> None:
        self._lst: List[Tuple[TKey, TValue]] = list()
    
    def __setitem__(self, key: TKey, value: TValue) -> None:
        for i in range(0, len(self._lst)):
            if self._lst[i][0] == key:
                self._lst[i] = (self._lst[i][0], value)
                return
        self._lst.append((key, value))
    
    def __getitem__(self, key: TKey) -> TValue:
        for k, v in self._lst:
            if k == key:
                return v
        raise KeyError(key)

    def __delitem__(self, key: TKey) -> None:
        for i in range(0, len(self._lst)):
            if self._lst[i][0] == key:
                del self._lst[i]
                return
        raise KeyError(key)

    def __iter__(self) -> Iterator[TKey]:
        return map(lambda e: e[0], self._lst)

    def __len__(self) -> int:
        return len(self._lst)


# Wrap Map to Set
class _SetWrapper(MutableSet[TValue]):

    def __init__(self, map: MutableMapping[TValue, None]) -> None:
        self._map = map

    def __contains__(self, x: object) -> bool:
        return x in self._map

    def __len__(self) -> int:
        return self._map.__len__()

    def add(self, value: TValue) -> None:
        self._map[value] = None

    def discard(self, value: TValue) -> None:
        try:
            self._map.pop(value)
        except KeyError:
            # set.discard() don't throw KeyError 
            # if element doesn't exist 
            ...
    
    def __iter__(self) -> Iterator[TValue]:
        return self._map.__iter__()


class ComposeSet(MutableSet[TValue]):
    '''
    A set which support hashable and unhashable type
    '''
    _set: Set[TValue]
    _cmp_set: MutableSet[TValue]

    def __init__(self, iter: Optional[Iterable[TValue]] = None):
        self._set = set()
        self._cmp_set = _SetWrapper(_ListMap())
        if iter:
            for item in iter:
                self.add(item)

    def _get_set(self, x: object) -> MutableSet[TValue]:
        if isinstance(x, Hashable):
            return self._set
        else:
            return self._cmp_set

    def __contains__(self, x: object) -> bool:
        return x in self._get_set(x)

    def __len__(self) -> int:
        return len(self._set) + len(self._cmp_set)

    def __iter__(self) -> Iterator[TValue]:
        yield from self._set
        yield from self._cmp_set

    def add(self, value: TValue) -> None:
        return self._get_set(value).add(value)

    def discard(self, value: TValue) -> None:
        return self._get_set(value).discard(value)


class ComposeMap(MutableMapping[TKey, TValue]):
    '''
    A map which support hashable and unhashable key type
    '''
    _map: Dict[TKey, TValue]
    _cmp_map: MutableMapping[TKey, TValue]

    def __init__(self, iter: Optional[Iterable[Tuple[TKey, TValue]]] = None) -> None:
        self._map = dict()
        self._cmp_map = _ListMap()
        if iter:
            for k, v in iter:
                self[k] = v

    def _get_map(self, x: object) -> MutableMapping[TKey, TValue]:
        # TODO: this test is not perfectly sufficient.
        # counterexample: x is namedtuple('t', ['x'])([])
        if isinstance(x, Hashable):
            return self._map
        else:
            return self._cmp_map

    def __setitem__(self, key: TKey, value: TValue):
        self._get_map(key).__setitem__(key, value)
    
    def __getitem__(self, key: TKey) -> TValue:
        return self._get_map(key).__getitem__(key)

    def __delitem__(self, key: TKey) -> None:
        return self._get_map(key).__delitem__(key)

    def __iter__(self) -> Iterator[TKey]:
        # notice on iteration order:
        # if this data structure contains only hashable objects (stored in the dict)
        # then the iter order is consistent with dict => using insertion order. this is
        # useful for meeting the .net ToLookup() spec. however, if this is not the case
        # then the iter order is broken.
        yield from self._map
        yield from self._cmp_map

    def __len__(self) -> int:
        return len(self._map) + len(self._cmp_map)
