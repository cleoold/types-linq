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


class _Set(MutableSet[TValue]):

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



class _Map(MutableMapping[TKey, TValue]):

    _map: Dict[TKey, TValue]
    _cmp_map: MutableMapping[TKey, TValue]

    def __init__(self, iter: Optional[Iterable[Tuple[TKey, TValue]]] = None) -> None:
        self._map = dict()
        self._cmp_map = _ListMap()
        if iter:
            for k, v in iter:
                self[k] = v

    def _get_map(self, x: object) -> MutableMapping[TKey, TValue]:
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
        yield from self._map
        yield from self._cmp_map

    def __len__(self) -> int:
        return len(self._map) + len(self._cmp_map)