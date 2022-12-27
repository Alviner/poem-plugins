import re
from shutil import which
import subprocess
from types import MappingProxyType
from typing import Any, Callable, ClassVar, Mapping, Match, Optional
import warnings

from poem_plugins.general.version_driver.base import IVervsionDriver, Version


GIT_BIN = which("git")
WARNING_TEXT = (
    '"git" binary was not found, this plugin this will not work properly'
)
if GIT_BIN is None:
    warnings.warn(WARNING_TEXT)


class GitLongVersionDriver(IVervsionDriver):
    CONVERTERS: ClassVar[Mapping[str, Callable[[Any], Any]]] = (
        MappingProxyType({
            'major': int,
            'minor': int,
            'patch': int,
        })
    )

    def get_version(self, git_version_prefix: str = "v") -> Version:
        if GIT_BIN is None:
            raise RuntimeError(WARNING_TEXT)

        result = subprocess.run(
            [GIT_BIN, "describe", "--long"],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

        if result.returncode != 0:
            raise RuntimeError("Cannot found git version")
        raw_version = result.stdout.strip()
        regex = (
            r"(?P<major>\d+)\.(?P<minor>\d+)-(?P<patch>\d+)-(?P<commit>\S+)"
        )
        match: Optional[Match[str]] = re.match(
            git_version_prefix + regex,
            raw_version,
        )

        if match is None:
            raise RuntimeError("Cannot parse git version")

        kwargs = {
            k: self.CONVERTERS.get(k, lambda x: x)(v)
            for k, v in match.groupdict().items()
        }

        return Version(**kwargs)
