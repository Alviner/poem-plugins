from pathlib import Path
from cleo.io.buffered_io import BufferedIO
from poetry.config.config import Config
from poetry.packages.locker import Locker
from poetry.poetry import Poetry
from poetry.core.factory import Factory
import pytest



@pytest.fixture
def poetry_io() -> BufferedIO:
    return BufferedIO()



@pytest.fixture
def poetry(simple_project: Path) -> Poetry:
    base_poetry = Factory().create_poetry(cwd=simple_project)
    locker = Locker(
        base_poetry.file.parent / "poetry.lock", base_poetry.local_config
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
    return poetry
