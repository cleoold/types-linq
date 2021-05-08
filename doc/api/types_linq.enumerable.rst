module ``types_linq.enumerable``
#################################

class ``Enumerable[TSource_co]``
**********************************

Provides a set of helper methods for querying iterable objects.

Bases
======
- ``Sequence[TSource_co]``
- ``Generic[TSource_co]``

Members
========
instancemethod ``__init__(__iterable)``
-----------------------------------------

Parameters
  - `__iterable` (``Iterable[TSource_co]``)

Returns
  - ``None``

Wraps an iterable.

----

instancemethod ``__init__(__iterable_factory)``
-------------------------------------------------

Parameters
  - `__iterable_factory` (``Callable[[], Iterable[TSource_co]]``)

Returns
  - ``None``

Wraps an iterable returned from the iterable factory. The factory will be called whenever
an enumerating operation is performed.

----

instancemethod ``__contains__(value)``
----------------------------------------

Parameters
  - `value` (``object``)

Returns
  - ``bool``

Tests whether the sequence contains the specified element. Prefers calling `__contains__()`
on the wrapped iterable if available, otherwise, calls `self.contains()`.

----

instancemethod ``__getitem__(index)``
---------------------------------------

Parameters
  - `index` (``int``)

Returns
  - ``TSource_co``

Returns the element at specified index in the sequence. Prefers calling `__getitem__()` on the
wrapped iterable if available, otherwise, calls `self.element_at()`.

----

instancemethod ``__getitem__(index)``
---------------------------------------

Parameters
  - `index` (``slice``)

Returns
  - ``Enumerable[TSource_co]``

Produces a subsequence defined by the given slice notation. Prefers calling `__getitem__()` on the
wrapped iterable if available, otherwise, calls `self.elements_in()`.

----

instancemethod ``__iter__()``
-------------------------------


Returns
  - ``Iterator[TSource_co]``

Returns an iterator that enumerates the values in the sequence.

----

instancemethod ``__len__()``
------------------------------


Returns
  - ``int``

Returns the number of elements in the sequence. Prefers calling `__len__()` on the wrapped iterable
if available, otherwise, calls `self.count()`.

----

instancemethod ``__reversed__()``
-----------------------------------


Returns
  - ``Iterator[TSource_co]``

Inverts the order of the elements in the sequence. Prefers calling `__reversed__()` on the wrapped
iterable if available, otherwise, calls `self.reverse()`.

----

instancemethod ``aggregate[TAccumulate, TResult](__seed, __func, __result_selector)``
---------------------------------------------------------------------------------------

Parameters
  - `__seed` (``TAccumulate``)
  - `__func` (``Callable[[TAccumulate, TSource_co], TAccumulate]``)
  - `__result_selector` (``Callable[[TAccumulate], TResult]``)

Returns
  - ``TResult``

Applies an accumulator function over the sequence. The seed is used as the initial
accumulator value, and the result_selector is used to select the result value.

----

instancemethod ``aggregate[TAccumulate](__seed, __func)``
-----------------------------------------------------------

Parameters
  - `__seed` (``TAccumulate``)
  - `__func` (``Callable[[TAccumulate, TSource_co], TAccumulate]``)

Returns
  - ``TAccumulate``

Applies an accumulator function over the sequence. The seed is used as the initial
accumulator value

----

instancemethod ``aggregate[TAccumulate](__func)``
---------------------------------------------------

Parameters
  - `__func` (``Callable[[TAccumulate, TSource_co], TAccumulate]``)

Returns
  - ``TAccumulate``

Applies an accumulator function over the sequence. Raises `InvalidOperationError` if
there is no value in the sequence.

----

instancemethod ``all(predicate)``
-----------------------------------

Parameters
  - `predicate` (``Callable[[TSource_co], bool]``)

Returns
  - ``bool``

Tests whether all elements of the sequence satisfy a condition.

----

instancemethod ``any()``
--------------------------


Returns
  - ``bool``

Tests whether the sequence has any elements.

----

instancemethod ``any(__predicate)``
-------------------------------------

Parameters
  - `__predicate` (``Callable[[TSource_co], bool]``)

Returns
  - ``bool``

Tests whether any element of the sequence satisfy a condition.

----

instancemethod ``append(element)``
------------------------------------

Parameters
  - `element` (``TSource_co``)

Returns
  - ``Enumerable[TSource_co]``

Appends a value to the end of the sequence.

----

