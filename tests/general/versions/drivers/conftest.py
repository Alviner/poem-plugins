import pytest

from poem_plugins.general.versions.drivers.git import GitLongVersionDriver


@pytest.fixture
def git_long_version_driver() -> GitLongVersionDriver:
    return GitLongVersionDriver()
