import re
import subprocess
import warnings
from dataclasses import dataclass
from shutil import which
from types import MappingProxyType
from typing import Any, Callable, ClassVar, Mapping, Match, Optional

from poem_plugins.config.git import GitProviderSettings, GitVersionFormatEnum
from poem_plugins.general.version import Version
from poem_plugins.general.version.drivers import IVersionDriver


GIT_BIN = which("git")
WARNING_TEXT = (
    '"git" binary was not found, this plugin this will not work properly'
)
if GIT_BIN is None:
    warnings.warn(WARNING_TEXT)


@dataclass
class GitVersionDriver(IVersionDriver):
    settings: GitProviderSettings

    VERSION_TEMPLATE: str = (
        "# THIS FILE WAS GENERATED AUTOMATICALLY\n"
        "# BY: {whoami}\n"
        "# NEVER EDIT THIS FILE MANUALLY\n"
        "\n"
        "version_info = ({major}, {minor}, {patch})\n"
        '__version__ = "{version}"\n'
    )

    CONVERTERS: ClassVar[
        Mapping[str, Callable[[Any], Any]]
    ] = MappingProxyType(
        {
            "major": int,
            "minor": int,
            "patch": int,
        },
    )

    def get_version(self) -> Version:
        if GIT_BIN is None:
            raise RuntimeError(WARNING_TEXT)

        result = subprocess.run(
            [GIT_BIN, "describe", "--long"],
            stdout=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError("Cannot found git version")
        raw_version = result.stdout.strip()
        regex = (
            r"(?P<major>\d+)\.(?P<minor>\d+)-(?P<patch>\d+)-(?P<commit>\S+)"
        )
        match: Optional[Match[str]] = re.match(
            self.settings.version_prefix + regex,
            raw_version,
        )

        if match is None:
            raise RuntimeError("Cannot parse git version")
        raw_kwargs = dict(match.groupdict())
        if self.settings.format == GitVersionFormatEnum.SHORT:
            raw_kwargs.pop("commit", None)
        kwargs = {
            k: self.CONVERTERS.get(k, lambda x: x)(v)
            for k, v in raw_kwargs.items()
        }

        return Version(**kwargs)

    def render_version_file(
        self,
        version: Version,
    ) -> str:
        return self.VERSION_TEMPLATE.format(
            whoami='poem-plugins "git" plugin',
            major=version.major,
            minor=version.minor,
            patch=version.patch,
            version=str(version),
        )
