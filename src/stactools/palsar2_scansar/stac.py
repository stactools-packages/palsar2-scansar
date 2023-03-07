import logging
import os
from datetime import datetime, timezone
from typing import Any

import rasterio
from pystac import Collection, Extent, Item, SpatialExtent, Summaries, TemporalExtent
from pystac.extensions.eo import EOExtension
from pystac.extensions.item_assets import ItemAssetsExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import RasterExtension
from pystac.extensions.sar import SarExtension
from pystac.extensions.sat import SatExtension

from stactools.palsar2_scansar import constants as c

from .card4l_metadata import (
    MetadataLinks,
    ProductMetadata,
    fill_sar_properties,
    fill_sat_properties,
)

# from pystac.extensions.sat import SatExtension


logger = logging.getLogger(__name__)


def create_collection() -> Collection:
    """Create a STAC Collection

    This function includes logic to extract all relevant metadata from
    an asset describing the STAC collection and/or metadata coded into an
    accompanying constants.py file.

    See `Collection<https://pystac.readthedocs.io/en/latest/api.html#collection>`_.

    Returns:
        Collection: STAC Collection object
    """

    # Time must be in UTC
    demo_time = datetime.now(tz=timezone.utc)

    extent = Extent(
        SpatialExtent([[-180.0, 90.0, 180.0, -90.0]]),
        TemporalExtent([[demo_time, None]]),
    )

    summary_dict = {
        "platform": c.SCANSAR_PALSAR_PLATFORMS,
    }

    collection = Collection(
        id="palsar2-scansar",
        title="ALOS-2 PALSAR-2 ScanSAR",
        description=c.SCANSAR_DESCRIPTION,
        providers=c.SCANSAR_PALSAR_PROVIDERS,
        extent=extent,
        summaries=Summaries(summary_dict),
        stac_extensions=[
            ItemAssetsExtension.get_schema_uri(),
            ProjectionExtension.get_schema_uri(),
            RasterExtension.get_schema_uri(),
            SarExtension.get_schema_uri(),
            SatExtension.get_schema_uri(),
            EOExtension.get_schema_uri(),
        ],
    )

    # Links
    collection.add_links(c.SCANSAR_LINKS)

    # SAR Extension
    sar = SarExtension.summaries(collection, add_if_missing=True)
    sar.looks_range = c.SCANSAR_SAR["looks_range"]
    sar.product_type = c.SCANSAR_SAR["product_type"]
    sar.looks_azimuth = c.SCANSAR_SAR["looks_azimuth"]
    sar.polarizations = c.SCANSAR_SAR["polarizations"]
    sar.frequency_band = c.SCANSAR_SAR["frequency_band"]
    sar.instrument_mode = c.SCANSAR_SAR["instrument_mode"]
    sar.center_frequency = c.SCANSAR_SAR["center_frequency"]
    sar.resolution_range = c.SCANSAR_SAR["resolution_range"]
    sar.resolution_azimuth = c.SCANSAR_SAR["resolution_azimuth"]
    sar.pixel_spacing_range = c.SCANSAR_SAR["pixel_spacing_range"]
    sar.pixel_spacing_azimuth = c.SCANSAR_SAR["pixel_spacing_azimuth"]
    sar.looks_equivalent_number = c.SCANSAR_SAR["looks_equivalent_number"]

    assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    assets.item_assets = c.SCANSAR_ASSETS

    return collection


def create_item(
    granule_href: str,
    **kwargs: Any,
) -> Item:
    """Create a STAC Item

    This function should include logic to extract all relevant metadata from an
    asset, metadata asset, and/or a constants.py file.

    See `Item<https://pystac.readthedocs.io/en/latest/api.html#item>`_.
    Example:
        ALOS2397743750-211004_WBDR2.2GUD_summary.xml

    Args:
        granule_href (str): The HREF pointing to a granule summary xml

    Returns:
        Item: STAC Item object
    """

    metalinks = MetadataLinks(
        granule_href,
        **kwargs,
    )

    granule_id = granule_href.replace("_summary.xml", "")
    product_metadata = ProductMetadata(granule_href, metalinks.manifest)

    asset_href = f"{granule_id}_HH_SLP.tif"
    with rasterio.open(asset_href) as dataset:
        bbox = list(dataset.bounds)
        # geometry = mapping(box(*bbox))
        # transform = dataset.transform
        # shape = dataset.shape

        item = Item(
            id=os.path.basename(granule_id),
            properties={},
            geometry=product_metadata.geometry,
            bbox=product_metadata.bbox,
            datetime=product_metadata.get_datetime,
            stac_extensions=[],
        )

        # It is a good idea to include proj attributes to optimize for libs like stac-vrt
        proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
        proj_attrs.epsg = dataset.crs.to_epsg()
        proj_attrs.bbox = bbox
        proj_attrs.shape = product_metadata.get_shape  # Raster shape ProductImageSize
        # proj_attrs.transform = [-180, 360, 0, 90, 0, 180]  # Raster GeoTransform

    # -- Add Extensions --
    # sar
    # sar = SarExtension.ext(item, add_if_missing=True)

    # TODO: get list of assets from metadata
    assets_dict = {
        "HH_SLP": f"{granule_id}_HH_SLP.tif",
        "HV_SLP": f"{granule_id}_HV_SLP.tif",
        "MSK": f"{granule_id}_MSK.tif",
        "LIN": f"{granule_id}_LIN.tif",
        "summary": granule_href,
        "kml": f"{granule_id}.kml",
    }

    # Add an asset to the item
    # Keeps the asset hrefs relative
    for key, value in assets_dict.items():
        if (asset_def := c.SCANSAR_ASSETS.get(key)) is not None:
            asset = asset_def.create_asset(os.path.basename(value))

            if (band := c.SCANSAR_POLARIZATIONS.get(key)) is not None:
                asset_eo = EOExtension.ext(asset)
                asset_eo.bands = [band]
            item.add_asset(key, asset)

    # SAR extension
    sar = SarExtension.ext(item, add_if_missing=True)
    fill_sar_properties(sar, metalinks.manifest)

    # SAT extension
    sat = SatExtension.ext(item, add_if_missing=True)
    fill_sat_properties(sat, metalinks.manifest)

    # eo extension

    return item
