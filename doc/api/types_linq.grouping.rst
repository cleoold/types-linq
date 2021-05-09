module ``types_linq.grouping``
###############################

class ``Grouping[TValue_co, TKey_co]``
****************************************

.. code-block:: python

    from types_linq.grouping import Grouping

Represents a collection of objects that have a common key.

Users should not construct instances of this class directly. Use ``Enumerable.group_by()`` instead.

Bases
======
- ``Enumerable[TValue_co]``
- ``Generic[TKey_co, TValue_co]``

Members
========
instanceproperty ``key``
--------------------------

Returns
  - ``TKey_co``

Gets the key of the grouping.


