from poem_plugins.general.versions import Version
from poem_plugins.general.versions.drivers import IVervsionDriver


def test_get_version(
    git_long_version_driver: IVervsionDriver, expected_version: Version,
) -> None:
    assert git_long_version_driver.get_version() == expected_version