instancemethod ``as_cached(*, cache_capacity=None)``
------------------------------------------------------

Parameters
  - `cache_capacity` (``Optional[int]``)

Returns
  - ``CachedEnumerable[TSource_co]``

Returns a CachedEnumerable to cache the enumerated results in this query so that if the wrapped
iterable is not repeatable (e.g. generator object), it will be repeatable.

By default, `Enumerable`s constructed from nonrepeatable sources cannot be enumerated multiple
times, for example
```py
def gen():
    yield 1
    yield 0
    yield 3

query = Enumerable(gen())
print(query.count())
print(query.where(lambda x: x > 0).to_list())
```
prints `3` followed by an empty list `[]`. This is because the `.count()` exhausts the contents
in the generator before the second query is run.

To avoid the issue, use this method which saves the results along the way.
```py
query = Enumerable(gen()).as_cached()
print(query.count())
print(query.take(2).to_list())
print(query.where(lambda x: x > 0).to_list())
```
printing `3`, `[1, 0]` and `[1, 3]`.

This is an alternative way to deal with non-repeatable sources other than passing function
(`query = Enumerable(gen)`) or solidifying the source in advance (`query = Enumerable(list(gen))`).
This method is useless if you have constructed an Enumerable from a repeatable source such as
a builtin list, an iterable factory mentioned above, or other `Enumerable`'s query methods.

If cache_capacity is None, it is infinite.

Raises `InvalidOperationError` if cache_capacity is negative.

The behavior of this method differs from that of CachedEnumerable.

----

instancemethod ``average[TResult]()``
---------------------------------------

Constraint
  - `self`: ``Enumerable[SupportsAverage[TResult]]``

Returns
  - ``TResult``

Computes the average value of the sequence. Raises `InvalidOperationError` if there
is no value.

The returned type is the type of the expression
`(elem1 + elem2 + ...) / cast(int, ...)`.

----

instancemethod ``average[TResult](__selector)``
-------------------------------------------------

Parameters
  - `__selector` (``Callable[[TSource_co], SupportsAverage[TResult]]``)

Returns
  - ``TResult``

Computes the average value of the sequence using the selector. Raises
`InvalidOperationError` if there is no value.

The returned type is the type of the expression
`(selector(elem1) + selector(elem2) + ...) / cast(int, ...)`.

----

instancemethod ``average2[TResult, TDefault](__default)``
-----------------------------------------------------------

Constraint
  - `self`: ``Enumerable[SupportsAverage[TResult]]``
Parameters
  - `__default` (``TDefault``)

Returns
  - ``Union[TResult, TDefault]``

Computes the average value of the sequence. Returns `default` if there is no value.

The returned type is the type of the expression
`(elem1 + elem2 + ...) / cast(int, ...)` or `TDefault`.

----

instancemethod ``average2[TResult, TDefault](__selector, __default)``
-----------------------------------------------------------------------

Parameters
  - `__selector` (``Callable[[TSource_co], SupportsAverage[TResult]]``)
  - `__default` (``TDefault``)

Returns
  - ``Union[TResult, TDefault]``

Computes the average value of the sequence using the selector. Returns `default` if there
is no value.

The returned type is the type of the expression
`(selector(elem1) + selector(elem2) + ...) / cast(int, ...)` or `TDefault`.

----

instancemethod ``cast[TResult](__t_result)``
----------------------------------------------

Parameters
  - `__t_result` (``Type[TResult]``)

Returns
  - ``Enumerable[TResult]``

Casts the elements to the specified type.

----

instancemethod ``concat(second)``
-----------------------------------

Parameters
  - `second` (``Iterable[TSource_co]``)

Returns
  - ``Enumerable[TSource_co]``

Concatenates two sequences.

----

instancemethod ``contains(value)``
------------------------------------

Parameters
  - `value` (``object``)

Returns
  - ``bool``

Tests whether the sequence contains the specified element using `==`.

----

instancemethod ``contains[TOther](value, __comparer)``
--------------------------------------------------------

Parameters
  - `value` (``TOther``)
  - `__comparer` (``Callable[[TSource_co, TOther], bool]``)

Returns
  - ``bool``

Tests whether the sequence contains the specified element using the provided comparer.

----

instancemethod ``count()``
----------------------------


Returns
  - ``int``

Returns the number of elements in the sequence.

----

instancemethod ``count(__predicate)``
---------------------------------------

Parameters
  - `__predicate` (``Callable[[TSource_co], bool]``)

