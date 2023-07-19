from pydantic.dataclasses import dataclass
from pydantic import ValidationError
from ipaddress import IPv4Address
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
    c_3: IPv4Address

    def __post_init__(self):
        print("__post_init__ for class C called:", self)
        # __mro__ lists the types inherited from in order.
        # The first item is the type itself, the last one is object.
        for x in type(self).__mro__[1:-1]:
            if hasattr(x, "__post_init__"):
                x.__post_init__(self)


# This doesn't fail, as the string 10.10.10.10 can be interpreted as an ip address
obj = C(c_2=10, b_2=None, a_2=123, c_3="10.10.10.10")
print("obj:", obj)
print("obj.c_3, type(obj.c_3):", obj.c_3, type(obj.c_3))


try:
    C(c_2=10, b_2=None, a_2=123, c_3="not an ip address")
    assert False
except ValidationError as e:
    ...


try:
    # missing non-defaultable argument c_3
    C(c_2="I'm not an int", b_2=None, a_2=123)
    assert False
except ValidationError as e:
    ...

# Script output:
# __post_init__ for class C called: C(b_1=2, b_2=None, a_1=1, a_2=123, a_3=None, c_1=3, c_2=10, c_3=IPv4Address('10.10.10.10'))
# __post_init__ for class A called: C(b_1=2, b_2=None, a_1=1, a_2=123, a_3=None, c_1=3, c_2=10, c_3=IPv4Address('10.10.10.10'))
# __post_init__ for class B called: C(b_1=2, b_2=None, a_1=1, a_2=123, a_3=None, c_1=3, c_2=10, c_3=IPv4Address('10.10.10.10'))
# obj: C(b_1=2, b_2=None, a_1=1, a_2=123, a_3=None, c_1=3, c_2=10, c_3=IPv4Address('10.10.10.10'))
# obj.c_3, type(obj.c_3): 10.10.10.10 <class 'ipaddress.IPv4Address'>
