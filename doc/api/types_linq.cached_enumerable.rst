module ``types_linq.cached_enumerable``
########################################

class ``CachedEnumerable[TSource_co]``
****************************************

.. code-block:: python

    from types_linq.cached_enumerable import CachedEnumerable

Enumerable that stores the enumerated results which can be accessed repeatedly.

Users should not construct instances of this class directly. Use ``Enumerable.as_cached()`` instead.

Revisions:
    - v0.1.1: New.

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

Updates settings and returns the original CachedEnumerable reference.

Raises `InvalidOperationError` if cache_capacity is negative.


