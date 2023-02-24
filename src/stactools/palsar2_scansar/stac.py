import logging
from datetime import datetime, timezone

from pystac import (
    Asset,
    Collection,
    Extent,
    Item,
    MediaType,
    SpatialExtent,
    Summaries,
    TemporalExtent,
)
from pystac.extensions.eo import EOExtension
from pystac.extensions.item_assets import ItemAssetsExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import RasterExtension
from pystac.extensions.sar import SarExtension
from pystac.extensions.sat import SatExtension

from stactools.palsar2_scansar import constants as c

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

    assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    assets.item_assets = c.SCANSAR_ASSETS

    return collection


def create_item(asset_href: str) -> Item:
    """Create a STAC Item

    This function should include logic to extract all relevant metadata from an
    asset, metadata asset, and/or a constants.py file.

    See `Item<https://pystac.readthedocs.io/en/latest/api.html#item>`_.

    Args:
        asset_href (str): The HREF pointing to an asset associated with the item

    Returns:
        Item: STAC Item object
    """

    properties = {
        "title": "A dummy STAC Item",
        "description": "Used for demonstration purposes",
    }

    demo_geom = {
        "type": "Polygon",
        "coordinates": [[[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]]],
    }

    # Time must be in UTC
    demo_time = datetime.now(tz=timezone.utc)

    item = Item(
        id="my-item-id",
        properties=properties,
        geometry=demo_geom,
        bbox=[-180, 90, 180, -90],
        datetime=demo_time,
        stac_extensions=[],
    )

    # It is a good idea to include proj attributes to optimize for libs like stac-vrt
    proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
    proj_attrs.epsg = 4326
    proj_attrs.bbox = [-180, 90, 180, -90]
    proj_attrs.shape = [1, 1]  # Raster shape
    proj_attrs.transform = [-180, 360, 0, 90, 0, 180]  # Raster GeoTransform

    # Add an asset to the item (COG for example)
    item.add_asset(
        "image",
        Asset(
            href=asset_href,
            media_type=MediaType.COG,
            roles=["data"],
            title="A dummy STAC Item COG",
        ),
    )

    return item
