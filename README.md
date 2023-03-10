# stactools-palsar2-scansar

[![PyPI](https://img.shields.io/pypi/v/stactools-palsar2-scansar)](https://pypi.org/project/stactools-palsar2-scansar/)

- Name: palsar2-scansar
- Package: `stactools.palsar2_scansar`
- [stactools-palsar2-scansar on PyPI](https://pypi.org/project/stactools-palsar2-scansar/)
- Owner: @wildintellect
- [Dataset homepage](https://www.eorc.jaxa.jp/ALOS/en/dataset/palsar2_l22_e.htm)
- STAC extensions used:
  - [projection](https://github.com/stac-extensions/projection/)
  - [sar](https://github.com/stac-extensions/sar)
  - [sat](https://github.com/stac-extensions/sat)
  - [raster](https://github.com/stac-extensions/raster)
  - [eo](https://github.com/stac-extensions/eo)
- [Browse the example in human-readable form](https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/stactools-packages/palsar2-scansar/main/examples/collection.json)

[stactools](https://github.com/stac-utils/stactools) package for use with
the JAXA ALOS-2 Palsar-2 Scansar, Normalised Radar Backscatter (NRB),
products in Cloud Optimized Geotiff format.

## STAC Examples

- [Collection](examples/collection.json)
- [Item](examples/ALOS2437590500-220630_WWDR2.2GUA/ALOS2437590500-220630_WWDR2.2GUA.json)

## Installation

```shell
pip install stactools-palsar2-scansar
```

## Command-line Usage

Description of the command line functions

```shell
stac palsar2-scansar create-collection <destination/>

stac palsar2-scansar create-item <source.xml> <destination/>
stac palsar2-scansar create-item \
https://jaxaalos2.s3.us-west-2.amazonaws.com/palsar2/L2.2/For_STAC/ALOS2397743750-211004_WBDR2.2GUD_summary.xml \
examples/
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
