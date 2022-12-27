from pathlib import Path

import pytest
from cleo.commands.command import Command
from cleo.io.buffered_io import BufferedIO
from cleo.io.io import IO
from poetry.config.config import Config
from poetry.console.application import Application
from poetry.core.factory import Factory
from poetry.packages.locker import Locker
from poetry.poetry import Poetry
from poetry.utils.env import MockEnv


class PoetryTestApplication(Application):
    def __init__(self, poetry: Poetry, io: IO) -> None:
        super().__init__()
        self._poetry = poetry
        self._io = io

    def run_command(self, command: Command) -> int:
        return self._run_command(command, self._io)


@pytest.fixture
def env(simple_project: Path) -> MockEnv:
    path = simple_project / ".venv"
    path.mkdir(parents=True)
    return MockEnv(path=path, is_venv=True)


@pytest.fixture
def poetry_io() -> BufferedIO:
    return BufferedIO()


@pytest.fixture
def poetry_application(
    simple_project: Path, poetry_io: BufferedIO, env: MockEnv, mocker,
) -> PoetryTestApplication:
    mocker.patch(
        "poetry.utils.env.EnvManager.create_venv",
        return_value=env,
    )
    mocker.patch(
        "poetry.core.masonry.builders.builder.Builder.build",
        return_value=None,
    )

    base_poetry = Factory().create_poetry(cwd=simple_project)
    locker = Locker(
        base_poetry.file.parent / "poetry.lock", base_poetry.local_config,
    )
    config = Config.create()
    poetry = Poetry(
        base_poetry.file.path,
        base_poetry.local_config,
        base_poetry.package,
        locker,
        config,
        disable_cache=True,
    )
    app = PoetryTestApplication(poetry=poetry, io=poetry_io)
    return app
