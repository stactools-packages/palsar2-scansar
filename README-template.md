# stactools-palsar2-scansar

[![PyPI](https://img.shields.io/pypi/v/stactools-palsar2-scansar)](https://pypi.org/project/stactools-palsar2-scansar/)

- Name: palsar2-scansar
- Package: `stactools.palsar2_scansar`
- [stactools-palsar2-scansar on PyPI](https://pypi.org/project/stactools-palsar2-scansar/)
- Owner: @githubusername
- [Dataset homepage](http://example.com)
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
- Extra fields:
  - `palsar2-scansar:custom`: A custom attribute
- [Browse the example in human-readable form](https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/stactools-packages/palsar2-scansar/main/examples/collection.json)

A short description of the package and its usage.

## STAC Examples

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

## Installation

```shell
pip install stactools-palsar2-scansar
```

## Command-line Usage

Description of the command line functions

```shell
stac palsar2-scansar create-item source destination
```

Use `stac palsar2-scansar --help` to see all subcommands and options.

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
pip install -e .
pip install -r requirements-dev.txt
pre-commit install
```

To check all files:

```shell
pre-commit run --all-files
```

To run the tests:

```shell
pytest -vv
```
