# module ``types_linq.more.more_enumerable``

(apiref.MoreEnumerable)=
## class `MoreEnumerable[TSource_co]`

```py
from types_linq.more import MoreEnumerable
```

MoreEnumerable provides more query methods. Instances of this class can be created by directly
constructing, using `as_more()`, or invoking MoreEnumerable methods that return MoreEnumerable
instead of Enumerable.

These APIs may have breaking changes more frequently than those in Enumerable class because updates
in .NET are happening and sometimes ones of these APIs could be moved to Enumerable with modification,
or changed to accommodate changes to Enumerable.

Revisions
    ~ v0.2.0: New.

### Bases

- [`Enumerable`](apiref.Enumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

### Members

#### instancemethod `aggregate_right[TAccumulate, TResult](__seed, __func, __result_selector)`

Parameters
  ~ *__seed*: [`TAccumulate`](apiref.TAccumulate)
  ~ *__func*: `Callable[[`[`TSource_co`](apiref.TSource_co)`, `[`TAccumulate`](apiref.TAccumulate)`], `[`TAccumulate`](apiref.TAccumulate)`]`
  ~ *__result_selector*: `Callable[[`[`TAccumulate`](apiref.TAccumulate)`], `[`TResult`](apiref.TResult)`]`

Returns
  ~ [`TResult`](apiref.TResult)

Applies a right-associative accumulator function over the sequence. The seed is used as
the initial accumulator value, and the result_selector is used to select the result value.

Revisions
    ~ v1.2.0: Fixed annotation for __func.

---

#### instancemethod `aggregate_right[TAccumulate](__seed, __func)`

Parameters
  ~ *__seed*: [`TAccumulate`](apiref.TAccumulate)
  ~ *__func*: `Callable[[`[`TSource_co`](apiref.TSource_co)`, `[`TAccumulate`](apiref.TAccumulate)`], `[`TAccumulate`](apiref.TAccumulate)`]`

Returns
  ~ [`TAccumulate`](apiref.TAccumulate)

Applies a right-associative accumulator function over the sequence. The seed is used as the
initial accumulator value.

Example
    ~   ```py
        >>> values = [9, 4, 2]
        >>> MoreEnumerable(values).aggregate_right('null', lambda e, rr: f'(cons {e} {rr})')
        '(cons 9 (cons 4 (cons 2 null)))'
        ```

Revisions
    ~ v1.2.0: Fixed annotation for __func.

---

#### instancemethod `aggregate_right(__func)`

Parameters
  ~ *__func*: `Callable[[`[`TSource_co`](apiref.TSource_co)`, `[`TSource_co`](apiref.TSource_co)`], `[`TSource_co`](apiref.TSource_co)`]`

Returns
  ~ [`TSource_co`](apiref.TSource_co)

Applies a right-associative accumulator function over the sequence. Raises [`InvalidOperationError`](apiref.InvalidOperationError)
if there is no value in the sequence.

Example
    ~   ```py
        >>> values = ['9', '4', '2', '5']
        >>> MoreEnumerable(values).aggregate_right(lambda e, rr: f'({e}+{rr})')
        '(9+(4+(2+5)))'
        ```

Revisions
    ~ v1.2.0: Fixed annotation for __func.

---

#### instancemethod `as_more()`


Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Returns the original MoreEnumerable reference.

---

#### instancemethod `consume()`


Returns
  ~ `None`

Consumes the sequence completely. This method iterates the sequence immediately and does not save
any intermediate data.

Revisions
    ~ v1.1.0: New.

---

#### instancemethod `cycle(count=None)`

Parameters
  ~ *count*: `Optional[int]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Repeats the sequence `count` times.

If `count` is `None`, the sequence is infinite. Raises [`InvalidOperationError`](apiref.InvalidOperationError) if `count`
is negative.

Example
    ~   ```py
        >>> MoreEnumerable([1, 2, 3]).cycle(3).to_list()
        [1, 2, 3, 1, 2, 3, 1, 2, 3]
        ```

Revisions
    ~ v1.1.0: New.

---

#### instancemethod `enumerate(start=0)`

Parameters
  ~ *start*: `int`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[Tuple[int, `[`TSource_co`](apiref.TSource_co)`]]`

Returns a sequence of tuples containing the index and the value from the source sequence. `start`
is used to specify the starting index.

Example
    ~   ```py
        >>> ints = [2, 4, 6]
        >>> MoreEnumerable(ints).enumerate().to_list()
        [(0, 2), (1, 4), (2, 6)]
        ```

Revisions
    ~ v1.0.0: New.

---

#### instancemethod `except_by2(second, key_selector)`

Parameters
  ~ *second*: `Iterable[`[`TSource_co`](apiref.TSource_co)`]`
  ~ *key_selector*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], object]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Produces the set difference of two sequences: self - second, according to a key selector that
