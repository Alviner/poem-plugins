from dataclasses import dataclass, field
from enum import unique
from types import MappingProxyType
from typing import Optional

from poem_plugins.config.base import BaseConfig
from poem_plugins.config.git import GitProviderSettings
from poem_plugins.general.strenum import StrEnum


@unique
class VersionProviderEnum(StrEnum):
    GIT = "git"


@unique
class QuotesEnum(StrEnum):
    double = '"'
    single = "'"


@unique
class VersionPlaceEnum(StrEnum):
    TOOL_POETRY = "tool.poetry"
    PROJECT = "project"


@dataclass
class VersionConfig(BaseConfig):
    MAPPERS = MappingProxyType(
        {
            "provider": VersionProviderEnum,
            "update_pyproject": bool,
            "update_pyproject_place": VersionPlaceEnum,
            "write_version_file": bool,
            "git": GitProviderSettings.fabric,
            "quote": QuotesEnum,
        },
    )

    provider: Optional[VersionProviderEnum] = None

    update_pyproject: bool = False
    update_pyproject_place: VersionPlaceEnum = VersionPlaceEnum.TOOL_POETRY
    write_version_file: bool = False
    version_file_quotes: Optional[QuotesEnum] = None

    git: GitProviderSettings = field(default_factory=GitProviderSettings)
