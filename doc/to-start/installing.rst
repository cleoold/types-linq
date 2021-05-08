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
***********

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
