Differences from `"IEnumerable<out T>"`
##########################################

Because Python and C# are two languages that have a lot of differences, this library does not
intimate everything from the .NET world as some practices are not possible Python world. This
section lists some differences (or limitations) between the ``types_linq.Enumerable`` class
and its .NET counterpart.

* In C#, there are extension methods. By ``using`` the correct namespaces, the query methods
  will be automatically available on all references to ``IEnumerable`` variables. Such concepts
  do not exist in Python, hence users have to wrap the object under a ``types_linq.Enumerable``
  class to use those query methods.
* C# uses overloading extensively while there are no real method overloading in Python. Rather,
  to define overload methods in Python, one must use the ``typing.overload`` decorator to decorate
  stubs, then implement all overloads together in a single definition. An example can be found
  `here <https://docs.python.org/3/library/typing.html#typing.overload>`_.
  The downside of this is that the features supported are quite limited.

  For example, it can be simple to seperate between ``def fn(a: int) -> None`` and ``def fn(a: int, b: int) -> None``,
  also between ``def fn(a: str) -> None`` and ``def fn(a: bytes) -> None`` by checking the number of
  arguments or using ``isinstance()``. However, when it comes to separate ``def fn(a: Callable[[TSource_co], bool]) -> None``
  and ``def fn(Callable[[TSource_co, int], bool]) -> None``, there is no straightforward way that works
  for all occasions (typical reflection check will fail for C extensions, and try-except is impractical).
  This library's solution is a sketchy one: using different names for these methods, for example, ``Enumerable.where()``
  and ``Enumerable.where2()``. This is the reason why some names of methods here end with numbers.

  It can also bring some troubles when disambiguating types that overlap. If an object implements both
  ``Iterable`` and ``Callable``, and there are method overloads for each, the behavior might be
  inconsistent if the implementation does not agree with stubs. Type checkers will pick the first matching
  overload.
* There are no "IEqualityComparer" or something like that in Python. C# people will use these to compare
  objects, construct hashmaps, etc. While in Python such identities are often solely determined by object's
  magic methods such as ``__hash__()``, ``__eq__()``, ``__lt__()``, etc. So method overloads that involve such
  comparer interfaces are omitted in this library, or implemented in another form.
* In C#, there are nullable types and default values for a type. For example, ``default(int) == 0`` and ``default(int?) == null``.
  Some C# methods return such default values if the source sequence is empty, or skip ``null``'s if the source sequence contains
  concrete data too. There are no such notions in Python and the C#-like default semantics are non-existent. So, this usage is
  not supported by this library (Can ``None`` be considered a default value for all cases? Hmm..).
* C# has `Index <https://docs.microsoft.com/en-us/dotnet/api/system.index>`_ syntaxes, and to be Pythonic, these are
  negative indices. C# has `Range <https://docs.microsoft.com/en-us/dotnet/api/system.range>`_, which are
  `slices <https://docs.python.org/3/library/functions.html#slice>`_. This difference can be seen in ``Enumerable.element_at()``
  and ``Enumerable.take()``.
* All classes in this library are concrete. There are no interfaces like what are usually done in C#.

Limitations:

* To deal with overloads, some method parameters are positional-only, e.g. those starting with double
  underscores. Some of them can be improved.
* ``OrderedEnumerable`` exposing unnecessary type parameter ``TKey``.
* ``Lookup.__getitem__()``, ``Lookup.contains()``, ``Lookup.count`` are incompatible with the superclass methods they
  are overriding.
