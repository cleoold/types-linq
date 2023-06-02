# module ``types_linq.more.more_enums``

(apiref.RankMethods)=
## class `RankMethods`

```py
from types_linq.more import RankMethods
```

Enumeration to select different methods of assigning rankings when breaking
[ties](https://en.wikipedia.org/wiki/Ranking#Strategies_for_assigning_rankings).

Revisions
    ~ v1.2.1: New.

### Bases

- `Enum`

### Fields

#### `dense`

Equals
  ~ `auto()`

Items that compare equally receive the same ranking, and the next items get the immediately
following ranking. *(1223)*

---

#### `competitive`

Equals
  ~ `auto()`

Items that compare equally receive the same highest ranking, and gaps are left out. *(1224)*

---

#### `ordinal`

Equals
  ~ `auto()`

Each item receives unique rankings. *(1234)*

