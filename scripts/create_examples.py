#!/usr/bin/env python3
"""
Generate example STAC from test data
"""
import shutil
from pathlib import Path

import pystac

from stactools.palsar2_scansar import stac

# GRD generate examples
root = Path(__file__).parents[1]
examples = root / "examples"
scansar_data = root / "tests" / "data-files"

shutil.rmtree(examples, ignore_errors=True)

stac_collection = stac.create_collection()

item1 = stac.create_item(
    str(scansar_data / "ALOS2437590500-220630_WWDR2.2GUA_summary.xml"),
)

stac_collection.add_items([item1])

stac_collection.normalize_hrefs(str(examples))
stac_collection.make_all_asset_hrefs_relative()
stac_collection.validate_all()
stac_collection.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
