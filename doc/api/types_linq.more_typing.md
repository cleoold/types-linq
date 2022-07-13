# module ``types_linq.more_typing``

Typing utilities used by methods's declarations across the library. For more details, see
[`typing`](https://docs.python.org/3/library/typing.html).
```{note} Definitions in this module are for documenting purposes only.
```

## Constants

(apiref.TAccumulate)=
### `TAccumulate`

Equals
  ~ `TypeVar('`[`TAccumulate`](apiref.TAccumulate)`')`

A generic type parameter.

---

(apiref.TAverage_co)=
### `TAverage_co`

Equals
  ~ `TypeVar('`[`TAverage_co`](apiref.TAverage_co)`', covariant=True)`

A generic covariant type parameter.

---

(apiref.TCollection)=
### `TCollection`

Equals
  ~ `TypeVar('`[`TCollection`](apiref.TCollection)`')`

A generic type parameter.

---

(apiref.TDefault)=
### `TDefault`

Equals
  ~ `TypeVar('`[`TDefault`](apiref.TDefault)`')`

A generic type parameter.

---

(apiref.TInner)=
### `TInner`

Equals
  ~ `TypeVar('`[`TInner`](apiref.TInner)`')`

A generic type parameter.

---

(apiref.TKey)=
### `TKey`

Equals
  ~ `TypeVar('`[`TKey`](apiref.TKey)`')`

A generic type parameter.

---

(apiref.TKey2)=
### `TKey2`

Equals
  ~ `TypeVar('`[`TKey2`](apiref.TKey2)`')`

A generic type parameter.

---

(apiref.TKey_co)=
### `TKey_co`

Equals
  ~ `TypeVar('`[`TKey_co`](apiref.TKey_co)`', covariant=True)`

A generic covariant type parameter.

---

(apiref.TOther)=
### `TOther`

Equals
  ~ `TypeVar('`[`TOther`](apiref.TOther)`')`

A generic type parameter.

---

(apiref.TOther2)=
### `TOther2`

Equals
  ~ `TypeVar('`[`TOther2`](apiref.TOther2)`')`

A generic type parameter.

---

(apiref.TOther3)=
### `TOther3`

Equals
  ~ `TypeVar('`[`TOther3`](apiref.TOther3)`')`

A generic type parameter.

---

(apiref.TOther4)=
### `TOther4`

Equals
  ~ `TypeVar('`[`TOther4`](apiref.TOther4)`')`

A generic type parameter.

---

(apiref.TResult)=
### `TResult`

Equals
  ~ `TypeVar('`[`TResult`](apiref.TResult)`')`

A generic type parameter.

---

(apiref.TSelf)=
### `TSelf`

Equals
  ~ `TypeVar('`[`TSelf`](apiref.TSelf)`')`

A generic type parameter.

---

(apiref.TSource)=
### `TSource`

Equals
  ~ `TypeVar('`[`TSource`](apiref.TSource)`')`

A generic type parameter.

---

(apiref.TSource_co)=
### `TSource_co`

Equals
  ~ `TypeVar('`[`TSource_co`](apiref.TSource_co)`', covariant=True)`

A generic covariant type parameter.

---

(apiref.TValue)=
### `TValue`

Equals
  ~ `TypeVar('`[`TValue`](apiref.TValue)`')`

A generic type parameter.

---

(apiref.TValue_co)=
### `TValue_co`

Equals
  ~ `TypeVar('`[`TValue_co`](apiref.TValue_co)`', covariant=True)`

A generic covariant type parameter.

---

(apiref.TSupportsLessThan)=
### `TSupportsLessThan`

Equals
  ~ `TypeVar('`[`TSupportsLessThan`](apiref.TSupportsLessThan)`', bound=`[`SupportsLessThan`](apiref.SupportsLessThan)`)`

A generic type parameter that represents a type that [`SupportsLessThan`](apiref.SupportsLessThan).

---

(apiref.TSupportsAdd)=
### `TSupportsAdd`

Equals
  ~ `TypeVar('`[`TSupportsAdd`](apiref.TSupportsAdd)`', bound=`[`SupportsAdd`](apiref.SupportsAdd)`)`

A generic type parameter that represents a type that [`SupportsAdd`](apiref.SupportsAdd).

---

(apiref.SupportsAverage)=
## class `SupportsAverage[TAverage_co]`

Instances of this protocol supports the averaging operation. that is, if `x` is such an instance,
and `N` is an integer, then `(x + x + ...) / N` is allowed, and has the type [`TAverage_co`](apiref.TAverage_co).

### Bases

- `Protocol[`[`TAverage_co`](apiref.TAverage_co)`]`

### Members

#### abstract instancemethod `__add__[TSelf](__o)`

Constraint
  ~ *self*: [`TSelf`](apiref.TSelf)

Parameters
  ~ *__o*: [`TSelf`](apiref.TSelf)

Returns
  ~ [`TSelf`](apiref.TSelf)



---

#### abstract instancemethod `__truediv__(__o)`

Parameters
  ~ *__o*: `int`

Returns
  ~ [`TAverage_co`](apiref.TAverage_co)



---

(apiref.SupportsLessThan)=
## class `SupportsLessThan`

Instances of this protocol supports the `<` operation.

Even though they may be unimplemented, the existence of `<` implies the existence of `>`,
and probably `==`, `!=`, `<=` and `>=`.

### Bases

- `Protocol`

### Members

#### abstract instancemethod `__lt__(__o)`

Parameters
  ~ *__o*: `Any`

Returns
  ~ `bool`



---

(apiref.SupportsAdd)=
## class `SupportsAdd`

Instances of this protocol supports the homogeneous `+` operation.

### Bases

- `Protocol`

### Members

#### abstract instancemethod `__add__[TSelf](__o)`

Constraint
  ~ *self*: [`TSelf`](apiref.TSelf)

Parameters
  ~ *__o*: [`TSelf`](apiref.TSelf)

Returns
  ~ [`TSelf`](apiref.TSelf)



