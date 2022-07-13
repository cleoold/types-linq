# module ``types_linq.more.more_error``

(apiref.DirectedGraphNotAcyclicError)=
## class `DirectedGraphNotAcyclicError`

```py
from types_linq.more import DirectedGraphNotAcyclicError
```

Exception raised when a cycle exists in a graph.

Revisions
    ~ main: New.

### Bases

- [`InvalidOperationError`](apiref.InvalidOperationError)

### Members

#### instanceproperty `cycle`

Returns
  ~ `Tuple[object, object]`

The two elements (A, B) in this tuple are part of a cycle. There exists an edge from A to B,
and a path from B back to A. A and B may be identical.

Example
    ~   ```py
        >>> adj = { 5: [2, 0], 4: [0, 1], 2: [3], 3: [1, 5] }
        >>> try:
        >>>     MoreEnumerable([5, 4]).traverse_topological(lambda x: adj.get(x, [])) \
        >>>         .consume()
        >>> except DirectedGraphNotAcyclicError as e:
        >>>     print(e.cycle)
        (3, 5)  # 3 -> 5 -> 2 -> 3
        ```

