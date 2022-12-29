import pytest

from poem_plugins.config.git import GitProviderSettings, GitVersionFormatEnum
from poem_plugins.general.version import Version
from poem_plugins.general.version.drivers import IVervsionDriver


@pytest.fixture
def git_settings() -> GitProviderSettings:
    return GitProviderSettings(format=GitVersionFormatEnum.LONG)


def test_get_version(
    git_version_driver: IVervsionDriver, expected_long_version: Version,
) -> None:
    assert git_version_driver.get_version() == expected_long_version


def test_render_version(
    git_version_driver: IVervsionDriver, expected_long_version: Version,
) -> None:
    content = git_version_driver.render_version_file(expected_long_version)
    expected = "\n".join(
        (
            '# THIS FILE WAS GENERATED AUTOMATICALLY',
            '# BY: poem-plugins "git" plugin',
            '# NEVER EDIT THIS FILE MANUALLY',
            '',
            'version_info = (1, 2, 0)',
            '__version__ = "1.2.0+gg3c3e199"',
            '',
        ),
    )
    assert content == expected
