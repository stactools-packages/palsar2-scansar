from datetime import datetime
from typing import Any, Dict, Optional

import pystac
from pystac import Extent, Link, Provider
from pystac import ProviderRole as PR
from pystac import SpatialExtent, TemporalExtent
from pystac.extensions import sar
from pystac.extensions.eo import Band
from pystac.extensions.item_assets import AssetDefinition
from pystac.extensions.raster import DataType
from pystac.utils import str_to_datetime

# Time must be in UTC
SCANSAR_COLLECTION_START: Optional[datetime] = str_to_datetime("2014-08-04T00:00:00Z")
SCANSAR_TEMPORAL_EXTENT = TemporalExtent([[SCANSAR_COLLECTION_START, None]])

# TODO: update to match bucket
SCANSAR_SPATIAL_EXTENT = SpatialExtent([-180.0, -56, 180.0, 85.0])

SCANSAR_EXTENT = Extent(SCANSAR_SPATIAL_EXTENT, SCANSAR_TEMPORAL_EXTENT)

SCANSAR_PALSAR_PROVIDERS = [
    Provider(
        "Japan Aerospace Exploration Agency",
        roles=[PR.PRODUCER, PR.PROCESSOR, PR.LICENSOR],
        url="https://www.eorc.jaxa.jp/ALOS/en/dataset/fnf_e.htm",
    ),
    Provider(
        "Japan Aerospace Exploration Agency",
        roles=[PR.HOST],
        url="https://registry.opendata.aws/jaxa-alos-palsar2-scansar/",
    ),
]
SCANSAR_DESCRIPTION = """The new PALSAR-2 ScanSAR products have been developed to conform with the CEOS-ARD format specifications for Normalised Radar Backscatter (CARD4L NRB). The NRB products have been subject to ortho-rectification and Radiometric Terrain Correction (RTC), and are provided in the Gamma-0 backscatter convention, which mitigates the variations from diverse observation geometries. The products include HH and HV polarisation backscatter, local incidence angle image and data mask."""  # noqa: E501

SCANSAR_REVISION = "E"

SCANSAR_LINKS = [
    Link(
        rel="documentation",
        target=("https://www.eorc.jaxa.jp/ALOS/en/dataset/palsar2_l22_e.htm"),
        media_type=pystac.MediaType.HTML,
        title="ALOS-2 PALSAR-2 ScanSAR Products",
    ),
    Link(
        rel="documentation",
        target=("PALSAR2_CARD4L_L2.2_Geotiff_Format_Description_E_20220715.pdf"),
        media_type=pystac.MediaType.PDF,
        title="PALSAR-2 ScanSAR NRB L2.2. Geotiff Format description",
        extra_fields={"description": "Also includes data usage information"},
    ),
    Link(
        rel="documentation",
        target=("https://ceos.org/ard/files/PFS/NRB/v5.5/CARD4L-PFS_NRB_v5.5.pdf"),
        media_type=pystac.MediaType.PDF,
        title="CARD4L CEOS-ARD NRB description",
    ),
    Link(
        rel="license",
        target="https://earth.jaxa.jp/policy/en.html",
        title="JAXA Terms of Use of Research Data",
        media_type=pystac.MediaType.HTML,
    ),
]


SCANSAR_PALSAR_PLATFORMS = ["ALOS2"]
SCANSAR_PALSAR_INSTRUMENTS = ["PALSAR-2"]
SCANSAR_PALSAR_GSD = 25  # meters
SCANSAR_PALSAR_EPSG = 4326
SCANSAR_PALSAR_CF = "83.0 dB"

SCANSAR_SAR: Dict[str, Any] = {
    "looks_range": [1],
    "product_type": ["GRD"],
    "looks_azimuth": [1],
    "polarizations": [sar.Polarization.HH, sar.Polarization.HV],
    "frequency_band": [sar.FrequencyBand.L],
    "instrument_mode": ["WBD", "WBS"],
    "center_frequency": [1.23650],
    "resolution_range": [19],
    "resolution_azimuth": [25.9],
    "pixel_spacing_range": [8.583],
    "observation_direction": [sar.ObservationDirection.RIGHT],
    "pixel_spacing_azimuth": [325.003],
    "looks_equivalent_number": [2.7],
}

SCANSAR_POLARIZATIONS = {
    "HH_SLP": Band.create(
        name="HH",
        description="HH band: horizontal transmit and horizontal receive",
    ),
    "HV_SLP": Band.create(
        name="HV",
        description="HV band: horizontal transmit and vertical receive",
    ),
}

SCANSAR_ASSETS: Dict[str, AssetDefinition] = {
    "HH_SLP": AssetDefinition(
        {
            "title": "HH",
            "type": pystac.MediaType.COG,
            "description": "HH polarization backscattering coefficient, 16-bit DN.",
            "role": "data",
        }
    ),
    "HV_SLP": AssetDefinition(
        {
            "title": "HV",
            "type": pystac.MediaType.COG,
            "description": "HV polarization backscattering coefficient, 16-bit DN.",
            "role": "data",
        }
    ),
    "LIN": AssetDefinition(
        {
            "title": "linci",
            "type": pystac.MediaType.COG,
            "description": "Local incidence angle (degrees).",
            "role": ["data", "local-incidence-angle"],
        }
    ),
    "MSK": AssetDefinition(
        {
            "title": "mask",
            "type": pystac.MediaType.COG,
            "description": "Quality Mask",
            "role": ["data", "data-mask"],
        }
    ),
    "summary": AssetDefinition(
        {
            "title": "summary",
            "type": pystac.MediaType.XML,
            "description": "CARD4L Metadata",
            "role": "metadata",
        }
    ),
    "kml": AssetDefinition(
        {
            "title": "kml",
            "type": "application/vnd.google-earth.kml+xml",
            "description": "Footprint Preview",
            "role": "overview",
        }
    ),
}


SCANSAR_BANDS = {
    "HH_SLP": {
        "data_type": DataType.UINT16,
    },
    "HV_SLP": {
        "data_type": DataType.UINT16,
    },
    "LIN": {
        "data_type": DataType.UINT8,
    },
    "MSK": {
        "data_type": DataType.UINT8,
    },
}
