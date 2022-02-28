module ``types_linq.more.more_enumerable``
###########################################

class ``MoreEnumerable[TSource_co]``
**************************************

.. code-block:: python

    from types_linq.more import MoreEnumerable

MoreEnumerable provides more query methods. Instances of this class can be created by directly
constructing, using as_more(), or invoking MoreEnumerable methods that return MoreEnumerable
instead of Enumerable.

These APIs may have breaking changes more frequently than those in Enumerable class because updates
in .NET are happening and sometimes ones of these APIs could be moved to Enumerable with modification,
or changed to accommodate changes to Enumerable.

Revisions:
    - v0.2.0: New.

Bases
======
- ``Enumerable[TSource_co]``

Members
========
instancemethod ``aggregate_right[TAccumulate, TResult](__seed, __func, __result_selector)``
---------------------------------------------------------------------------------------------

Parameters
  - `__seed` (``TAccumulate``)
  - `__func` (``Callable[[TSource_co, TAccumulate], TAccumulate]``)
  - `__result_selector` (``Callable[[TAccumulate], TResult]``)

Returns
  - ``TResult``

Applies a right-associative accumulator function over the sequence. The seed is used as
the initial accumulator value, and the result_selector is used to select the result value.

Revisions:
    - main: Fixed annotation for __func.

----

instancemethod ``aggregate_right[TAccumulate](__seed, __func)``
-----------------------------------------------------------------

Parameters
  - `__seed` (``TAccumulate``)
  - `__func` (``Callable[[TSource_co, TAccumulate], TAccumulate]``)

Returns
  - ``TAccumulate``

Applies a right-associative accumulator function over the sequence. The seed is used as the
initial accumulator value.

Example:
    >>> values = [9, 4, 2]
    >>> MoreEnumerable(values).aggregate_right('null', lambda e, rr: f'(cons {e} {rr})')
    '(cons 9 (cons 4 (cons 2 null)))'

Revisions:
    - main: Fixed annotation for __func.

----

instancemethod ``aggregate_right(__func)``
--------------------------------------------

Parameters
  - `__func` (``Callable[[TSource_co, TSource_co], TSource_co]``)

Returns
  - ``TSource_co``

Applies a right-associative accumulator function over the sequence. Raises `InvalidOperationError`
if there is no value in the sequence.

Example
    >>> values = ['9', '4', '2', '5']
    >>> MoreEnumerable(values).aggregate_right(lambda e, rr: f'({e}+{rr})')
    '(9+(4+(2+5)))'

Revisions:
    - main: Fixed annotation for __func.

----

instancemethod ``as_more()``
------------------------------


Returns
  - ``MoreEnumerable[TSource_co]``

Returns the original MoreEnumerable reference.

----

instancemethod ``consume()``
------------------------------


Returns
  - ``None``

Consumes the sequence completely. This method iterates the sequence immediately and does not save
any intermediate data.

Revisions:
    - v1.1.0: New.

----

instancemethod ``cycle(count=None)``
--------------------------------------

Parameters
  - `count` (``Optional[int]``)

Returns
  - ``MoreEnumerable[TSource_co]``

Repeats the sequence `count` times.

If `count` is `None`, the sequence is infinite. Raises `InvalidOperationError` if `count`
is negative.

Example
    >>> MoreEnumerable([1, 2, 3]).cycle(3).to_list()
    [1, 2, 3, 1, 2, 3, 1, 2, 3]

Revisions:
    - v1.1.0: New.

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

Revisions:
    - v1.0.0: New.

----

instancemethod ``except_by2(second, key_selector)``
-----------------------------------------------------

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
    >>> MoreEnumerable(first).except_by2(second, lambda x: x[1]).to_list()
    [(16, 'x'), (16, 't')]

Revisions:
    - v1.0.0: Renamed from ``except_by()`` to this name to accommodate the update to Enumerable class.
    - v0.2.1: Added preliminary support for unhashable keys.

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

