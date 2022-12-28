import pytest

from poem_plugins.config.git import GitProviderSettings
from poem_plugins.general.version.drivers.git import GitVersionDriver


@pytest.fixture
def git_settings() -> GitProviderSettings:
    return GitProviderSettings()

@pytest.fixture
def git_version_driver(git_settings) -> GitVersionDriver:
    return GitVersionDriver(git_settings)
