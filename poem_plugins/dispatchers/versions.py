from dataclasses import dataclass

from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event import Event
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.commands.build import BuildCommand
from poetry.core.utils.helpers import module_name
from poetry.poetry import Poetry
from tomlkit.toml_document import TOMLDocument

from poem_plugins.config import Config, VersionEnum
from poem_plugins.general.versions import Version
from poem_plugins.general.versions.drivers import IVervsionDriver
from poem_plugins.general.versions.drivers.git import GitLongVersionDriver


@dataclass(frozen=True)
class VersionDispatcher:
    config: Config
    driver: IVervsionDriver

    @classmethod
    def factory(cls, config: Config) -> "VersionDispatcher":
        if config.version_plugin == VersionEnum.GIT_LONG:
            driver = GitLongVersionDriver()
        else:
            driver = GitLongVersionDriver()
        return cls(
            driver=driver,
            config=config,
        )

    def _write_pyproject(
        self, poetry: Poetry, version: Version,
    ) -> None:
        if not self.config.update_pyproject:
            return
        content: TOMLDocument = poetry.file.read()
        poetry_content = content["tool"]["poetry"]  # type: ignore
        poetry_content["version"] = str(version)  # type: ignore
        poetry.file.write(content)

    def _write_module(
        self, poetry: Poetry, version: Version,
    ) -> None:
        if not self.config.write_version_file:
            return
        package_name = module_name(poetry.package.name)
        with open(f"{package_name}/version.py", "w") as file:
            file.write(
                self.driver.render_version_file(version=version),
            )

    def __call__(
        self, event: Event, event_name: str, dispatcher: EventDispatcher,
    ) -> None:
        if not isinstance(event, ConsoleCommandEvent):
            return
        command = event.command
        if not isinstance(command, BuildCommand):
            return
        if not self.config.version_plugin:
            return
        io = event.io
        poetry = command.poetry
        try:
            version = self.driver.get_version(self.config.git_version_prefix)
        except Exception as exc:
            io.write_error_line(f"<b>poem-plugins</b>: {exc}")
            raise exc

        io.write_line(
            f"<b>poem-plugins</b>: Setting version to: {version}",
        )
        poetry.package.version = str(version)  # type: ignore

        self._write_pyproject(poetry, version)
        self._write_module(poetry, version)
