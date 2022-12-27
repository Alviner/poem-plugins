from contextlib import contextmanager
import os
from pathlib import Path
import tempfile
from typing import Iterator, Optional
import zipfile

import pytest

from poem_plugins.general.version_driver.base import Version


FIXTURES = Path(__file__).parent / 'fixtures'

PROJECT_ZIP = FIXTURES / 'project_folder.zip'


@pytest.fixture(scope='session')
def tmpdir():
    @contextmanager
    def _getter(
        dir: Optional[Path] = None, prefix: Optional[str] = None,
    ) -> Iterator[str]:
        with tempfile.TemporaryDirectory(dir=dir, prefix=prefix) as dirname:
            yield dirname
    return _getter



@pytest.fixture(autouse=True)
def simple_project(tmpdir) -> Iterator[Path]:
    with tmpdir(prefix="projects_") as dir:
        with zipfile.ZipFile(PROJECT_ZIP, 'r') as zip_ref:
            zip_ref.extractall(dir)
            simple_project_path = Path(dir) / 'simple_project'
            os.chdir(simple_project_path)
            yield simple_project_path


@pytest.fixture
def expected_version() -> Version:
    return Version(1, 2, 0, 'g3c3e199')
