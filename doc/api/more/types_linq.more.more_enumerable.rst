module ``types_linq.more.more_enumerable``
###########################################

class ``MoreEnumerable[TSource_co]``
**************************************

.. code-block:: python

    from types_linq.more import MoreEnumerable

MoreEnumerable provides more query methods. Instances of this class can be created by directly
constructing, using as_more(), or invoking MoreEnumerable methods that return MoreEnumerable
instead of Enumerable.

Some APIs are subject to change as updates to .NET (6) are happening - they will move to Enumerable
class if one day they appear in the official .NET doc.

Bases
======
- ``Enumerable[TSource_co]``

Members
========
instancemethod ``aggregate_right[TAccumulate, TResult](__seed, __func, __result_selector)``
---------------------------------------------------------------------------------------------

Parameters
  - `__seed` (``TAccumulate``)
  - `__func` (``Callable[[TAccumulate, TSource_co], TAccumulate]``)
  - `__result_selector` (``Callable[[TAccumulate], TResult]``)

Returns
  - ``TResult``

Applies a right-associative accumulator function over the sequence. The seed is used as
the initial accumulator value, and the result_selector is used to select the result value.

----

instancemethod ``aggregate_right[TAccumulate](__seed, __func)``
-----------------------------------------------------------------

Parameters
  - `__seed` (``TAccumulate``)
  - `__func` (``Callable[[TAccumulate, TSource_co], TAccumulate]``)

Returns
  - ``TAccumulate``

Applies a right-associative accumulator function over the sequence. The seed is used as the
initial accumulator value.

----

instancemethod ``aggregate_right[TAccumulate](__func)``
---------------------------------------------------------

Parameters
  - `__func` (``Callable[[TAccumulate, TSource_co], TAccumulate]``)

Returns
  - ``TAccumulate``

Applies a right-associative accumulator function over the sequence. Raises `InvalidOperationError`
if there is no value in the sequence.

Example
    >>> things = [4, 16, 'x', object(), 'uv']
    >>> MoreEnumerable(things).aggregate_right(lambda e, rr: f'(cons {repr(e)} {rr})')
    '(cons 4 (cons 16 (cons 'x' (cons <object object at 0x000000000B000000> 'uv'))))'

----

instancemethod ``as_more()``
------------------------------


Returns
  - ``MoreEnumerable[TSource_co]``

Returns the original MoreEnumerable reference.

----

instancemethod ``distinct_by(key_selector)``
----------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], object]``)

Returns
  - ``MoreEnumerable[TSource_co]``

Returns distinct elements from the sequence where "distinctness" is determined by the value
returned by the selector.

