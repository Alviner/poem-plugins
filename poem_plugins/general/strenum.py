from enum import Enum
from typing import Iterable


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self._value_

    @classmethod
    def choices(cls) -> Iterable[str]:
        return set(map(str, cls))