Returns
  - ``int``

Returns the number of elements that satisfy the condition.

----

instancemethod ``default_if_empty[TDefault](default)``
--------------------------------------------------------

Parameters
  - `default` (``TDefault``)

Returns
  - ``Union[Enumerable[TSource_co], Enumerable[TDefault]]``

Returns the elements of the sequence or the provided value in a singleton collection if
the sequence is empty.

----

instancemethod ``distinct()``
-------------------------------


Returns
  - ``Enumerable[TSource_co]``

Returns distinct elements from the sequence.

----

instancemethod ``element_at(index)``
--------------------------------------

Parameters
  - `index` (``int``)

Returns
  - ``TSource_co``

Returns the element at specified index in the sequence. `IndexOutOfRangeError` is raised if
no such element exists.

----

instancemethod ``element_at[TDefault](index, __default)``
-----------------------------------------------------------

Parameters
  - `index` (``int``)
  - `__default` (``TDefault``)

Returns
  - ``Union[TSource_co, TDefault]``

Returns the element at specified index in the sequence. Default value is returned if no
such element exists.

----

staticmethod ``empty()``
--------------------------


Returns
  - ``Enumerable[TSource_co]``

Returns an empty enumerable.

----

instancemethod ``except1(second)``
------------------------------------

Parameters
  - `second` (``Iterable[TSource_co]``)

Returns
  - ``Enumerable[TSource_co]``

Produces the set difference of two sequences: self - second.

----

instancemethod ``first()``
----------------------------


Returns
  - ``TSource_co``

Returns the first element of the sequence. Raises `InvalidOperationError` if there is no
first element.

----

instancemethod ``first(__predicate)``
---------------------------------------

Parameters
  - `__predicate` (``Callable[[TSource_co], bool]``)

Returns
  - ``TSource_co``

Returns the first element of the sequence that satisfies the condition. Raises
`InvalidOperationError` if no such element exists.

----

instancemethod ``first2[TDefault](__default)``
------------------------------------------------

Parameters
  - `__default` (``TDefault``)

Returns
  - ``Union[TSource_co, TDefault]``

Returns the first element of the sequence or a default value if there is no such
element.

----

instancemethod ``first2[TDefault](__predicate, __default)``
-------------------------------------------------------------

Parameters
  - `__predicate` (``Callable[[TSource_co], bool]``)
  - `__default` (``TDefault``)

Returns
  - ``Union[TSource_co, TDefault]``

Returns the first element of the sequence that satisfies the condition or a default value if
no such element exists.

----

instancemethod ``group_by[TKey, TValue, TResult](key_selector, value_selector, __result_selector)``
-----------------------------------------------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey]``)
  - `value_selector` (``Callable[[TSource_co], TValue]``)
  - `__result_selector` (``Callable[[TKey, Enumerable[TValue]], TResult]``)

Returns
  - ``Enumerable[TResult]``

Groups the elements of the sequence according to specified key selector and value selector. Then
it returns the result value using each grouping and its key.

----

instancemethod ``group_by[TKey, TValue](key_selector, value_selector)``
-------------------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey]``)
  - `value_selector` (``Callable[[TSource_co], TValue]``)

Returns
  - ``Enumerable[Grouping[TKey, TValue]]``

Groups the elements of the sequence according to specified key selector and value selector.

----

instancemethod ``group_by2[TKey, TResult](key_selector, __result_selector)``
------------------------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey]``)
  - `__result_selector` (``Callable[[TKey, Enumerable[TSource_co]], TResult]``)

Returns
  - ``Enumerable[TResult]``

Groups the elements of the sequence according to a specified key selector function and creates a
result value using each grouping and its key.

----

instancemethod ``group_by2[TKey](key_selector)``
--------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey]``)

Returns
  - ``Enumerable[Grouping[TKey, TSource_co]]``

Groups the elements of the sequence according to a specified key selector function.

----

instancemethod ``group_join[TInner, TKey, TResult](inner, outer_key_selector, inner_key_selector, result_selector)``
----------------------------------------------------------------------------------------------------------------------

Parameters
  - `inner` (``Iterable[TInner]``)
  - `outer_key_selector` (``Callable[[TSource_co], TKey]``)
  - `inner_key_selector` (``Callable[[TInner], TKey]``)
  - `result_selector` (``Callable[[TSource_co, Enumerable[TInner]], TResult]``)

