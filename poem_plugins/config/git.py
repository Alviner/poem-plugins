from enum import unique

from pydantic import BaseModel

from poem_plugins.general.strenum import StrEnum


@unique
class GitVersionFormatEnum(StrEnum):
    LONG = "long"
    SHORT = "short"


class GitProviderSettings(BaseModel):
    format: GitVersionFormatEnum = GitVersionFormatEnum.SHORT
    version_prefix: str = "v"
