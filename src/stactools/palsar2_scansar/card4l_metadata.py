from datetime import datetime
from typing import Any, Dict, List, Tuple, TypeVar

import pystac
from pystac.extensions.sar import Polarization, SarExtension
from pystac.extensions.sat import OrbitState, SatExtension
from pystac.utils import str_to_datetime
from shapely.geometry import mapping
from shapely.wkt import loads
from stactools.core.io.xml import XmlElement

from stactools.palsar2_scansar import constants as c

T = TypeVar("T", pystac.Item, pystac.Asset)


class MetadataLinks:
    """Read the metadata file into an object"""

    def __init__(
        self,
        granule_href: str,
        **kwargs: Any,
    ) -> None:
        self.granule_href = granule_href
        self.href = granule_href
        self.manifest = XmlElement.from_file(self.href, **kwargs)


class ProductMetadataError(Exception):
    """Class for Handling Errors in Metadata parsing"""

    pass


class ProductMetadata:
    """Parse the CARD4L Metadata"""

    def __init__(
        self,
        href: str,
        manifest: XmlElement,
    ) -> None:
        self.href = href
        self._root = manifest

        # self.resolution = self.product_id.split("_")[2][-1]

        def _get_geometries() -> Tuple[List[float], Dict[str, Any]]:
            # Find the footprint descriptor
            footprint_text = self._root.find_text_or_throw(
                ".//SourceDataGeometry", ProductMetadataError
            )
            if footprint_text is None:
                raise ProductMetadataError(
                    f"Cannot parse footprint from product metadata at {self.href}"
                )

            footprint_polygon = loads(footprint_text)
            geometry = mapping(footprint_polygon)
            bbox = list(footprint_polygon.bounds)

            return (bbox, geometry)

        self.bbox, self.geometry = _get_geometries()

    @property
    def start_datetime(self) -> datetime:
        time = self._root.find_text_or_throw(".//StartTime", ProductMetadataError)

        if time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}"
            )
        else:
            return str_to_datetime(time)

    @property
    def end_datetime(self) -> datetime:
        time = self._root.find_text_or_throw(".//EndTime", ProductMetadataError)

        if time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}"
            )
        else:
            return str_to_datetime(time)

    @property
    def get_datetime(self) -> datetime:
        start_time = self.start_datetime
        end_time = self.end_datetime

        if start_time is not None:
            central_time = start_time + (end_time - start_time) / 2

        if central_time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}"
            )
        else:
            return str_to_datetime(str(central_time))

    @property
    def get_shape(self) -> List[int]:
        rows = int(
            self._root.find_text_or_throw(".//NumberLines", ProductMetadataError)
        )
        cols = int(
            self._root.find_text_or_throw(".//NumPixelsPerLine", ProductMetadataError)
        )
        shape = [rows, cols]
        return shape

    @property
    def get_epsg(self) -> str:
        epsg = self._root.find_text_or_throw(
            ".//CoordinateReferenceSystem[@type='EPSG']", ProductMetadataError
        )
        return epsg


def fill_sar_properties(sar_ext: SarExtension[T], manifest: XmlElement) -> None:
    """Fills the properties for SAR.
    Based on the sar Extension.py
    Args:
        sar_ext (SarExtension): The extension to be populated.
        manifest (XmlElement): manifest.safe file parsed into an XmlElement
    """
    # Fixed properties
    sar_ext.frequency_band = c.SCANSAR_SAR["frequency_band"][0]
    sar_ext.center_frequency = c.SCANSAR_SAR["center_frequency"][0]
    sar_ext.observation_direction = c.SCANSAR_SAR["observation_direction"][0]

    # Read properties
    instrument_mode = manifest.find_text_or_throw(
        ".//ObservationMode", ProductMetadataError
    )
    if instrument_mode:
        sar_ext.instrument_mode = instrument_mode
    sar_ext.polarizations = [
        Polarization(x)
        for x in manifest.find_text_or_throw(
            ".//Polarizations", ProductMetadataError
        ).split(" ")
    ]
    sar_ext.product_type = c.SCANSAR_SAR["product_type"][0]

    # TODO: Decide what additional SAR properties to include
    # Properties depending on mode and resolution
    # sar.looks_range = c.SCANSAR_SAR["looks_range"]
    # sar.looks_azimuth = c.SCANSAR_SAR["looks_azimuth"]
    # sar.polarizations = c.SCANSAR_SAR["polarizations"]
    # sar.resolution_range = c.SCANSAR_SAR["resolution_range"]
    # sar.resolution_azimuth = c.SCANSAR_SAR["resolution_azimuth"]
    # sar.pixel_spacing_range = c.SCANSAR_SAR["pixel_spacing_range"]
    # sar.pixel_spacing_azimuth = c.SCANSAR_SAR["pixel_spacing_azimuth"]
    # sar.looks_equivalent_number = c.SCANSAR_SAR["looks_equivalent_number"]


def fill_sat_properties(sat_ext: SatExtension[T], manifest: XmlElement) -> None:
    """Fills the properties for SAR.
    Based on the sar Extension.py
    Args:
        sar_ext (SarExtension): The extension to be populated.
        manifest (XmlElement): manifest.safe file parsed into an XmlElement
    """
    # Fixed properties
    orbit_state = manifest.find_text_or_throw(".//PassDirection", ProductMetadataError)
    if orbit_state:
        sat_ext.orbit_state = OrbitState(orbit_state.lower())