Returns
  - ``Enumerable[TResult]``

Correlates the elements of two sequences based on equality of keys and groups the results using the
selector.

----

instancemethod ``intersect(second)``
--------------------------------------

Parameters
  - `second` (``Iterable[TSource_co]``)

Returns
  - ``Enumerable[TSource_co]``

Produces the set intersection of two sequences: self * second.

----

instancemethod ``join[TInner, TKey, TResult](inner, outer_key_selector, inner_key_selector, result_selector)``
----------------------------------------------------------------------------------------------------------------

Parameters
  - `inner` (``Iterable[TInner]``)
  - `outer_key_selector` (``Callable[[TSource_co], TKey]``)
  - `inner_key_selector` (``Callable[[TInner], TKey]``)
  - `result_selector` (``Callable[[TSource_co, TInner], TResult]``)

Returns
  - ``Enumerable[TResult]``

Correlates the elements of two sequences based on matching keys.

----

instancemethod ``last()``
---------------------------


Returns
  - ``TSource_co``

Returns the last element of the sequence. Raises `InvalidOperationError` if there is no first
element.

----

instancemethod ``last(__predicate)``
--------------------------------------

Parameters
  - `__predicate` (``Callable[[TSource_co], bool]``)

Returns
  - ``TSource_co``

Returns the last element of the sequence that satisfies the condition. Raises
`InvalidOperationError` if no such element exists.

----

instancemethod ``last2[TDefault](__default)``
-----------------------------------------------

Parameters
  - `__default` (``TDefault``)

Returns
  - ``Union[TSource_co, TDefault]``

Returns the last element of the sequence or a default value if there is no such
element.

----

instancemethod ``last2[TDefault](__predicate, __default)``
------------------------------------------------------------

Parameters
  - `__predicate` (``Callable[[TSource_co], bool]``)
  - `__default` (``TDefault``)

Returns
  - ``Union[TSource_co, TDefault]``

Returns the last element of the sequence that satisfies the condition or a default value if
no such element exists.

----

instancemethod ``max[TSupportsLessThan]()``
---------------------------------------------

Constraint
  - `self`: ``Enumerable[TSupportsLessThan]``

Returns
  - ``TSupportsLessThan``

Returns the maximum value in the sequence. Raises `InvalidOperationError` if there is no value.

----

instancemethod ``max[TSupportsLessThan](__result_selector)``
--------------------------------------------------------------

Parameters
  - `__result_selector` (``Callable[[TSource_co], TSupportsLessThan]``)

Returns
  - ``TSupportsLessThan``

Invokes a transform function on each element of the sequence and returns the maximum of the
resulting values. Raises `InvalidOperationError` if there is no value.

----

instancemethod ``max2[TSupportsLessThan, TDefault](__default)``
-----------------------------------------------------------------

Constraint
  - `self`: ``Enumerable[TSupportsLessThan]``
Parameters
  - `__default` (``TDefault``)

Returns
  - ``Union[TSupportsLessThan, TDefault]``

Returns the maximum value in the sequence, or the default one if there is no value.

----

instancemethod ``max2[TSupportsLessThan, TDefault](__result_selector, __default)``
------------------------------------------------------------------------------------

Parameters
  - `__result_selector` (``Callable[[TSource_co], TSupportsLessThan]``)
  - `__default` (``TDefault``)

Returns
  - ``Union[TSupportsLessThan, TDefault]``

Invokes a transform function on each element of the sequence and returns the maximum of the
resulting values. Returns the default one if there is no value.

----

instancemethod ``min[TSupportsLessThan]()``
---------------------------------------------

Constraint
  - `self`: ``Enumerable[TSupportsLessThan]``

Returns
  - ``TSupportsLessThan``

Returns the minimum value in the sequence. Raises `InvalidOperationError` if there is no value.

----

instancemethod ``min[TSupportsLessThan](__result_selector)``
--------------------------------------------------------------

Parameters
  - `__result_selector` (``Callable[[TSource_co], TSupportsLessThan]``)

Returns
  - ``TSupportsLessThan``

Invokes a transform function on each element of the sequence and returns the minimum of the
resulting values. Raises `InvalidOperationError` if there is no value.

----

instancemethod ``min2[TSupportsLessThan, TDefault](__default)``
-----------------------------------------------------------------

Constraint
  - `self`: ``Enumerable[TSupportsLessThan]``
Parameters
  - `__default` (``TDefault``)