determines "distinctness". Note the second iterable is homogenous to self.

Example
    ~   ```py
        >>> first = [(16, 'x'), (9, 'y'), (12, 'd'), (16, 't')]
        >>> second = [(24, 'd'), (77, 'y')]
        >>> MoreEnumerable(first).except_by2(second, lambda x: x[1]).to_list()
        [(16, 'x'), (16, 't')]
        ```

Revisions
    ~ v1.0.0: Renamed from `except_by()` to this name to accommodate an update to Enumerable class.
    ~ v0.2.1: Added preliminary support for unhashable keys.

---

#### instancemethod `flatten()`


Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[Any]`

Flattens the sequence containing arbitrarily-nested subsequences.

Note: the nested objects must be Iterable to be flatten.
Instances of `str` or `bytes` are not flattened.

Example
    ~   ```py
        >>> lst = ['apple', ['orange', ['juice', 'mango'], 'delta function']]
        >>> MoreEnumerable(lst).flatten().to_list()
        ['apple', 'orange', 'juice', 'mango', 'delta function']
        ```

---

#### instancemethod `flatten(__predicate)`

Parameters
  ~ *__predicate*: `Callable[[Iterable[Any]], bool]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[Any]`

Flattens the sequence containing arbitrarily-nested subsequences. A predicate function determines
whether a nested iterable should be flattened or not.

Note: the nested objects must be Iterable to be flatten.

---

#### instancemethod `flatten2(selector)`

Parameters
  ~ *selector*: `Callable[[Any], Optional[Iterable[object]]]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[Any]`

Flattens the sequence containing arbitrarily-nested subsequences. A selector is used to select a
subsequence based on the object's properties. If the selector returns None, then the object is
considered a leaf.

---

#### instancemethod `for_each(action)`

Parameters
  ~ *action*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], object]`

Returns
  ~ `None`

Executes the given function on each element in the source sequence. The return values are discarded.

Example
    ~   ```py
        >>> def gen():
        ...     yield 116; yield 35; yield -9

        >>> Enumerable(gen()).where(lambda x: x > 0).as_more().for_each(print)
        116
        35
        ```

---

#### instancemethod `for_each2(action)`

Parameters
  ~ *action*: `Callable[[`[`TSource_co`](apiref.TSource_co)`, int], object]`

Returns
  ~ `None`

Executes the given function on each element in the source sequence. Each element's index is used in
the logic of the function. The return values are discarded.

---

#### instancemethod `interleave(*iters)`

Parameters
  ~ **iters*: `Iterable[`[`TSource_co`](apiref.TSource_co)`]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Interleaves the elements of two or more sequences into a single sequence, skipping sequences if they
are consumed.

Example
    ~   ```py
        >>> MoreEnumerable(['1', '2']).interleave(['4', '5', '6'], ['7', '8', '9']).to_list()
        ['1', '4', '7', '2', '5', '8', '6', '9']
        ```

---

#### instancemethod `maxima_by[TSupportsLessThan](selector)`

Parameters
  ~ *selector*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], `[`TSupportsLessThan`](apiref.TSupportsLessThan)`]`

Returns
  ~ [`ExtremaEnumerable`](apiref.ExtremaEnumerable)`[`[`TSource_co`](apiref.TSource_co)`, `[`TSupportsLessThan`](apiref.TSupportsLessThan)`]`

Returns the maximal elements of the sequence based on the given selector.

