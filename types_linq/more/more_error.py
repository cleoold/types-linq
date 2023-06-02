# class 'MoreError' is nonexistent
from __future__ import annotations
from typing import Tuple

from ..types_linq_error import InvalidOperationError


class DirectedGraphNotAcyclicError(InvalidOperationError):
    '''
    ```py
    from types_linq.more import DirectedGraphNotAcyclicError
    ```

    Exception raised when a cycle exists in a graph.

    Revisions
        ~ v1.2.1: New.
    '''

    def __init__(self, cycle: Tuple[object, object]) -> None:
        super().__init__('cycle detected')
        self._cycle = cycle

    @property
    def cycle(self) -> Tuple[object, object]:
        '''
        The two elements (A, B) in this tuple are part of a cycle. There exists an edge from A to B,
        and a path from B back to A. A and B may be identical.

        Example
        ```py
        >>> adj = { 5: [2, 0], 4: [0, 1], 2: [3], 3: [1, 5] }
        >>> try:
        >>>     MoreEnumerable([5, 4]).traverse_topological(lambda x: adj.get(x, [])) \\
        >>>         .consume()
        >>> except DirectedGraphNotAcyclicError as e:
        >>>     print(e.cycle)
        (3, 5)  # 3 -> 5 -> 2 -> 3
        ```
        '''
        return self._cycle
