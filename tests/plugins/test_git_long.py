from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest
from cleo.io.buffered_io import BufferedIO
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.plugins.plugin_manager import PluginManager
from poetry.utils.env import MockEnv

from poem_plugins.general.versions import Version
from poem_plugins.versions.git import GitLongVersionPlugin
from tests.plugins.conftest import PoetryTestApplication


@pytest.fixture
def run_command(
    poetry_application: PoetryTestApplication, env: MockEnv,
):
    plugin_manager = PluginManager(ApplicationPlugin.group)
    plugin_manager.add_plugin(GitLongVersionPlugin())
    plugin_manager.activate(poetry_application)

    def _activate(command: str):
        cmd = poetry_application.find(command)
        if hasattr(cmd, "set_env"):
            cmd.set_env(env)
        poetry_application.run_command(cmd)
    return _activate


def test_output_version(poetry_io: BufferedIO, run_command) -> None:
    run_command("build")
    expected = "poem-plugins: Setting version to: 1.2.0+gg3c3e199\n"
    assert poetry_io.fetch_output().startswith(expected)


def test_file_version(
    simple_project: Path, expected_version: Version, run_command,
) -> None:
    run_command("build")
    version_path = simple_project / "simple_project" / "version.py"
    spec = spec_from_file_location(
        "simple_project.version", version_path,
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
    poetry_application: PoetryTestApplication,
    expected_version: Version, run_command,
) -> None:
    run_command("build")
    content = poetry_application.poetry.file.read()
    poetry_content = content["tool"]["poetry"]
    assert poetry_content["version"] == str(expected_version)