Revisions:
    - v0.2.1: New.

----

instancemethod ``pre_scan[TAccumulate](identity, transformation)``
--------------------------------------------------------------------

Parameters
  - `identity` (``TAccumulate``)
  - `transformation` (``Callable[[TAccumulate, TSource_co], TAccumulate]``)

Returns
  - ``MoreEnumerable[TAccumulate]``

Performs a pre-scan (exclusive prefix sum) over the sequence. Such scan returns an
equal-length sequence where the first element is the identity, and i-th element (i>1) is
the sum of the first i-1 (and identity) elements in the original sequence.

Example
    >>> values = [9, 4, 2, 5, 7]
    >>> MoreEnumerable(values).pre_scan(0, lambda acc, e: acc + e).to_list()
    [0, 9, 13, 15, 20]
    >>> MoreEnumerable([]).pre_scan(0, lambda acc, e: acc + e).to_list()
    []

Revisions:
    - main: New.

----

instancemethod ``rank[TSupportsLessThan]()``
----------------------------------------------

Constraint
  - `self`: ``MoreEnumerable[TSupportsLessThan]``

Returns
  - ``MoreEnumerable[int]``

Ranks each item in the sequence in descending order.

Example
    >>> scores = [1, 4, 77, 23, 23, 4, 9, 0, -7, 101, 23]
    >>> MoreEnumerable(scores).rank().to_list()
    [6, 5, 2, 3, 3, 5, 4, 7, 8, 1, 3]  # 101 is largest, so has rank of 1

Revisions:
    - v1.0.0: New.

----

instancemethod ``rank(__comparer)``
-------------------------------------

Parameters
  - `__comparer` (``Callable[[TSource_co, TSource_co], int]``)

Returns
  - ``MoreEnumerable[int]``

Ranks each item in the sequence in descending order using the given comparer.

Such comparer takes two values and return positive ints when lhs > rhs, negative ints
if lhs < rhs, and 0 if they are equal.

Revisions:
    - v1.0.0: New.

----

instancemethod ``rank_by[TSupportsLessThan](key_selector)``
-------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TSupportsLessThan]``)

Returns
  - ``MoreEnumerable[int]``

Ranks each item in the sequence in descending order using the given selector.

Example
    .. code-block:: python

        >>> scores = [
        ...     {'name': 'Frank', 'score': 75},
        ...     {'name': 'Alica', 'score': 90},
        ...     {'name': 'Erika', 'score': 99},
        ...     {'name': 'Rogers', 'score': 90},
        ... ]

        >>> MoreEnumerable(scores).rank_by(lambda x: x['score']) \
        ...     .zip(scores) \
        ...     .group_by(lambda t: t[0], lambda t: t[1]['name']) \
        ...     .to_dict(lambda g: g.key, lambda g: g.to_list())
        {3: ['Frank'], 2: ['Alica', 'Rogers'], 1: ['Erika']}

Revisions:
    - v1.0.0: New.

----

instancemethod ``rank_by[TKey](key_selector, __comparer)``
------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey]``)
  - `__comparer` (``Callable[[TKey, TKey], int]``)

Returns
  - ``MoreEnumerable[int]``

Ranks each item in the sequence in descending order using the given selector and comparer.

Such comparer takes two values and return positive ints when lhs > rhs, negative ints
if lhs < rhs, and 0 if they are equal.

Revisions:
    - v1.0.0: New.

----

instancemethod ``run_length_encode()``
----------------------------------------


Returns
  - ``MoreEnumerable[Tuple[TSource_co, int]]``

Run-length encodes the sequence into a sequence of tuples where each tuple contains an
(the first) element and its number of contingent occurrences, where equality is based on
`==`.

Example
    >>> MoreEnumerable('abbcaeeeaa').run_length_encode().to_list()
    [('a', 1), ('b', 2), ('c', 1), ('a', 1), ('e', 3), ('a', 2)]

