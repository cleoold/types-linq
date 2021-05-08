module ``types_linq.cached_enumerable``
########################################

class ``CachedEnumerable[TSource_co]``
****************************************

Enumerable that stores the enumerated results which can be accessed repeatedly.

Bases
======
- ``Enumerable[TSource_co]``

Members
========
instancemethod ``as_cached(*, cache_capacity=None)``
------------------------------------------------------

Parameters
  - `cache_capacity` (``Optional[int]``)

Returns
  - ``CachedEnumerable[TSource_co]``

Updates settings and returns the original Enumerable reference.

Raises `InvalidOperationError` if cache_capacity is negative.


