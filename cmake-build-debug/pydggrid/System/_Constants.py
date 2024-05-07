import math
from typing import List


class Dictionary:
    """
    System Constants
    """
    MAX_DGG_RES: int = 35
    DEFAULT_DGG_RES: int = 9
    DEFAULT_RAND_SEED: int = 77316727
    MAXIMUM_DENSIFICATION: int = 500
    DEFAULT_PRECISION: int = 7
    MAXIMUM_VERBOSITY: int = 3
    MAXIMUM_INT: int = 2147483647
    MAXIMUM_ID_FIELD_LEN: int = 50
    MAXIMUM_DATUM_RADIUS: float = 10000.00
    MAXIMUM_GEO_DENSIFY: float = float(360.0)
    APERTURE_VALUES: List[int] = [3, 4, 7]
    LONGITUDE_LIMITS: List[float] = [-180.0, 180.0]
    LATITUDE_LIMITS: List[float] = [-90.0, 90.0]
    AZIMUTH_LIMITS: List[float] = [0.0, 360.0]
    VERT0_LONGITUDE_DEFAULT: float = 11.25
    CENTER_LONGITUDE_DEFAULT: float = 0.0
    VERT0_LATITUDE_DEFAULT: float = 58.28252559
    CENTER_LATITUDE_DEFAULT: float = 0
    VERT0_AZIMUTH_DEFAULT: float = 0.0
    MAXIMUM_INTERCELL_DISTANCE: float = (2.0 * math.pi * 6500.0)
    DEFAULT_INTERCELL_DISTANCE: float = 100.00
    MAXIMUM_RESOLUTION_AREA: float = (4.0 * math.pi * 6500.0)
    DEFAULT_RESOLUTION_AREA: float = 100.00
    DEFAULT_COUNT_FIELD_NAME: str = "count"
    DEFAULT_VALUE_FIELD_NAME: str = "value"
    DEFAULT_TOTAL_FIELD_NAME: str = "total"
    DEFAULT_MEAN_FIELD_NAME: str = "mean"
    DEFAULT_PRESENCE_FIELD_NAME: str = "presVec"
    DEFAULT_N_CLASS_FIELD_NAME: str = "numClass"
    DEFAULT_OUTPUT_FILE_NAME: str = "valsout.txt"
    DEFAULT_CELL_OUTPUT_FILE: str = "cells"
    DEFAULT_POINTS_OUTPUT_FILE: str = "centers"
    DEFAULT_RAND_POINTS_OUTPUT_FILE: str = "randPts"
    DEFAULT_COLLECTION_OUTPUT_FILE: str = "centers"
    DEFAULT_NEIGHBOR_OUTPUT_FILE: str = "nbr"
    DEFAULT_CHILDREN_OUTPUT_FILE: str = "chld"
    DEFAULT_DGGS_ORIENT_OUTPUT_FILE: str = "grid.meta"
    DEFAULT_GDAL_FORMAT: str = "GeoJSON"
    DEFAULT_DELIMITER: str = "\" \""
    MAXIMUM_KML_WIDTH: int = 100
    DEFAULT_KML_WIDTH: int = 4
    DEFAULT_KML_COLOR: str = "ffffffff"
    DEFAULT_KML_DESC: str = "dgpy[q]"
    DEFAULT_KML_NAME: str = ""
    ENDIAN_TYPE = "little"
    ENDIAN_CODE = "little"