# module ``types_linq.types_linq_error``

(apiref.TypesLinqError)=
## class `TypesLinqError`

```py
from types_linq import TypesLinqError
```

Types-linq has run into problems.

### Bases

- `Exception`

---

(apiref.InvalidOperationError)=
## class `InvalidOperationError`

```py
from types_linq import InvalidOperationError
```

Exception raised when a call is invalid for the object's current state.

### Bases

- [`TypesLinqError`](apiref.TypesLinqError)
- `ValueError`

---

(apiref.IndexOutOfRangeError)=
## class `IndexOutOfRangeError`

```py
from types_linq import IndexOutOfRangeError
```

An `IndexError` with types-linq flavour.

### Bases

- [`TypesLinqError`](apiref.TypesLinqError)
- `IndexError`

