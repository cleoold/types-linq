module ``types_linq.grouping``
###############################

class ``Grouping[TValue_co, TKey_co]``
****************************************

Represents a collection of objects that have a common key.

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


