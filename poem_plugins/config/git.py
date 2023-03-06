from dataclasses import dataclass
from enum import unique
from types import MappingProxyType

from poem_plugins.config.base import BaseConfig
from poem_plugins.general.strenum import StrEnum


@unique
class GitVersionFormatEnum(StrEnum):
    LONG = "long"
    SHORT = "short"


@dataclass
class GitProviderSettings(BaseConfig):
    MAPPERS = MappingProxyType(
        {
            "format": GitVersionFormatEnum,
            "version_prefix": str,
        },
    )

    format: GitVersionFormatEnum = GitVersionFormatEnum.SHORT
    version_prefix: str = "v"
