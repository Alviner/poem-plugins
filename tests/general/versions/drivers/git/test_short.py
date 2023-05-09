import pytest

from poem_plugins.config.git import GitProviderSettings, GitVersionFormatEnum
from poem_plugins.general.version import Version
from poem_plugins.general.version.drivers import IVersionDriver


@pytest.fixture
def git_settings() -> GitProviderSettings:
    return GitProviderSettings(format=GitVersionFormatEnum.SHORT)


def test_get_version(
    git_version_driver: IVersionDriver,
    expected_version: Version,
) -> None:
    assert git_version_driver.get_version() == expected_version


def test_render_version(
    git_version_driver: IVersionDriver,
    expected_version: Version,
) -> None:
    content = git_version_driver.render_version_file(expected_version)
    expected = "\n".join(
        (
            "# THIS FILE WAS GENERATED AUTOMATICALLY",
            '# BY: poem-plugins "git" plugin',
            "# NEVER EDIT THIS FILE MANUALLY",
            "",
            "version_info = (1, 2, 0)",
            '__version__ = "1.2.0"',
            "",
        ),
    )
    assert content == expected
