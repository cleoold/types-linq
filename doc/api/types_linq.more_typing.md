# module ``types_linq.more_typing``

Typing utilities used by methods's declarations across the library. For more details, see
[`typing`](https://docs.python.org/3/library/typing.html).
```{note} Definitions in this module are for documenting purposes only.
```

## Constants

### `TAccumulate`

Equals
  ~ `TypeVar('TAccumulate')`

A generic type parameter.

---

### `TAverage_co`

Equals
  ~ `TypeVar('TAverage_co', covariant=True)`

A generic type parameter.

---

### `TCollection`

Equals
  ~ `TypeVar('TCollection')`

A generic type parameter.

---

### `TDefault`

Equals
  ~ `TypeVar('TDefault')`

A generic type parameter.

---

### `TInner`

Equals
  ~ `TypeVar('TInner')`

A generic type parameter.

---

### `TKey`

Equals
  ~ `TypeVar('TKey')`

A generic type parameter.

---

### `TKey2`

Equals
  ~ `TypeVar('TKey2')`

A generic type parameter.

---

### `TKey_co`

Equals
  ~ `TypeVar('TKey_co', covariant=True)`

A generic covariant type parameter.

---

### `TOther`

Equals
  ~ `TypeVar('TOther')`

A generic type parameter.

---

### `TOther2`

Equals
  ~ `TypeVar('TOther2')`

A generic type parameter.

---

### `TOther3`

Equals
  ~ `TypeVar('TOther3')`

A generic type parameter.

---

### `TOther4`

Equals
  ~ `TypeVar('TOther4')`

A generic type parameter.

---

### `TResult`

Equals
  ~ `TypeVar('TResult')`

A generic type parameter.

---

### `TSelf`

Equals
  ~ `TypeVar('TSelf')`

A generic type parameter.

---

### `TSource`

Equals
  ~ `TypeVar('TSource')`

A generic type parameter.

---

### `TSource_co`

Equals
  ~ `TypeVar('TSource_co', covariant=True)`

A generic covariant type parameter.

---

### `TValue`

Equals
  ~ `TypeVar('TValue')`

A generic type parameter.

---

### `TValue_co`

Equals
  ~ `TypeVar('TValue_co', covariant=True)`

A generic covariant type parameter.

---

### `TSupportsLessThan`

Equals
  ~ `TypeVar('TSupportsLessThan', bound=SupportsLessThan)`

A generic type parameter that represents a type that `SupportsLessThan`.

---

### `TSupportsAdd`

Equals
  ~ `TypeVar('TSupportsAdd', bound=SupportsAdd)`

A generic type parameter that represents a type that `SupportsAdd`.

---

## class `SupportsAverage[TAverage_co]`

Instances of this protocol supports the averaging operation. that is, if `x` is such an instance,
and `N` is an integer, then `(x + x + ...) / N` is allowed, and has the type `TAverage_co`.

### Bases

- `Protocol[TAverage_co]`

### Members

#### abstract instancemethod `__add__[TSelf](__o)`

Constraint
  ~ *self*: `TSelf`

Parameters
  ~ *__o* (`TSelf`)

Returns
  ~ `TSelf`



---

#### abstract instancemethod `__truediv__(__o)`

Parameters
  ~ *__o* (`int`)

Returns
  ~ `TAverage_co`



---

## class `SupportsLessThan`

Instances of this protocol supports the `<` operation.

Even though they may be unimplemented, the existence of `<` implies the existence of `>`,
and probably `==`, `!=`, `<=` and `>=`.

### Bases

- `Protocol`

### Members

#### abstract instancemethod `__lt__(__o)`

Parameters
  ~ *__o* (`Any`)

Returns
  ~ `bool`



---

## class `SupportsAdd`

Instances of this protocol supports the homogeneous `+` operation.

### Bases

- `Protocol`

### Members

#### abstract instancemethod `__add__[TSelf](__o)`

Constraint
  ~ *self*: `TSelf`

Parameters
  ~ *__o* (`TSelf`)

Returns
  ~ `TSelf`



