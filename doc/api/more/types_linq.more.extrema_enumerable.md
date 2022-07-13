# module ``types_linq.more.extrema_enumerable``

(apiref.ExtremaEnumerable)=
## class `ExtremaEnumerable[TSource_co, TKey]`

```py
from types_linq.more.extrema_enumerable import ExtremaEnumerable
```

Specialization for manipulating extrema.

Users should not construct instances of this class directly. Use `MoreEnumerable.maxima_by()`
instead.

Revisions
    ~ v0.2.0: New.

### Bases

- [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`
- `Generic[`[`TSource_co`](apiref.TSource_co)`, `[`TKey`](apiref.TKey)`]`

### Members

#### instancemethod `take(count)`

Parameters
  ~ *count*: `int`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Returns a specified number of contiguous elements from the start of the sequence.

---

#### instancemethod `take(__index)`

Parameters
  ~ *__index*: `slice`

Returns
  ~ [`Enumerable`](apiref.Enumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Identical to parent.

Revisions
    ~ v1.1.0: Fixed incorrect override of `Enumerable.take()` when it takes a slice.

---

#### instancemethod `take_last(count)`

Parameters
  ~ *count*: `int`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Returns a new sequence that contains the last `count` elements.

