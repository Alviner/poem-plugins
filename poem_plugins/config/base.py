from types import MappingProxyType
from typing import (
    Any, Callable, ClassVar, Type, TypeVar, Mapping, MutableMapping,
)


ConfigType = TypeVar("ConfigType", bound="BaseConfig")

KwargsType = Mapping[str, Any]

MapperType = Callable[[Any], Any]


class BaseConfig:
    MAPPERS: ClassVar[Mapping[str, MapperType]] = MappingProxyType({})

    @classmethod
    def fabric(cls: Type[ConfigType], kwargs: KwargsType) -> ConfigType:
        mapped_kwargs: MutableMapping[str, Any] = {}
        for field, raw_value in kwargs.items():
            mapper = cls.MAPPERS.get(field)
            if not mapper:
                continue
            mapped_value = mapper(raw_value)
            mapped_kwargs[field] = mapped_value
        return cls(**mapped_kwargs)
