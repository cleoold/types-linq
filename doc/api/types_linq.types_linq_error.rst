module ``types_linq.types_linq_error``
#######################################

class ``TypesLinqError``
**************************

Types-linq has run into problems.

Bases
======
- ``Exception``

Members
========

class ``InvalidOperationError``
*********************************

Exception raised when a call is invalid for the object's current state.

Bases
======
- ``TypesLinqError``
- ``ValueError``

Members
========

class ``IndexOutOfRangeError``
********************************

An `IndexError` with types-linq flavour.

Bases
======
- ``TypesLinqError``
- ``IndexError``

Members
========