Returns
  - ``Union[TSupportsLessThan, TDefault]``

Returns the minimum value in the sequence, or the default one if there is no value.

----

instancemethod ``min2[TSupportsLessThan, TDefault](__result_selector, __default)``
------------------------------------------------------------------------------------

Parameters
  - `__result_selector` (``Callable[[TSource_co], TSupportsLessThan]``)
  - `__default` (``TDefault``)

Returns
  - ``Union[TSupportsLessThan, TDefault]``

Invokes a transform function on each element of the sequence and returns the minimum of the
resulting values. Returns the default one if there is no value.

----

instancemethod ``of_type[TResult](t_result)``
-----------------------------------------------

Parameters
  - `t_result` (``Type[TResult]``)

Returns
  - ``Enumerable[TResult]``

Filters elements based on the specified type.

Builtin `isinstance()` is used.

----

instancemethod ``order_by[TSupportsLessThan](key_selector)``
--------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TSupportsLessThan]``)

Returns
  - ``OrderedEnumerable[TSource_co, TSupportsLessThan]``

Sorts the elements of the sequence in ascending order according to a key.

----

instancemethod ``order_by[TKey](key_selector, __comparer)``
-------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey]``)
  - `__comparer` (``Callable[[TKey, TKey], int]``)

Returns
  - ``OrderedEnumerable[TSource_co, TKey]``

Sorts the elements of the sequence in ascending order by using a specified comparer.

----

instancemethod ``order_by_descending[TSupportsLessThan](key_selector)``
-------------------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TSupportsLessThan]``)

Returns
  - ``OrderedEnumerable[TSource_co, TSupportsLessThan]``

Sorts the elements of the sequence in descending order according to a key.

----

instancemethod ``order_by_descending[TKey](key_selector, __comparer)``
------------------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey]``)
  - `__comparer` (``Callable[[TKey, TKey], int]``)

Returns
  - ``OrderedEnumerable[TSource_co, TKey]``

Sorts the elements of the sequence in descending order by using a specified comparer.

----

instancemethod ``prepend(element)``
-------------------------------------

Parameters
  - `element` (``TSource_co``)

Returns
  - ``Enumerable[TSource_co]``

Adds a value to the beginning of the sequence.

----

staticmethod ``range(start, count)``
--------------------------------------

Parameters
  - `start` (``int``)
  - `count` (``Optional[int]``)

Returns
  - ``Enumerable[int]``

Generates a sequence of `count` integral numbers from `start`, incrementing each by one.

If `count` is `None`, the sequence is infinite. Raises `InvalidOperationError` if `count`
is negative.

----

staticmethod ``repeat[TResult](value, count=None)``
-----------------------------------------------------

Parameters
  - `value` (``TResult``)
  - `count` (``Optional[int]``)

Returns
  - ``Enumerable[TResult]``

Generates a sequence that contains one repeated value.

If `count` is `None`, the sequence is infinite. Raises `InvalidOperationError` if `count`
is negative.

----

instancemethod ``reverse()``
------------------------------


Returns
  - ``Enumerable[TSource_co]``

Inverts the order of the elements in the sequence.

----

instancemethod ``select[TResult](selector)``
----------------------------------------------

Parameters
  - `selector` (``Callable[[TSource_co], TResult]``)

Returns
  - ``Enumerable[TResult]``

Projects each element of the sequence into a new form.

----

instancemethod ``select2[TResult](selector)``
-----------------------------------------------

Parameters
  - `selector` (``Callable[[TSource_co, int], TResult]``)

Returns
  - ``Enumerable[TResult]``

Projects each element of the sequence into a new form by incorporating the indices.

----

instancemethod ``select_many[TCollection, TResult](collection_selector, __result_selector)``
----------------------------------------------------------------------------------------------

Parameters
  - `collection_selector` (``Callable[[TSource_co], Iterable[TCollection]]``)
  - `__result_selector` (``Callable[[TSource_co, TCollection], TResult]``)

Returns
  - ``Enumerable[TResult]``

Projects each element of the sequence into an iterable, flattens the resulting sequence
into one sequence, then calls result_selector on each element therein.

----

instancemethod ``select_many[TResult](__selector)``
-----------------------------------------------------

Parameters
  - `__selector` (``Callable[[TSource_co], Iterable[TResult]]``)

Returns
  - ``Enumerable[TResult]``

Projects each element of the sequence to an iterable and flattens the resultant sequences.

