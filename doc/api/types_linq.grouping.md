# module ``types_linq.grouping``

(apiref.Grouping)=
## class `Grouping[TValue_co, TKey_co]`

```py
from types_linq.grouping import Grouping
```

Represents a collection of objects that have a common key.

Users should not construct instances of this class directly. Use `Enumerable.group_by()` instead.

### Bases

- [`Enumerable`](apiref.Enumerable)`[`[`TValue_co`](apiref.TValue_co)`]`
- `Generic[`[`TKey_co`](apiref.TKey_co)`, `[`TValue_co`](apiref.TValue_co)`]`

### Members

#### instanceproperty `key`

Returns
  ~ [`TKey_co`](apiref.TKey_co)

Gets the key of the grouping.

