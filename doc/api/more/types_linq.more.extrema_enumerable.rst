module ``types_linq.more.extrema_enumerable``
##############################################

class ``ExtremaEnumerable[TSource_co, TKey]``
***********************************************

.. code-block:: python

    from types_linq.more.extrema_enumerable import ExtremaEnumerable

Specialization for manipulating extrema.

Users should not construct instances of this class directly. Use ``MoreEnumerable.maxima_by()``
instead.

Bases
======
- ``MoreEnumerable[TSource_co]``
- ``Generic[TSource_co, TKey]``

Members
========
instancemethod ``take(count)``
--------------------------------

Parameters
  - `count` (``int``)

Returns
  - ``MoreEnumerable[TSource_co]``

Returns a specified number of contiguous elements from the start of the sequence.

----

instancemethod ``take_last(count)``
-------------------------------------

Parameters
  - `count` (``int``)

Returns
  - ``MoreEnumerable[TSource_co]``

Returns a new sequence that contains the last `count` elements.


