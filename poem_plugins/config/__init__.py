from enum import unique

from pydantic import BaseModel, Field

from poem_plugins.config.git import GitProviderSettings
from poem_plugins.general.strenum import StrEnum


@unique
class VersionProviderEnum(StrEnum):
    GIT = "git"


class BaseConfig(BaseModel):
    pass


class VersionConfig(BaseConfig):
    enabled: bool = False
    update_pyproject: bool = False
    write_version_file: bool = False

    provider: VersionProviderEnum = VersionProviderEnum.GIT
    git: GitProviderSettings = Field(default_factory=GitProviderSettings)


class Config(BaseConfig):
    version: VersionConfig = Field(default_factory=VersionConfig)
