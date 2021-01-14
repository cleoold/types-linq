# types-linq

![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg) [![pypi](https://img.shields.io/pypi/v/types-linq)](https://pypi.org/project/types-linq/)

This is an attempt to implement linq methods seen in .NET ([link](https://docs.microsoft.com/en-us/dotnet/api/system.linq.enumerable?view=net-5.0)). Currently WIP.

Goal:
* Incorporates Enumerable method specs as precise as possible
* Handles infinite streams (generators) smoothly like in _SICP_
  * Deferred evaluations
* Detailed typing support
* Honours collections.abc interfaces

To run the test cases, install `pytest`, and then invoke it under the current directory:
```sh
$ pytest
```

To install it on the computer, do
```sh
$ pip install .
# or
$ python setup.py install
```
Or install from pypi.

The usage is simple if you know about the interfaces in .NET as this library provides almost the exact methods:
```py
from dataclasses import dataclass
from types_linq import Enumerable as en

@dataclass
class PetOwner:
    name: str
    pets: List[str]

pet_owners = [
    PetOwner(name='Higa', pets=['Scruffy', 'Sam']),
    PetOwner(name='Ashkenazi', pets=['Walker', 'Sugar']),
    PetOwner(name='Price', pets=['Scratches', 'Diesel']),
    PetOwner(name='Hines', pets=['Dusty']),
]

query = en(pet_owners)                                             \
    .select_many(
        lambda pet_owner: pet_owner.pets,
        lambda pet_owner, pet_name: (pet_owner, pet_name),
    )                                                              \
    .where(lambda owner_and_pet: owner_and_pet[1].startswith('S')) \
    .select(lambda owner_and_pet: {
        'owner': owner_and_pet[0].name, 'pet': owner_and_pet[1],
        }
    )

for obj in query:
    print(obj)

# output:
# {'owner': 'Higa', 'pet': 'Scruffy'}
# {'owner': 'Higa', 'pet': 'Sam'}
# {'owner': 'Ashkenazi', 'pet': 'Sugar'}
# {'owner': 'Price', 'pet': 'Scratches'}
```
This example is taken from the .NET doc.