Example
    ~   ```py
        >>> strings = ['foo', 'bar', 'cheese', 'orange', 'baz', 'spam', 'egg', 'toasts', 'dish']
        >>> MoreEnumerable(strings).maxima_by(len).to_list()
        ['cheese', 'orange', 'toasts']
        >>> MoreEnumerable(strings).maxima_by(lambda x: x.count('e')).first()
        'cheese'
        ```

---

#### instancemethod `maxima_by[TKey](selector, __comparer)`

Parameters
  ~ *selector*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], `[`TKey`](apiref.TKey)`]`
  ~ *__comparer*: `Callable[[`[`TKey`](apiref.TKey)`, `[`TKey`](apiref.TKey)`], int]`

Returns
  ~ [`ExtremaEnumerable`](apiref.ExtremaEnumerable)`[`[`TSource_co`](apiref.TSource_co)`, `[`TKey`](apiref.TKey)`]`

Returns the maximal elements of the sequence based on the given selector and the comparer.

Such comparer takes two values and return positive ints when lhs > rhs, negative ints
if lhs < rhs, and 0 if they are equal.

---

#### instancemethod `minima_by[TSupportsLessThan](selector)`

Parameters
  ~ *selector*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], `[`TSupportsLessThan`](apiref.TSupportsLessThan)`]`

Returns
  ~ [`ExtremaEnumerable`](apiref.ExtremaEnumerable)`[`[`TSource_co`](apiref.TSource_co)`, `[`TSupportsLessThan`](apiref.TSupportsLessThan)`]`

Returns the minimal elements of the sequence based on the given selector.

---

#### instancemethod `minima_by[TKey](selector, __comparer)`

Parameters
  ~ *selector*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], `[`TKey`](apiref.TKey)`]`
  ~ *__comparer*: `Callable[[`[`TKey`](apiref.TKey)`, `[`TKey`](apiref.TKey)`], int]`

Returns
  ~ [`ExtremaEnumerable`](apiref.ExtremaEnumerable)`[`[`TSource_co`](apiref.TSource_co)`, `[`TKey`](apiref.TKey)`]`

Returns the minimal elements of the sequence based on the given selector and the comparer.

Such comparer takes two values and return positive ints when lhs > rhs, negative ints
if lhs < rhs, and 0 if they are equal.

---

#### instancemethod `pipe(action)`

Parameters
  ~ *action*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], object]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Executes the given action on each element in the sequence and yields it. Return values of
action are discarded.

Example
    ~   ```py
        >>> store = set()
        >>> MoreEnumerable([1, 2, 2, 1]).pipe(store.add).where(lambda x: x % 2 == 0).to_list()
        [2, 2]
        >>> store
        {1, 2}
        ```

Revisions
    ~ v0.2.1: New.

---

#### instancemethod `pre_scan[TAccumulate](identity, transformation)`

Parameters
  ~ *identity*: [`TAccumulate`](apiref.TAccumulate)
  ~ *transformation*: `Callable[[`[`TAccumulate`](apiref.TAccumulate)`, `[`TSource_co`](apiref.TSource_co)`], `[`TAccumulate`](apiref.TAccumulate)`]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TAccumulate`](apiref.TAccumulate)`]`

Performs a pre-scan (exclusive prefix sum) over the sequence. Such scan returns an
equal-length sequence where the first element is the identity, and i-th element (i>1) is
the sum of the first i-1 (and identity) elements in the original sequence.

Example
    ~   ```py
        >>> values = [9, 4, 2, 5, 7]
        >>> MoreEnumerable(values).pre_scan(0, lambda acc, e: acc + e).to_list()
        [0, 9, 13, 15, 20]
        >>> MoreEnumerable([]).pre_scan(0, lambda acc, e: acc + e).to_list()
        []
        ```

Revisions
    ~ v1.2.0: New.

---

#### instancemethod `rank[TSupportsLessThan]()`

Constraint
  ~ *self*: [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSupportsLessThan`](apiref.TSupportsLessThan)`]`


Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[int]`

Ranks each item in the sequence in descending order.

Example
    ~   ```py
        >>> scores = [1, 4, 77, 23, 23, 4, 9, 0, -7, 101, 23]
        >>> MoreEnumerable(scores).rank().to_list()
        [6, 5, 2, 3, 3, 5, 4, 7, 8, 1, 3]  # 101 is largest, so has rank of 1
        ```

Revisions
    ~ v1.0.0: New.

---

#### instancemethod `rank(__comparer)`

Parameters
  ~ *__comparer*: `Callable[[`[`TSource_co`](apiref.TSource_co)`, `[`TSource_co`](apiref.TSource_co)`], int]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[int]`

Ranks each item in the sequence in descending order using the given comparer.

Such comparer takes two values and return positive ints when lhs > rhs, negative ints
if lhs < rhs, and 0 if they are equal.

Revisions
    ~ v1.0.0: New.

---

#### instancemethod `rank_by[TSupportsLessThan](key_selector)`

Parameters
  ~ *key_selector*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], `[`TSupportsLessThan`](apiref.TSupportsLessThan)`]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[int]`

