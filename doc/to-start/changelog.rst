Changelog
############

`GitHub Releases <https://github.com/cleoold/types-linq/releases>`_

v1.2.0
********

- Add pre_scan(), scan(), scan_right() and segment() to MoreEnumerable class
- Fix type annotation mistake in Enumerable.aggregate(__func)
- Fix type annotation mistakes in MoreEnumerable.aggregate_right()

v1.1.0
********

- Add consume(), cycle(), and run_length_encode() to MoreEnumerable class
- Fix error in ExtremaEnumerable.take() when it takes a slice

v1.0.0
********

- Add enumerate(), rank() and rank_by() to MoreEnumerable class
- Add chunk(), max_by(), min_by(), intersect_by() and union_by() to Enumerable class
- Enumerable.element_at() now supports negative index
- Enumerable.take() now supports taking a slice (which is same as Enumerable.elements_in()) to be consistent with
  .NET 6
- Enumerable.__getitem__() now supports providing a default value
- **Breaking**: Add Enumerable.distinct_by() that returns an Enumerable instance. MoreEnumerable.distinct_by() that
  returned a MoreEnumerable instance is removed
- **Breaking**: Add Enumerable.except_by(). The previous MoreEnumerable.except_by() that took homogeneous values as
  the second iterable is now renamed as MoreEnumerable.except_by2()

v0.2.1
********

- Add pipe() to MoreEnumerable class
- Enumerable.distinct(), except1(), .union(), .intersect(), .to_lookup(), .join(), .group_by(), .group_join(),
  MoreEnumerable.distinct_by(), .except_by() now have preliminary support for unhashable keys

v0.2.0
********

- Add a MoreEnumerable class containing the following method names: aggregate_right(), distinct_by(), except_by(),
  flatten(), for_each(), interleave(), maxima_by(), minima_by(), traverse_breath_first() and traverse_depth_first()
- Add as_more() to Enumerable class

v0.1.2
********

- Add to_tuple()
- Add an overload to sequence_equal() that accepts a comparision function
- https://github.com/cleoold/types-linq/commit/f70bd510492a915776f6cac26854111650541b22

v0.1.1
********

- Change zip() to support multiple
- Add as_cached() method to memoize results
- Fix OrderedEnumerable bug that once use [] operator on it, returning incorrect result
- Add dunder to some parameter names seen in pyi to prevent them from being passed as named arguments
- https://github.com/cleoold/types-linq/commit/b1b70b9d489cfe06ab1a69c4a0e4a5d195f5f5d7

v0.1.0
********

- Initial releases under the BSD-2-Clause License