Revisions:
    - v1.1.0: New.

----

instancemethod ``run_length_encode(__comparer)``
--------------------------------------------------

Parameters
  - `__comparer` (``Callable[[TSource_co, TSource_co], bool]``)

Returns
  - ``MoreEnumerable[Tuple[TSource_co, int]]``

Run-length encodes the sequence into a sequence of tuples where each tuple contains an
(the first) element and its number of contingent occurrences, where equality is determined by
the comparer.

Example
    >>> MoreEnumerable('abBBbcaEeeff') \
    >>>     .run_length_encode(lambda x, y: x.lower() == y.lower()).to_list()
    [('a', 1), ('b', 4), ('c', 1), ('a', 1), ('E', 3), ('f', 2)]

Revisions:
    - v1.1.0: New.

----

instancemethod ``scan(__transformation)``
-------------------------------------------

Parameters
  - `__transformation` (``Callable[[TSource_co, TSource_co], TSource_co]``)

Returns
  - ``MoreEnumerable[TSource_co]``

Performs a inclusive prefix sum over the sequence. Such scan returns an equal-length sequence
where the i-th element is the sum of the first i elements in the original sequence.

Example
    >>> values = [9, 4, 2, 5, 7]
    >>> MoreEnumerable(values).scan(lambda acc, e: acc + e).to_list()
    [9, 13, 15, 20, 27]
    >>> MoreEnumerable([]).scan(lambda acc, e: acc + e).to_list()
    []

Example
    >>> # running max
    >>> fruits = ['apple', 'mango', 'orange', 'passionfruit', 'grape']
    >>> MoreEnumerable(fruits).scan(lambda acc, e: e if len(e) > len(acc) else acc).to_list()
    ['apple', 'apple', 'orange', 'passionfruit', 'passionfruit']

Revisions:
    - main: New.

----

instancemethod ``scan[TAccumulate](__seed, __transformation)``
----------------------------------------------------------------

Parameters
  - `__seed` (``TAccumulate``)
  - `__transformation` (``Callable[[TAccumulate, TSource_co], TAccumulate]``)

Returns
  - ``MoreEnumerable[TAccumulate]``

Like Enumerable.aggregate(seed, transformation) except that the intermediate results are
included in the result sequence.

Example
    >>> Enumerable.range(1, 5).as_more().scan(-1, lambda acc, e: acc * e).to_list()
    [-1, -1, -2, -6, -24, -120]

Revisions:
    - main: New.

----

instancemethod ``scan_right(__func)``
---------------------------------------

Parameters
  - `__func` (``Callable[[TSource_co, TSource_co], TSource_co]``)

Returns
  - ``MoreEnumerable[TSource_co]``

Performs a right-associative inclusive prefix sum over the sequence. This is the
right-associative version of MoreEnumerable.scan(func).

Example
    >>> values = ['9', '4', '2', '5']
    >>> MoreEnumerable(values).scan_right(lambda e, rr: f'({e}+{rr})').to_list()
    ['(9+(4+(2+5)))', '(4+(2+5))', '(2+5)', '5']
    >>> MoreEnumerable([]).scan_right(lambda e, rr: e + rr).to_list()
    []

Revisions:
    - main: New.

----

instancemethod ``scan_right[TAccumulate](__seed, __func)``
------------------------------------------------------------

Parameters
  - `__seed` (``TAccumulate``)
  - `__func` (``Callable[[TSource_co, TAccumulate], TAccumulate]``)

Returns
  - ``MoreEnumerable[TAccumulate]``

The right-associative version of MoreEnumerable.scan(seed, func).

Example
    >>> values = [9, 4, 2]
    >>> MoreEnumerable(values).scan_right('null', lambda e, rr: f'(cons {e} {rr})').to_list()
    ['(cons 9 (cons 4 (cons 2 null)))', '(cons 4 (cons 2 null))', '(cons 2 null)', 'null']

Revisions:
    - main: New.

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