Ranks each item in the sequence in descending order using the given selector.

Example
    ~   ```py
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
        ```

Revisions
    ~ v1.0.0: New.

---

#### instancemethod `rank_by[TKey](key_selector, __comparer)`

Parameters
  ~ *key_selector*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], `[`TKey`](apiref.TKey)`]`
  ~ *__comparer*: `Callable[[`[`TKey`](apiref.TKey)`, `[`TKey`](apiref.TKey)`], int]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[int]`

Ranks each item in the sequence in descending order using the given selector and comparer.

Such comparer takes two values and return positive ints when lhs > rhs, negative ints
if lhs < rhs, and 0 if they are equal.

Revisions
    ~ v1.0.0: New.

---

#### instancemethod `run_length_encode()`


Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[Tuple[`[`TSource_co`](apiref.TSource_co)`, int]]`

Run-length encodes the sequence into a sequence of tuples where each tuple contains an
(the first) element and its number of contingent occurrences, where equality is based on
`==`.

Example
    ~   ```py
        >>> MoreEnumerable('abbcaeeeaa').run_length_encode().to_list()
        [('a', 1), ('b', 2), ('c', 1), ('a', 1), ('e', 3), ('a', 2)]
        ```

Revisions
    ~ v1.1.0: New.

---

#### instancemethod `run_length_encode(__comparer)`

Parameters
  ~ *__comparer*: `Callable[[`[`TSource_co`](apiref.TSource_co)`, `[`TSource_co`](apiref.TSource_co)`], bool]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[Tuple[`[`TSource_co`](apiref.TSource_co)`, int]]`

Run-length encodes the sequence into a sequence of tuples where each tuple contains an
(the first) element and its number of contingent occurrences, where equality is determined by
the comparer.

Example
    ~   ```py
        >>> MoreEnumerable('abBBbcaEeeff') \
        >>>     .run_length_encode(lambda x, y: x.lower() == y.lower()).to_list()
        [('a', 1), ('b', 4), ('c', 1), ('a', 1), ('E', 3), ('f', 2)]
        ```

Revisions
    ~ v1.1.0: New.

---

#### instancemethod `scan(__transformation)`

Parameters
  ~ *__transformation*: `Callable[[`[`TSource_co`](apiref.TSource_co)`, `[`TSource_co`](apiref.TSource_co)`], `[`TSource_co`](apiref.TSource_co)`]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Performs a inclusive prefix sum over the sequence. Such scan returns an equal-length sequence
where the i-th element is the sum of the first i elements in the original sequence.

Example
    ~   ```py
        >>> values = [9, 4, 2, 5, 7]
        >>> MoreEnumerable(values).scan(lambda acc, e: acc + e).to_list()
        [9, 13, 15, 20, 27]
        >>> MoreEnumerable([]).scan(lambda acc, e: acc + e).to_list()
        []
        ```

Example
    ~   ```py
        >>> # running max
        >>> fruits = ['apple', 'mango', 'orange', 'passionfruit', 'grape']
        >>> MoreEnumerable(fruits).scan(lambda acc, e: e if len(e) > len(acc) else acc).to_list()
        ['apple', 'apple', 'orange', 'passionfruit', 'passionfruit']
        ```

Revisions
    ~ v1.2.0: New.

---

#### instancemethod `scan[TAccumulate](__seed, __transformation)`

Parameters
  ~ *__seed*: [`TAccumulate`](apiref.TAccumulate)
  ~ *__transformation*: `Callable[[`[`TAccumulate`](apiref.TAccumulate)`, `[`TSource_co`](apiref.TSource_co)`], `[`TAccumulate`](apiref.TAccumulate)`]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TAccumulate`](apiref.TAccumulate)`]`

Like Enumerable.aggregate(seed, transformation) except that the intermediate results are
included in the result sequence.

Example
    ~   ```py
        >>> Enumerable.range(1, 5).as_more().scan(-1, lambda acc, e: acc * e).to_list()
        [-1, -1, -2, -6, -24, -120]
        ```

Revisions
    ~ v1.2.0: New.

---

#### instancemethod `scan_right(__func)`

Parameters
  ~ *__func*: `Callable[[`[`TSource_co`](apiref.TSource_co)`, `[`TSource_co`](apiref.TSource_co)`], `[`TSource_co`](apiref.TSource_co)`]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Performs a right-associative inclusive prefix sum over the sequence. This is the
