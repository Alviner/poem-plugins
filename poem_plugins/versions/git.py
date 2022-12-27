import abc
import re
import subprocess
from typing import Match, Optional

from cleo.io.io import IO
from poetry.poetry import Poetry
from poetry.core.utils.helpers import module_name

from poem_plugins.base import BasePlugin
from poem_plugins.config import Config, VersionEnum


class IVersionPlugin(abc.ABC):
    @abc.abstractmethod
    def _can_be_used(self, config: Config) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_version(self) -> str:
        raise NotImplementedError


class BaseVersionPlugin(BasePlugin, IVersionPlugin, abc.ABC):
    def activate(self, poetry: Poetry, io: IO) -> None:
        config = self.get_config(poetry)
        if not self._can_be_used(config):
            return
        try:
            version = self._get_version()
        except Exception as exc:
            io.write_error_line(f"<b>poem-plugins</b>: {exc}")
            raise exc

        io.write_line(
            f"<b>poem-plugins</b>: Setting version to: {version}"
        )
        poetry.package.version = version  # type: ignore

        package_name = module_name(poetry.package.name)
        with open(f"{package_name}/version.py", "w") as file:
            file.write(f'__version__ = "{version}"')
        return


class GitLongVersionPlugin(BaseVersionPlugin):
    def _can_be_used(self, config: Config) -> bool:
        return config.version_plugin == VersionEnum.GIT_LONG

    def _get_version(self) -> str:
        result = subprocess.run(
            ["git", "describe"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        if result.returncode != 0:
            raise RuntimeError("Cannot found git version")
        match: Optional[Match[str]] = re.match(
            r'v(\d+)\.(\d+)-(\d+)-(\S+)',
            result.stdout.strip(),
        )

        if match is None:
            raise RuntimeError("Cannot parse git version")
        major, minor, patch, commit_hash = match.groups()
        return f'{major}.{minor}.{patch}+{commit_hash}'
