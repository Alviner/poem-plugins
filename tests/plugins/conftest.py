from pathlib import Path
from typing import Callable, Type

import pytest
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from cleo.io.buffered_io import BufferedIO
from poetry.config.config import Config as PoetryConfig
from poetry.console.commands.env_command import EnvCommand
from poetry.core.factory import Factory
from poetry.packages.locker import Locker
from poetry.poetry import Poetry
from poetry.utils.env import MockEnv

from poem_plugins.config import Config, VersionEnum
from poem_plugins.dispatchers.versions import VersionDispatcher


@pytest.fixture
def poetry_io() -> BufferedIO:
    return BufferedIO()


@pytest.fixture
def poetry(
    simple_project: Path,
) -> Poetry:
    base_poetry = Factory().create_poetry(cwd=simple_project)
    locker = Locker(
        base_poetry.file.parent / "poetry.lock", base_poetry.local_config,
    )
    config = PoetryConfig.create()
    return Poetry(
        base_poetry.file.path,
        base_poetry.local_config,
        base_poetry.package,
        locker,
        config,
        disable_cache=True,
    )



@pytest.fixture
def config() -> Config:
    return Config(
        version_plugin=VersionEnum.GIT_LONG,
        update_pyproject=True,
        write_version_file=True,
    )

@pytest.fixture
def version_dispatcher(config: Config) -> VersionDispatcher:
    return VersionDispatcher.factory(config)


@pytest.fixture
def run_command(
    poetry: Poetry, poetry_io: BufferedIO,
    version_dispatcher: VersionDispatcher,
) -> Callable[[Type[EnvCommand]], None]:
    env = MockEnv()
    event_dispatcher = EventDispatcher()

    def _creator(cls: Type[EnvCommand]) -> None:
        command = cls()
        command.set_env(env)
        command.set_poetry(poetry)
        event = ConsoleCommandEvent(
            command=command,
            io=poetry_io,
        )
        version_dispatcher(
            event, "anything", event_dispatcher,
        )
    return _creator