right-associative version of MoreEnumerable.scan(func).

Example
    ~   ```py
        >>> values = ['9', '4', '2', '5']
        >>> MoreEnumerable(values).scan_right(lambda e, rr: f'({e}+{rr})').to_list()
        ['(9+(4+(2+5)))', '(4+(2+5))', '(2+5)', '5']
        >>> MoreEnumerable([]).scan_right(lambda e, rr: e + rr).to_list()
        []
        ```

Revisions
    ~ v1.2.0: New.

---

#### instancemethod `scan_right[TAccumulate](__seed, __func)`

Parameters
  ~ *__seed*: [`TAccumulate`](apiref.TAccumulate)
  ~ *__func*: `Callable[[`[`TSource_co`](apiref.TSource_co)`, `[`TAccumulate`](apiref.TAccumulate)`], `[`TAccumulate`](apiref.TAccumulate)`]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TAccumulate`](apiref.TAccumulate)`]`

The right-associative version of MoreEnumerable.scan(seed, func).

Example
    ~   ```py
        >>> values = [9, 4, 2]
        >>> MoreEnumerable(values).scan_right('null', lambda e, rr: f'(cons {e} {rr})').to_list()
        ['(cons 9 (cons 4 (cons 2 null)))', '(cons 4 (cons 2 null))', '(cons 2 null)', 'null']
        ```

Revisions
    ~ v1.2.0: New.

---

#### instancemethod `segment(new_segment_predicate)`

