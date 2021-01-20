# types-linq

![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg) [![pypi](https://img.shields.io/pypi/v/types-linq)](https://pypi.org/project/types-linq/) [![pytest](https://github.com/cleoold/types-linq/workflows/pytest/badge.svg)](https://github.com/cleoold/types-linq/actions?query=workflow%3Apytest) [![codecov](https://codecov.io/gh/cleoold/types-linq/branch/main/graph/badge.svg?token=HTUKZ0SQJ3)](https://codecov.io/gh/cleoold/types-linq)

This is an attempt to implement linq methods seen in .NET ([link](https://docs.microsoft.com/en-us/dotnet/api/system.linq.enumerable?view=net-5.0)). Currently WIP.

Goal:
* Incorporates Enumerable method specs as precise as possible
* Handles infinite streams (generators) smoothly like in _SICP_
  * Deferred evaluations
* Detailed typing support
* Honours collections.abc interfaces

## Install

To install this library on your computer, do:
```sh
$ git clone https://github.com/cleoold/types-linq && cd types-linq
$ pip install .
# or
$ python setup.py install
```
Or install from pypi:
```sh
$ pip install types-linq -U
```

## Dev
Execute the following commands (or something similar) to run the test cases:
```sh
# optionally set up venv
$ python -m venv
$ ./scripts/activate

$ pip install pytest
$ python -m pytest
```

## Examples

The usage is simple if you know about the interfaces in .NET as this library provides almost the exact methods.

### [Grouping](https://docs.microsoft.com/en-us/dotnet/api/system.linq.enumerable.groupjoin) & Transforming lists
```py
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
```

### Working with generators
```py
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
```

### Also querying stream output
Mixing with builtin iterable type objects.
```py
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
```
