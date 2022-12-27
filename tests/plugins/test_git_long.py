from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from cleo.io.buffered_io import BufferedIO
from poetry.plugins import Plugin
from poetry.plugins.plugin_manager import PluginManager
from poetry.poetry import Poetry
import pytest
from poem_plugins.general.version_driver.base import Version

from poem_plugins.versions.git import GitLongVersionPlugin


@pytest.fixture
def run_plugin(poetry: Poetry, poetry_io: BufferedIO):
    def _activate():
        plugin_manager = PluginManager(Plugin.group)
        plugin_manager.add_plugin(GitLongVersionPlugin())
        plugin_manager.activate(poetry, poetry_io)
    return _activate



def test_output_version(poetry_io: BufferedIO, run_plugin) -> None:
    run_plugin()
    expected = 'poem-plugins: Setting version to: 1.2.0+gg3c3e199\n'
    assert poetry_io.fetch_output() == expected


def test_file_version(
    simple_project: Path, expected_version: Version, run_plugin,
) -> None:
    run_plugin()
    version_path = simple_project / "simple_project" / "version.py"
    spec = spec_from_file_location(
        "simple_project.version", version_path
    )
    assert spec
    version_module = module_from_spec(spec)
    spec.loader.exec_module(version_module)
    assert version_module.__version__ == str(expected_version)
    assert version_module.version_info == (
        expected_version.major,
        expected_version.minor,
        expected_version.patch,
    )


def test_pyproject_version(
    poetry: Poetry, expected_version: Version, run_plugin,
) -> None:
    run_plugin()
    content = poetry.file.read()
    poetry_content = content["tool"]["poetry"]
    assert poetry_content["version"] == str(expected_version)
