module ``types_linq.ordered_enumerable``
#########################################

class ``OrderedEnumerable[TSource_co, TKey]``
***********************************************

Represents a sorted Enumerable sequence that is sorted by some key.

Bases
======
- ``Enumerable[TSource_co]``
- ``Generic[TSource_co, TKey]``

Members
========
instancemethod ``create_ordered_enumerable[TKey2](key_selector, comparer, descending)``
-----------------------------------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey2]``)
  - `comparer` (``Optional[Callable[[TKey2], int]]``)
  - `descending` (``bool``)

Returns
  - ``OrderedEnumerable[TSource_co, TKey2]``

Performs a subsequent ordering on the elements of the sequence according to a key.

----

instancemethod ``then_by[TSupportsLessThan](key_selector)``
-------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TSupportsLessThan]``)

Returns
  - ``OrderedEnumerable[TSource_co, TSupportsLessThan]``

Performs a subsequent ordering of the elements in ascending order according to key.

----

instancemethod ``then_by[TKey2](key_selector, __comparer)``
-------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey2]``)
  - `__comparer` (``Callable[[TKey2, TKey2], int]``)

Returns
  - ``OrderedEnumerable[TSource_co, TKey2]``

Performs a subsequent ordering of the elements in ascending order by using a specified comparer.

----

instancemethod ``then_by_descending[TSupportsLessThan](key_selector)``
------------------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TSupportsLessThan]``)

Returns
  - ``OrderedEnumerable[TSource_co, TSupportsLessThan]``

Performs a subsequent ordering of the elements in descending order according to key.

----

instancemethod ``then_by_descending[TKey2](key_selector, __comparer)``
------------------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey2]``)
  - `__comparer` (``Callable[[TKey2, TKey2], int]``)

Returns
  - ``OrderedEnumerable[TSource_co, TKey2]``

Performs a subsequent ordering of the elements in descending order by using a specified comparer.


