# module ``types_linq.types_linq_error``

## class `TypesLinqError`

```py
from types_linq import TypesLinqError
```

Types-linq has run into problems.

### Bases

- `Exception`

---

## class `InvalidOperationError`

```py
from types_linq import InvalidOperationError
```

Exception raised when a call is invalid for the object's current state.

### Bases

- `TypesLinqError`
- `ValueError`

---

## class `IndexOutOfRangeError`

```py
from types_linq import IndexOutOfRangeError
```

An `IndexError` with types-linq flavour.

### Bases

- `TypesLinqError`
- `IndexError`

