Examples
#########

The primary class importable from this library is the ``Enumerable`` class. To query on an
existing object such as lists, tuples, or generators, you pass the object to the ``Enumerable``
constructor, then invoke chained methods like this:

.. code-block:: python

    from types_linq import Enumerable

    lst = [1, 4, 7, 9, 16]

    query = Enumerable(lst).where(lambda x: x % 2 == 0).select(lambda x: x ** 2)

    for x in query:
        print(x)

This will filter the list by whether the element is even, then converts each element to
the square of it. The call to ``where`` and ``select`` will return immediately. Finally
when the iterator of ``query`` is requested in the for loop, the element will be enumerated
in the order.

It is roughly equivalent to the following code:

.. code-block:: python

    for x in lst:
        if x % 2 == 0:
            print(x ** 2)

or

.. code-block:: python

    for x in map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, lst)):
        print(x)

The output will be ``16`` and ``256`` printed on newlines.

The class supports a lot more than this. The usage is simple if you know about the interfaces
in .NET as this library provides almost the exact methods. It is advised to take a look at
the `tests <https://github.com/cleoold/types-linq/tree/main/tests>`_ to digest more in-action
use cases.

More examples
*******************

`Grouping <https://docs.microsoft.com/en-us/dotnet/api/system.linq.enumerable.groupjoin>`_ and
transforming lists:

.. code-block:: python

    from typing import NamedTuple
    from types_linq import Enumerable as En


    class AnswerSheet(NamedTuple):
        subject: str
        score: int
        name: str

    students = ['Jacque', 'Franklin', 'Romeo']
    papers = [
        AnswerSheet(subject='Calculus', score=78, name='Jacque'),
        AnswerSheet(subject='Calculus', score=98, name='Romeo'),
        AnswerSheet(subject='Algorithms', score=59, name='Romeo'),
        AnswerSheet(subject='Mechanics', score=93, name='Jacque'),
        AnswerSheet(subject='E & M', score=87, name='Jacque'),
    ]

    query = En(students) \
        .order_by(lambda student: student) \
        .group_join(papers,
            lambda student: student,
            lambda paper: paper.name,
            lambda student, papers: {
                'student': student,
                'papers': papers.order_by(lambda paper: paper.subject) \
                    .select(lambda paper: {
                        'subject': paper.subject,
                        'score': paper.score,
                    }).to_list(),
                'gpa': papers.average2(lambda paper: paper.score, None),
            }
        )

    for obj in query:
        print(obj)

    # output:
    # {'student': 'Franklin', 'papers': [], 'gpa': None}
    # {'student': 'Jacque', 'papers': [{'subject': 'E & M', 'score': 87}, {'subject': 'Mechanics', 'score': 93}, {'subject': 'Calculus', 'score': 78}], 'gpa': 86.0}
    # {'student': 'Romeo', 'papers': [{'subject': 'Algorithms', 'score': 59}, {'subject': 'Calculus', 'score': 98}], 'gpa': 78.5}

Working with generators:

.. code-block:: python

    import random
    from types_linq import Enumerable as En

    def toss_coins():
        while True:
            yield random.choice(('Head', 'Tail'))

    times_head = En(toss_coins()).take(5) \  # [:5] also works
        .count(lambda r: r == 'Head')

    print(f'You tossed 5 times with {times_head} HEADs!')

    # possible output:
    # You tossed 5 times with 2 HEADs!

Working with stream output:

.. code-block:: python

    import sys, subprocess
    from types_linq import Enumerable as En

    proc = subprocess.Popen('kubectl logs -f my-pod', shell=True, stdout=subprocess.PIPE)
    stdout = iter(proc.stdout.readline, b'')

    query = En(stdout).where(lambda line: line.startswith(b'CRITICAL: ')) \
        .select(lambda line: line[10:].decode())

    for line in query:
        sys.stdout.write(line)
        sys.stdout.flush()

    # whatever.
