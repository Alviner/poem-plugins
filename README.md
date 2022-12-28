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

Add tool section in project pyproject.toml

```toml
[tool.poem-plugins]
version_plugin = "git-long"
# Version tags must be starts with this prefix
git_version_prefix = "v"
# Create a file with version inside a project
write_version_file = true
# Save new version on pyproject
update_pyproject = true
```

Create a git tag, for example:

```console
$ git tag v0.1
```

Next, build your project. It will show an output like:

```console
$ poetry build
poem-plugins: Setting version to: 0.1.0+g5ee9240
Building awesome_package (0.1.0+g5ee9240)
  - Building sdist
  - Built awesome_package-0.1.0+g5ee9240.tar.gz
  - Building wheel
  - Built awesome_package-0.1.0+g5ee9240-py3-none-any.whl```
```
