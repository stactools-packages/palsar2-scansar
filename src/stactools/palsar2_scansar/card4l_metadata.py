from datetime import datetime
from typing import Any, Dict, List, Tuple

from pystac.utils import str_to_datetime
from shapely.geometry import mapping
from shapely.wkt import loads
from stactools.core.io.xml import XmlElement


class MetadataLinks:
    """Read the metadata file into an object"""

    def __init__(
        self,
        granule_href: str,
        **kwargs: Any,
    ) -> None:
        self.granule_href = granule_href
        self.href = f"{granule_href}_summary.xml"

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
            central_time = (
                datetime.strptime(str(start_time), "%Y-%m-%dT%H:%M:%S.%f+00.00")
                + (
                    datetime.strptime(str(end_time), "%Y-%m-%dT%H:%M:%S.%f+00.00")
                    - datetime.strptime(str(start_time), "%Y-%m-%dT%H:%M:%S.%f+00.00")
                )
                / 2
            )

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
