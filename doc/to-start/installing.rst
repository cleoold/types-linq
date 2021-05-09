Installing
################

From pypi
***********

The project is available on `pypi <https://pypi.org/project/types-linq/>`_, to install the
letest version, do:

.. code-block:: bash

    $ pip install types-linq -U

From GitHub Repo
******************

Clone the project and install from local files:

.. code-block:: bash

    $ git clone https://github.com/cleoold/types-linq && cd types-linq
    $ pip install .
    # or
    $ python setup.py install

Run Tests
============

In the project root, execute the following commands (or something similar) to run the
test cases:

.. code-block:: bash

    # optionally set up venv
    $ python -m venv
    $ ./scripts/activate

    $ pip install pytest
    $ python -m pytest

If you want to run the project against `pyright <https://github.com/microsoft/pyright>`_,
the following should do:

.. code-block:: bash

    $ npx install pyright -g
    $ npx pyright

Instead, opening vscode should also hightlight red striggles (?)

However, the `GitHub action settings <https://github.com/cleoold/types-linq/tree/main/.github/workflows>`_
are most up-to-date and can be consulted.

Build the Documentation
=========================

To generate the pages you are currently looking at, in the project root,
execute the following commands:

.. code-block:: bash

    $ cd doc
    $ pip install -r requirements.txt
    # generate api rst files
    $ python ./gen_api_doc.py
    # create html pages, contents are available in _build/html folder
    $ make html

Note to generate api files, one must have Python version 3.9 or above. The api rst files
are commited to the repository.