Example
    >>> ints = [1, 4, 5, 6, 4, 3, 1, 99]
    >>> MoreEnumerable(ints).distinct_by(lambda x: x // 2).to_list()
    [1, 4, 6, 3, 99]

----

instancemethod ``enumerate(start=0)``
---------------------------------------

Parameters
  - `start` (``int``)

Returns
  - ``MoreEnumerable[Tuple[int, TSource_co]]``

Returns a sequence of tuples containing the index and the value from the source sequence. `start`
is used to specify the starting index.

Example
    >>> ints = [2, 4, 6]
    >>> MoreEnumerable(ints).enumerate().to_list()
    [(0, 2), (1, 4), (2, 6)]

----

instancemethod ``except_by(second, key_selector)``
----------------------------------------------------

Parameters
  - `second` (``Iterable[TSource_co]``)
  - `key_selector` (``Callable[[TSource_co], object]``)

Returns
  - ``MoreEnumerable[TSource_co]``

Produces the set difference of two sequences: self - second, according to a key selector that
determines "distinctness". Note the second iterable is homogenous to self.

Example
    >>> first = [(16, 'x'), (9, 'y'), (12, 'd'), (16, 't')]
    >>> second = [(24, 'd'), (77, 'y')]
    >>> MoreEnumerable(first).except_by(second, lambda x: x[1]).to_list()
    [(16, 'x'), (16, 't')]

----

instancemethod ``flatten()``
------------------------------


Returns
  - ``MoreEnumerable[Any]``

Flattens the sequence containing arbitrarily-nested subsequences.

Note: the nested objects must be Iterable to be flatten.
Instances of `str` or `bytes` are not flattened.

Example
    >>> lst = ['apple', ['orange', ['juice', 'mango'], 'delta function']]
    >>> MoreEnumerable(lst).flatten().to_list()
    ['apple', 'orange', 'juice', 'mango', 'delta function']

----

instancemethod ``flatten(__predicate)``
-----------------------------------------

Parameters
  - `__predicate` (``Callable[[Iterable[Any]], bool]``)

Returns
  - ``MoreEnumerable[Any]``

Flattens the sequence containing arbitrarily-nested subsequences. A predicate function determines
whether a nested iterable should be flattened or not.

Note: the nested objects must be Iterable to be flatten.

----

instancemethod ``flatten2(selector)``
---------------------------------------

Parameters
  - `selector` (``Callable[[Any], Optional[Iterable[object]]]``)

Returns
  - ``MoreEnumerable[Any]``

Flattens the sequence containing arbitrarily-nested subsequences. A selector is used to select a
subsequence based on the object's properties. If the selector returns None, then the object is
considered a leaf.

----

instancemethod ``for_each(action)``
-------------------------------------

Parameters
  - `action` (``Callable[[TSource_co], object]``)

Returns
  - ``None``

Executes the given function on each element in the source sequence. The return values are discarded.

Example
    .. code-block:: python

        >>> def gen():
        ...     yield 116; yield 35; yield -9

        >>> Enumerable(gen()).where(lambda x: x > 0).as_more().for_each(print)
        116
        35

----

instancemethod ``for_each2(action)``
--------------------------------------

Parameters
  - `action` (``Callable[[TSource_co, int], object]``)

Returns
  - ``None``

Executes the given function on each element in the source sequence. Each element's index is used in
the logic of the function. The return values are discarded.

----

instancemethod ``interleave(*iters)``
---------------------------------------

Parameters
  - `*iters` (``Iterable[TSource_co]``)

Returns
  - ``MoreEnumerable[TSource_co]``

Interleaves the elements of two or more sequences into a single sequence, skipping sequences if they
are consumed.

Example
    >>> MoreEnumerable(['1', '2']).interleave(['4', '5', '6'], ['7', '8', '9']).to_list()
    ['1', '4', '7', '2', '5', '8', '6', '9']

----

instancemethod ``maxima_by[TSupportsLessThan](selector)``
-----------------------------------------------------------

Parameters
  - `selector` (``Callable[[TSource_co], TSupportsLessThan]``)

Returns
  - ``ExtremaEnumerable[TSource_co, TSupportsLessThan]``

Returns the maximal elements of the sequence based on the given selector.

Example
    >>> strings = ['foo', 'bar', 'cheese', 'orange', 'baz', 'spam', 'egg', 'toasts', 'dish']
    >>> MoreEnumerable(strings).maxima_by(len).to_list()
    ['cheese', 'orange', 'toasts']
    >>> MoreEnumerable(strings).maxima_by(lambda x: x.count('e')).first()
    'cheese'

----

instancemethod ``maxima_by[TKey](selector, __comparer)``
----------------------------------------------------------

Parameters
  - `selector` (``Callable[[TSource_co], TKey]``)
  - `__comparer` (``Callable[[TKey, TKey], int]``)

Returns
  - ``ExtremaEnumerable[TSource_co, TKey]``

Returns the maximal elements of the sequence based on the given selector and the comparer.

Such comparer takes two values and return positive ints when lhs > rhs, negative ints
if lhs < rhs, and 0 if they are equal.

----

instancemethod ``minima_by[TSupportsLessThan](selector)``
-----------------------------------------------------------

Parameters
  - `selector` (``Callable[[TSource_co], TSupportsLessThan]``)

Returns
  - ``ExtremaEnumerable[TSource_co, TSupportsLessThan]``

Returns the minimal elements of the sequence based on the given selector.

----

instancemethod ``minima_by[TKey](selector, __comparer)``
----------------------------------------------------------

Parameters
  - `selector` (``Callable[[TSource_co], TKey]``)
  - `__comparer` (``Callable[[TKey, TKey], int]``)

Returns
  - ``ExtremaEnumerable[TSource_co, TKey]``

Returns the minimal elements of the sequence based on the given selector and the comparer.

Such comparer takes two values and return positive ints when lhs > rhs, negative ints
if lhs < rhs, and 0 if they are equal.

----

instancemethod ``pipe(action)``
---------------------------------

Parameters
  - `action` (``Callable[[TSource_co], object]``)

Returns
  - ``MoreEnumerable[TSource_co]``

Executes the given action on each element in the sequence and yields it. Return values of
action are discarded.

Example
    >>> store = set()
    >>> MoreEnumerable([1, 2, 2, 1]).pipe(store.add).where(lambda x: x % 2 == 0).to_list()
    [2, 2]
    >>> store
    {1, 2}

----

staticmethod ``traverse_breath_first[TSource](root, children_selector)``
--------------------------------------------------------------------------

Parameters
  - `root` (``TSource``)
  - `children_selector` (``Callable[[TSource], Iterable[TSource]]``)

Returns
  - ``MoreEnumerable[TSource]``

Traverses the tree (graph) from the root node in a breath-first fashion. A selector is used to
select children of each node.

Graphs are not checked for cycles. If the resulting sequence needs to be finite then it is the
responsibility of children_selector to ensure that duplicate nodes are not visited.

----

staticmethod ``traverse_depth_first[TSource](root, children_selector)``
-------------------------------------------------------------------------

Parameters
  - `root` (``TSource``)
  - `children_selector` (``Callable[[TSource], Iterable[TSource]]``)

Returns
  - ``MoreEnumerable[TSource]``

Traverses the tree (graph) from the root node in a depth-first fashion. A selector is used to
select children of each node.

Graphs are not checked for cycles. If the resulting sequence needs to be finite then it is the
responsibility of children_selector to ensure that duplicate nodes are not visited.


