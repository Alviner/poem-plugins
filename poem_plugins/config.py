from dataclasses import dataclass
from typing import Optional

from poem_plugins.general.strenum import StrEnum


class VersionEnum(StrEnum):
    GIT_LONG = "git-long"


@dataclass
class Config:
    version_plugin: Optional[VersionEnum] = None
    git_version_prefix: str = "v"
