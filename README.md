# Poem Plugins

[![Pypi](https://img.shields.io/pypi/v/poem-plugins?color=%2334D058&label=pypi%20package)](https://pypi.org/project/poem-plugins)
[![Coverage Status](https://coveralls.io/repos/github/Alviner/poem-plugins/badge.svg?branch=main)](https://coveralls.io/github/Alviner/poem-plugins?branch=main)

A set of plugins for [**Poetry**](https://python-poetry.org/).

## How to use
Make sure you have Poetry version `1.2.0` or above. Read below for instructions to install it if you haven't.

### Install Poem Plugins

Install this plugin to your Poetry:

```console
$ poetry self add poem-plugins
```

### Version Plugin

The poetry plugin for project versioning allows users to specify
the version of their project via the provider other than the default `pyproject.toml` file.
This can be useful for users who prefer to set the project version based on a git tag, for example.

Plugin can be configured via a section in the `pyproject.toml` file.
To use the plugin, you will need to add a section to your `pyproject.toml`
file that specifies the provider.

Here's an example of how you might configure the plugin in your `pyproject.toml` file:
```toml
[tool.poem-plugins.version]
provider = "git"
```
Likewise, you can specify a number of optional arguments to control the plugin
behavior. Here are some of the arguments that you can use:
| Name  | description |  Default |
|-------|-------------|---------|
| `update_pyproject`   | plugin will not only use version from provider for building, but save it in `pyproject.toml` | `false` |
| `write_version_file` | plugin will create a file `version.py` inside a module, with version information             | `false` |


You can specify provider-specific settings in your configuration.
To specify provider-specific settings, you can use the `tool.poem-plugins.version.{provider}` section.
Here are some of the arguments that you can use for `git` provider:
| Name  | description | Default |
|-------|-------------|---------|
| `version_prefix`    | filter tags only starts with this prefix  | `v` |
| `format`            | plugin will use commit hash (long) or not (short) to build a project version | `short` |

Example:

```toml
[tool.poem-plugins.version.git]
version_prefix = "v"
format = "short"
```

To build your project, run the `poetry build` command.
The plugin will build the version via provider and use it to set the version for the project.
```console
$ git tag -a v0.1 -m 'tag description'
$ poetry build
poem-plugins: Setting version to: 0.1.0
Building awesome_package (0.1.0)
  - Building sdist
  - Built awesome_package-0.1.0.tar.gz
  - Building wheel
  - Built awesome_package-0.1.0-py3-none-any.whl```
```