----

instancemethod ``select_many2[TCollection, TResult](collection_selector, __result_selector)``
-----------------------------------------------------------------------------------------------

Parameters
  - `collection_selector` (``Callable[[TSource_co, int], Iterable[TCollection]]``)
  - `__result_selector` (``Callable[[TSource_co, TCollection], TResult]``)

Returns
  - ``Enumerable[TResult]``

Projects each element of the sequence into an iterable, flattens the resulting sequence
into one sequence, then calls result_selector on each element therein. The indices of
source elements are used.

----

instancemethod ``select_many2[TResult](__selector)``
------------------------------------------------------

Parameters
  - `__selector` (``Callable[[TSource_co, int], Iterable[TResult]]``)

Returns
  - ``Enumerable[TResult]``

Projects each element of the sequence to an iterable and flattens the resultant sequences.
The indices of source elements are used.

----

instancemethod ``sequence_equal(second)``
-------------------------------------------

Parameters
  - `second` (``Iterable[TSource_co]``)

Returns
  - ``bool``

Determines whether two sequences are equal using `==` on each element.

----

instancemethod ``single()``
-----------------------------


Returns
  - ``TSource_co``

Returns the only element in the sequence. Raises `InvalidOperationError` if the sequence does not
contain exactly one element.

----

instancemethod ``single(__predicate)``
----------------------------------------

Parameters
  - `__predicate` (``Callable[[TSource_co], bool]``)

Returns
  - ``TSource_co``

Returns the only element in the sequence that satisfies the condition. Raises `InvalidOperationError`
if no element satisfies the condition, or more than one do.

----

instancemethod ``single2[TDefault](__default)``
-------------------------------------------------

Parameters
  - `__default` (``TDefault``)

Returns
  - ``Union[TSource_co, TDefault]``

Returns the only element in the sequence or the default value if the sequence is empty. Raises
`InvalidOperationError` if there are more than one elements in the sequence.

----

instancemethod ``single2[TDefault](__predicate, __default)``
--------------------------------------------------------------

Parameters
  - `__predicate` (``Callable[[TSource_co], bool]``)
  - `__default` (``TDefault``)

Returns
  - ``Union[TSource_co, TDefault]``

Returns the only element in the sequence that satisfies the condition, or the default value if there is
no such element. Raises `InvalidOperationError` if there are more than one elements satisfying the
condition.

----

instancemethod ``skip(count)``
--------------------------------

Parameters
  - `count` (``int``)

Returns
  - ``Enumerable[TSource_co]``

Bypasses a specified number of elements in the sequence and then returns the remaining.

----

instancemethod ``skip_last(count)``
-------------------------------------

Parameters
  - `count` (``int``)

Returns
  - ``Enumerable[TSource_co]``

Returns a new sequence that contains the elements of the current one with `count` elements omitted.

----

instancemethod ``skip_while(predicate)``
------------------------------------------

Parameters
  - `predicate` (``Callable[[TSource_co], bool]``)

Returns
  - ``Enumerable[TSource_co]``

Bypasses elements in the sequence as long as the condition is true and then returns the remaining
elements.

----

instancemethod ``skip_while2(predicate)``
-------------------------------------------

Parameters
  - `predicate` (``Callable[[TSource_co, int], bool]``)

Returns
  - ``Enumerable[TSource_co]``

Bypasses elements in the sequence as long as the condition is true and then returns the remaining
elements. The element's index is used in the predicate function.

----

instancemethod ``sum[TSupportsAdd]()``
----------------------------------------

Constraint
  - `self`: ``Enumerable[TSupportsAdd]``

Returns
  - ``Union[TSupportsAdd, int]``

Computes the sum of the sequence, or `0` if the sequence is empty.

----

instancemethod ``sum[TSupportsAdd](__selector)``
--------------------------------------------------

Parameters
  - `__selector` (``Callable[[TSource_co], TSupportsAdd]``)

Returns
  - ``Union[TSupportsAdd, int]``

Computes the sum of the sequence using the selector. Returns `0` if the sequence is empty.

----

instancemethod ``sum2[TSupportsAdd, TDefault](__default)``
------------------------------------------------------------

Constraint
  - `self`: ``Enumerable[TSupportsAdd]``
Parameters
  - `__default` (``TDefault``)

Returns
  - ``Union[TSupportsAdd, TDefault]``

Computes the sum of the sequence. Returns the default value if it is empty.

----

