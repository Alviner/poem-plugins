from types import MappingProxyType
from typing import (
    Any, Callable, ClassVar, Mapping, MutableMapping, Type, TypeVar,
)


ConfigType = TypeVar("ConfigType", bound="BaseConfig")

KwargsType = Mapping[str, Any]

MapperType = Callable[[Any], Any]


def is_unset(value: Any) -> bool:
    return value in (None, "")


class BaseConfig:
    MAPPERS: ClassVar[Mapping[str, MapperType]] = MappingProxyType({})

    @classmethod
    def fabric(cls: Type[ConfigType], kwargs: KwargsType) -> ConfigType:
        mapped_kwargs: MutableMapping[str, Any] = {}
        for field, raw_value in kwargs.items():
            mapper = cls.MAPPERS.get(field)
            if not mapper:
                continue
            if is_unset(raw_value):
                mapped_value = None
            else:
                mapped_value = mapper(raw_value)
            mapped_kwargs[field] = mapped_value
        return cls(**mapped_kwargs)
