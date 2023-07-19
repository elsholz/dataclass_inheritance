from dataclasses import dataclass, field
from typing import Optional


@dataclass(kw_only=True)
class A:
    a_1: int = 1
    a_2: Optional[int]
    a_3: Optional[int] = None

    def __post_init__(self):
        print("__post_init__ for class A called:", self)


@dataclass(kw_only=True)
class B:
    b_1: int = 2
    b_2: Optional[int]

    def __post_init__(self):
        print("__post_init__ for class B called:", self)


@dataclass(kw_only=True)
class C(A, B):
    c_1: int = 3
    c_2: int
    kwargs: field(default_factory=dict) = None

    def __post_init__(self):
        print("__post_init__ for class C called:", self)
        # __mro__ lists the types inherited from in order.
        # The first item is the type itself, the last one is object.
        for x in type(self).__mro__[1:-1]:
            if hasattr(x, '__post_init__'):
                x.__post_init__(self)

C(c_2=5, b_2=None, a_2=123)

# Script output:
# __post_init__ for class C called: C(b_1=2, b_2=None, a_1=1, a_2=123, a_3=None, c_1=3, c_2=5, kwargs=None)
# __post_init__ for class A called: C(b_1=2, b_2=None, a_1=1, a_2=123, a_3=None, c_1=3, c_2=5, kwargs=None)
# __post_init__ for class B called: C(b_1=2, b_2=None, a_1=1, a_2=123, a_3=None, c_1=3, c_2=5, kwargs=None)
