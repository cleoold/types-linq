# module ``types_linq.cached_enumerable``

(apiref.CachedEnumerable)=
## class `CachedEnumerable[TSource_co]`

```py
from types_linq.cached_enumerable import CachedEnumerable
```

Enumerable that stores the enumerated results which can be accessed repeatedly.

Users should not construct instances of this class directly. Use `Enumerable.as_cached()` instead.

Revisions
    ~ v0.1.1: New.

### Bases

- [`Enumerable`](apiref.Enumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

### Members

#### instancemethod `as_cached(*, cache_capacity=None)`

Parameters
  ~ *cache_capacity*: `Optional[int]`

Returns
  ~ [`CachedEnumerable`](apiref.CachedEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Updates settings and returns the original CachedEnumerable reference.

Raises [`InvalidOperationError`](apiref.InvalidOperationError) if cache_capacity is negative.