instancemethod ``sum2[TSupportsAdd, TDefault](__selector, __default)``
------------------------------------------------------------------------

Parameters
  - `__selector` (``Callable[[TSource_co], TSupportsAdd]``)
  - `__default` (``TDefault``)

Returns
  - ``Union[TSupportsAdd, TDefault]``

Computes the sum of the sequence using the selector. Returns the default value if it is empty.

----

instancemethod ``take(count)``
--------------------------------

Parameters
  - `count` (``int``)

Returns
  - ``Enumerable[TSource_co]``

Returns a specified number of contiguous elements from the start of the sequence.

----

instancemethod ``take_last(count)``
-------------------------------------

Parameters
  - `count` (``int``)

Returns
  - ``Enumerable[TSource_co]``

Returns a new sequence that contains the last `count` elements.

----

instancemethod ``take_while(predicate)``
------------------------------------------

Parameters
  - `predicate` (``Callable[[TSource_co], bool]``)

Returns
  - ``Enumerable[TSource_co]``

Returns elements from the sequence as long as the condition is true and skips the remaining.

----

instancemethod ``take_while2(predicate)``
-------------------------------------------

Parameters
  - `predicate` (``Callable[[TSource_co, int], bool]``)

Returns
  - ``Enumerable[TSource_co]``

Returns elements from the sequence as long as the condition is true and skips the remaining. The
element's index is used in the predicate function.

----

instancemethod ``to_dict[TKey, TValue](key_selector, __value_selector)``
--------------------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey]``)
  - `__value_selector` (``Callable[[TSource_co], TValue]``)

Returns
  - ``Dict[TKey, TValue]``

Enumerates all values and returns a dict containing them. key_selector and value_selector
are used to select keys and values.

----

instancemethod ``to_dict[TKey](key_selector)``
------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey]``)

Returns
  - ``Dict[TKey, TSource_co]``

Enumerates all values and returns a dict containing them. key_selector is used to select
keys.

----

instancemethod ``to_set()``
-----------------------------


Returns
  - ``Set[TSource_co]``

Enumerates all values and returns a set containing them.

----

instancemethod ``to_list()``
------------------------------


Returns
  - ``List[TSource_co]``

Enumerates all values and returns a list containing them.

----

instancemethod ``to_lookup[TKey, TValue](key_selector, __value_selector)``
----------------------------------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey]``)
  - `__value_selector` (``Callable[[TSource_co], TValue]``)

Returns
  - ``Lookup[TKey, TValue]``

Enumerates all values and returns a lookup containing them according to specified key
selector and value selector.

----

instancemethod ``to_lookup[TKey](key_selector)``
--------------------------------------------------

Parameters
  - `key_selector` (``Callable[[TSource_co], TKey]``)

Returns
  - ``Lookup[TKey, TSource_co]``

Enumerates all values and returns a lookup containing them according to the specified
key selector.

----

instancemethod ``union(second)``
----------------------------------

Parameters
  - `second` (``Iterable[TSource_co]``)

Returns
  - ``Enumerable[TSource_co]``

Produces the set union of two sequences: self + second.

----

instancemethod ``where(predicate)``
-------------------------------------

Parameters
  - `predicate` (``Callable[[TSource_co], bool]``)

Returns
  - ``Enumerable[TSource_co]``

Filters the sequence of values based on a predicate.

----

instancemethod ``where2(predicate)``
--------------------------------------

Parameters
  - `predicate` (``Callable[[TSource_co, int], bool]``)

Returns
  - ``Enumerable[TSource_co]``

Filters the sequence of values based on a predicate. Each element's index is used in the
predicate logic.

----

instancemethod ``zip[TOther](__second)``
------------------------------------------

Parameters
  - `__second` (``Iterable[TOther]``)

Returns
  - ``Enumerable[Tuple[TSource_co, TOther]]``

Produces a sequence of 2-element tuples from the two sequences.

----

instancemethod ``zip[TOther, TOther2](__second, __third)``
------------------------------------------------------------

Parameters
  - `__second` (``Iterable[TOther]``)
  - `__third` (``Iterable[TOther2]``)

Returns
  - ``Enumerable[Tuple[TSource_co, TOther, TOther2]]``



----

instancemethod ``zip[TOther, TOther2, TOther3](__second, __third, __fourth)``
-------------------------------------------------------------------------------

Parameters
  - `__second` (``Iterable[TOther]``)
  - `__third` (``Iterable[TOther2]``)
  - `__fourth` (``Iterable[TOther3]``)