Parameters
  ~ *new_segment_predicate*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], bool]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]]`

Splits the sequence into segments by using a detector function that returns True to signal a
new segment.

Example
    ~   ```py
        >>> values = [0, 1, 2, 4, -4, -2, 6, 2, -2]
        >>> MoreEnumerable(values).segment(lambda x: x < 0).select(lambda x: x.to_list()).to_list()
        [[0, 1, 2, 4], [-4], [-2, 6, 2], [-2]]
        ```

Revisions
    ~ v1.2.0: New.

---

#### instancemethod `segment2(new_segment_predicate)`

Parameters
  ~ *new_segment_predicate*: `Callable[[`[`TSource_co`](apiref.TSource_co)`, int], bool]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]]`

Splits the sequence into segments by using a detector function that returns True to signal a
new segment. The element's index is used in the detector function.

Example
    ~   ```py
        >>> values = [0, 1, 2, 4, -4, -2, 6, 2, -2]
        >>> MoreEnumerable(values).segment2(lambda x, i: x < 0 or i % 3 == 0) \
        ...     .select(lambda x: x.to_list()) \
        ...     .to_list()
        [[0, 1, 2], [4], [-4], [-2], [6, 2], [-2]]
        ```

Revisions
    ~ v1.2.0: New.

---

#### instancemethod `segment3(new_segment_predicate)`

Parameters
  ~ *new_segment_predicate*: `Callable[[`[`TSource_co`](apiref.TSource_co)`, `[`TSource_co`](apiref.TSource_co)`, int], bool]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]]`

Splits the sequence into segments by using a detector function that returns True to signal a
new segment. The last element and the current element's index are used in the detector
function.

Example
    ~   ```py
        >>> values = [0, 1, 2, 4, -4, -2, 6, 2, -2]
        >>> MoreEnumerable(values).segment3(lambda curr, prev, i: curr * prev < 0) \
        ...     .select(lambda x: x.to_list()) \
        ...     .to_list()
        [[0, 1, 2, 4], [-4, -2], [6, 2], [-2]]
        ```

Revisions
    ~ v1.2.0: New.

---

#### staticmethod `traverse_breath_first[TSource](root, children_selector)`

Parameters
  ~ *root*: [`TSource`](apiref.TSource)
  ~ *children_selector*: `Callable[[`[`TSource`](apiref.TSource)`], Iterable[`[`TSource`](apiref.TSource)`]]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource`](apiref.TSource)`]`

Traverses the tree (graph) from the root node in a breath-first fashion. A selector is used to
select children of each node.

Graphs are not checked for cycles or duplicates visits. If the resulting sequence needs to be
finite then it is the responsibility of children_selector to ensure that duplicate nodes are not
visited.

Example
    ~   ```py
        >>> tree = { 3: [1, 4], 1: [0, 2], 4: [5] }
        >>> MoreEnumerable.traverse_breath_first(3, lambda x: tree.get(x, [])) \
        >>>     .to_list()
        [3, 1, 4, 0, 2, 5]
        ```

---

#### staticmethod `traverse_depth_first[TSource](root, children_selector)`

Parameters
  ~ *root*: [`TSource`](apiref.TSource)
  ~ *children_selector*: `Callable[[`[`TSource`](apiref.TSource)`], Iterable[`[`TSource`](apiref.TSource)`]]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource`](apiref.TSource)`]`

Traverses the tree (graph) from the root node in a depth-first fashion. A selector is used to
select children of each node.

Graphs are not checked for cycles or duplicates visits. If the resulting sequence needs to be
finite then it is the responsibility of children_selector to ensure that duplicate nodes are not
visited.

Example
    ~   ```py
        >>> tree = { 3: [1, 4], 1: [0, 2], 4: [5] }
        >>> MoreEnumerable.traverse_depth_first(3, lambda x: tree.get(x, [])) \
        >>>     .to_list()
        [3, 1, 0, 2, 4, 5]
        ```

---

#### instancemethod `traverse_topological(children_selector)`

Parameters
  ~ *children_selector*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], Iterable[`[`TSource_co`](apiref.TSource_co)`]]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Traverses the graph in topological order, A selector is used to select children of each
node. The ordering created from this method is a variant of depth-first traversal and ensures
duplicate nodes are output once.

To invoke this method, the self sequence contains nodes with zero in-degrees to start the
iteration. Passing a list of all nodes is allowed although not required.

Raises [`DirectedGraphNotAcyclicError`](apiref.DirectedGraphNotAcyclicError) if the directed graph contains a cycle and the
topological ordering cannot be produced.

Example
    ~   ```py
        >>> adj = { 5: [2, 0], 4: [0, 1], 2: [3], 3: [1] }
        >>> MoreEnumerable([5, 4]).traverse_topological(lambda x: adj.get(x, [])) \
        >>>     .to_list()
        [5, 2, 3, 4, 0, 1]
        ```

Revisions
    ~ main: New.

---

#### instancemethod `traverse_topological(children_selector, __key_selector)`

Parameters
  ~ *children_selector*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], Iterable[`[`TSource_co`](apiref.TSource_co)`]]`
  ~ *__key_selector*: `Callable[[`[`TSource_co`](apiref.TSource_co)`], object]`

Returns
  ~ [`MoreEnumerable`](apiref.MoreEnumerable)`[`[`TSource_co`](apiref.TSource_co)`]`

Traverses the graph in topological order, A selector is used to select children of each
node. The ordering created from this method is a variant of depth-first traversal and
ensures duplicate nodes are output once. A key selector is used to determine equality
between nodes.

To invoke this method, the self sequence contains nodes with zero in-degrees to start the
iteration. Passing a list of all nodes is allowed although not required.

Raises [`DirectedGraphNotAcyclicError`](apiref.DirectedGraphNotAcyclicError) if the directed graph contains a cycle and the
topological ordering cannot be produced.

Revisions
    ~ main: New.

