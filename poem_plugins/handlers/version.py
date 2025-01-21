from dataclasses import dataclass
from typing import Container, Optional

from cleo.io.io import IO
from poetry.core.utils.helpers import module_name
from poetry.poetry import Poetry
from tomlkit import TOMLDocument, item

from poem_plugins.config import (
    QuotesEnum,
    VersionConfig,
    VersionPlaceEnum,
    VersionProviderEnum,
)
from poem_plugins.general.version import Version
from poem_plugins.general.version.drivers import IVersionDriver
from poem_plugins.general.version.drivers.git import GitVersionDriver
from poem_plugins.handlers import IHandler
from poetry.core.constraints.version import Version as pcVersion


@dataclass(frozen=True)
class VersionHandler(IHandler):
    config: VersionConfig
    driver: IVersionDriver

    @classmethod
    def factory(cls, config: VersionConfig) -> "VersionHandler":
        if config.provider == VersionProviderEnum.GIT:
            driver = GitVersionDriver(settings=config.git)
        else:
            driver = GitVersionDriver(settings=config.git)
        return cls(
            config=config,
            driver=driver,
        )

    def handle(self, poetry: Poetry, io: IO) -> None:
        if not self.config.provider:
            return
        try:
            version = self.driver.get_version()
        except Exception as exc:
            io.write_error_line(f"<b>poem-plugins</b>: {exc}")
            raise exc

        io.write_line(
            f"<b>poem-plugins</b>: Setting version to: {version}",
        )
        poetry.package.version = pcVersion.parse(str(version))

        if self.config.update_pyproject:
            self._write_pyproject(poetry, version)

        if self.config.write_version_file:
            self._write_module(
                poetry,
                version,
                self.config.version_file_quotes,
            )

    def _write_pyproject(
        self,
        poetry: Poetry,
        version: Version,
    ) -> None:
        content: TOMLDocument = poetry.file.read()

        if self.config.update_pyproject_place == VersionPlaceEnum.PROJECT:
            if "project" not in content:
                content["project"] = {}
            if isinstance(content["project"], Container):
                content["project"]["version"] = item(str(version))

        elif self.config.update_pyproject_place == VersionPlaceEnum.TOOL_POETRY:
            if "tool" not in content:
                content["tool"] = {}
            if "poetry" not in content["tool"]:  # type: ignore
                content["tool"]["poetry"] = {}  # type: ignore
            content["tool"]["poetry"]["version"] = str(version)  # type: ignore
        else:
            upp = self.config.update_pyproject_place
            raise ValueError(f"Unknown place: {upp}")

        poetry.file.write(content)

    def _write_module(
        self,
        poetry: Poetry,
        version: Version,
        quotes: Optional[QuotesEnum] = None,
    ) -> None:
        package_name = module_name(poetry.package.name)
        with open(f"{package_name}/version.py", "w") as file:
            content = self.driver.render_version_file(version=version)
            if quotes is not None:
                content = content.replace('"', quotes)
            file.write(content)