Returns
  - ``Enumerable[Tuple[TSource_co, TOther, TOther2, TOther3]]``



----

instancemethod ``zip[TOther, TOther2, TOther3, TOther4](__second, __third, __fourth, __fifth)``
-------------------------------------------------------------------------------------------------

Parameters
  - `__second` (``Iterable[TOther]``)
  - `__third` (``Iterable[TOther2]``)
  - `__fourth` (``Iterable[TOther3]``)
  - `__fifth` (``Iterable[TOther4]``)

Returns
  - ``Enumerable[Tuple[TSource_co, TOther, TOther2, TOther3, TOther4]]``



----

instancemethod ``zip(__second, __third, __fourth, __fifth, __sixth, *iters)``
-------------------------------------------------------------------------------

Parameters
  - `__second` (``Iterable[Any]``)
  - `__third` (``Iterable[Any]``)
  - `__fourth` (``Iterable[Any]``)
  - `__fifth` (``Iterable[Any]``)
  - `__sixth` (``Iterable[Any]``)
  - `*iters` (``Iterable[Any]``)

Returns
  - ``Enumerable[Tuple[Any, ...]]``



----

instancemethod ``zip2[TOther, TResult](__second, __result_selector)``
-----------------------------------------------------------------------

Parameters
  - `__second` (``Iterable[TOther]``)
  - `__result_selector` (``Callable[[TSource_co, TOther], TResult]``)

Returns
  - ``Enumerable[TResult]``

Applies a specified function to the corresponding elements of two sequences, producing a
sequence of the results.

----

instancemethod ``zip2[TOther, TOther2, TResult](__second, __third, __result_selector)``
-----------------------------------------------------------------------------------------

Parameters
  - `__second` (``Iterable[TOther]``)
  - `__third` (``Iterable[TOther2]``)
  - `__result_selector` (``Callable[[TSource_co, TOther, TOther2], TResult]``)

Returns
  - ``Enumerable[TResult]``



----

instancemethod ``zip2[TOther, TOther2, TOther3, TResult](__second, __third, __fourth, __result_selector)``
------------------------------------------------------------------------------------------------------------

Parameters
  - `__second` (``Iterable[TOther]``)
  - `__third` (``Iterable[TOther2]``)
  - `__fourth` (``Iterable[TOther3]``)
  - `__result_selector` (``Callable[[TSource_co, TOther, TOther2, TOther3], TResult]``)

Returns
  - ``Enumerable[TResult]``



----

instancemethod ``zip2[TOther, TOther2, TOther3, TOther4, TResult](__second, __third, __fourth, __fifth, __result_selector)``
------------------------------------------------------------------------------------------------------------------------------

Parameters
  - `__second` (``Iterable[TOther]``)
  - `__third` (``Iterable[TOther2]``)
  - `__fourth` (``Iterable[TOther3]``)
  - `__fifth` (``Iterable[TOther4]``)
  - `__result_selector` (``Callable[[TSource_co, TOther, TOther2, TOther3, TOther4], TResult]``)

Returns
  - ``Enumerable[TResult]``



----

instancemethod ``zip2(__second, __third, __fourth, __fifth, __sixth, *iters_and_result_selector)``
----------------------------------------------------------------------------------------------------

Parameters
  - `__second` (``Iterable[Any]``)
  - `__third` (``Iterable[Any]``)
  - `__fourth` (``Iterable[Any]``)
  - `__fifth` (``Iterable[Any]``)
  - `__sixth` (``Iterable[Any]``)
  - `*iters_and_result_selector` (``Union[Iterable[Any], Callable[..., Any]]``)

Returns
  - ``Enumerable[Any]``



----

instancemethod ``elements_in(__index)``
-----------------------------------------

Parameters
  - `__index` (``slice``)

Returns
  - ``Enumerable[TSource_co]``

Produces a subsequence defined by the given slice notation.

----

instancemethod ``elements_in(__start, __stop, __step=1)``
-----------------------------------------------------------

Parameters
  - `__start` (``int``)
  - `__stop` (``int``)
  - `__step` (``int``)

Returns
  - ``Enumerable[TSource_co]``

Produces a subsequence with indices that define a slice.

----

instancemethod ``to_tuple()``
-------------------------------


Returns
  - ``Tuple[TSource_co, ...]``

Enumerates all values and returns a tuple containing them.


