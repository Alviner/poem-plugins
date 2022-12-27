from dataclasses import dataclass

from poem.general.strenum import StrEnum


class VersionEnum(StrEnum):
    GIT_LONG = "git-long"


@dataclass
class Config:
    version_plugin: VersionEnum = VersionEnum.GIT_LONG
