Welcome to types-linq's documentation!
########################################

``types-linq`` is a lightweight Python library that attempts to implement LINQ (Language Integrated Query)
features seen in .NET languages (`see here for their documentation <https://docs.microsoft.com/en-us/dotnet/api/system.linq.enumerable>`_).

This library provides similarly expressive and unified querying exprience on objects so long as it is
`iterable <https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable>`_.
With few simple method calls and lambdas, developers can perform complex traversal, filter and transformations
on any data that typically had to be done with many iterative logics such as for loops.

There have been several libraries that try providing such functionalities, while this library tries to accomplish
something different:

* It incorporates the original APIs in .NET ``IEnumerable`` class as close as possible, including method names,
  conventions, edge behaviors, etc. This means typical Python conventions might be shadowed here
* It tries to implement deferred evaluations. The library operates in a streaming manner if possible and handles
  infinite streams (Python generators) properly
* Strong type safety while using this library is guarenteed since the APIs are `typed <https://www.python.org/dev/peps/pep-0484/>`_
* It honours the Python `collections.abc <https://docs.python.org/3/library/collections.abc.html>`_ interfaces

The project is licensed under the BSD-2-Clause License.

.. toctree::
    :hidden:

    self

.. toctree::
    :maxdepth: 1
    :caption: To Start:

    to-start/installing.rst
    to-start/examples.rst
    to-start/differences.rst
    to-start/changelog.rst
    GitHub Project <https://github.com/cleoold/types-linq>

.. toctree::
    :maxdepth: 1
    :caption: API:
    :glob:

    api/*

.. toctree::
    :maxdepth: 1
    :caption: API (MORE):
    :glob:

    api/more/*
