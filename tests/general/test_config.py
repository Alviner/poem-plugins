from dataclasses import dataclass, field
from types import MappingProxyType

import pytest

from poem_plugins.config.base import BaseConfig

@dataclass
class B(BaseConfig):
    MAPPERS = MappingProxyType({
        "c": bool
    })
    c: bool = True


@dataclass
class A(BaseConfig):
    MAPPERS = MappingProxyType({
        "a": int,
        "b": B.fabric
    })

    a: int
    b: B = field(default_factory=B)


@pytest.mark.parametrize(
    "kwargs, expected", (
        (dict(a=1), A(a=1, b=B(c=True))),
        (dict(a=1, b=dict(c=False)), A(a=1, b=B(c=False))),
        (dict(a=1, z="unexpected"), A(a=1, b=B(c=True))),
    )
)
def test_from_fabric(kwargs, expected):
    assert A.fabric(kwargs) == expected
