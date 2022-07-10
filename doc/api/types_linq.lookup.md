# module ``types_linq.lookup``

## class `Lookup[TKey_co, TValue_co]`

```py
from types_linq.lookup import Lookup
```

A lookup is a one-to-many dictionary. It maps keys to Enumerable sequences of values.

Users should not construct instances of this class directly. Use `Enumerable.to_lookup()`
instead.

### Bases

- `Enumerable[Grouping[TKey_co, TValue_co]]`

### Members

#### instanceproperty `count`

Returns
  ~ `int`

Gets the number of key-collection pairs.

---

#### instancemethod `__contains__(value)`

Parameters
  ~ *value* (`object`)

Returns
  ~ `bool`

Tests whether key is in the lookup.

---

#### instancemethod `__len__()`


Returns
  ~ `int`

Gets the number of key-collection pairs.

---

#### instancemethod `__getitem__(key)`

Parameters
  ~ *key* (`TKey_co`)

Returns
  ~ `Enumerable[TValue_co]`

Gets the collection of values indexed by the specified key, or empty if no such key
exists.

---

#### instancemethod `apply_result_selector[TResult](result_selector)`

Parameters
  ~ *result_selector* (`Callable[[TKey_co, Enumerable[TValue_co]], TResult]`)

Returns
  ~ `Enumerable[TResult]`

Applies a transform function to each key and its associated values, then returns the
results.

---

#### instancemethod `contains(value)`

Parameters
  ~ *value* (`object`)

Returns
  ~ `bool`

Tests whether key is in the lookup.

