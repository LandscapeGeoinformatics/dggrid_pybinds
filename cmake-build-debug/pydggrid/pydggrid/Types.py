import struct
import sys
from enum import IntEnum
from typing import List, Dict, Any

from pydggrid.System import Constants


class TypeDef(IntEnum):

    @classmethod
    def values(cls) -> List[int]:
        """
        Lists all internal value elements
        :return:
        """
        return list(map(lambda c: c.value, cls))

    @classmethod
    def keys(cls) -> List[str]:
        """
        Lists all internal value elements
        :return:
        """
        return list(cls._member_names_)

    @classmethod
    def map(cls) -> Dict[str, int]:
        """
        Lists all internal value elements
        :return:
        """
        # noinspection PyTypeChecker
        return {x: int(cls._member_map_[x]) for x in cls._member_map_}


class DataType(TypeDef):
    """
    Data Type definitions
    INT = Integer
    """
    INT = 1
    FLOAT = 2
    SHORT = 3
    BINARY = 4
    STRING = 5
    SHAPE_BINARY = 6
    GDAL_GEOJSON = 7
    LOCATION = 13

    @classmethod
    def from_type(cls, input_type: type) -> Any:
        """
        Returns a data type from type hinting
        :param input_type: Input type hint
        :return: DataType object
        """
        if input_type == int:
            return DataType.INT
        if input_type == float:
            return DataType.FLOAT
        if input_type == str:
            return DataType.STRING
        if input_type == bytes:
            return DataType.BINARY

    def cast(self, input_value: Any) -> Any:
        """
        Casts a value type according to self
        :param input_value: Value to cast
        :return: Casted Value
        """
        if self.value == DataType.INT:
            return int(input_value)
        elif self.value == DataType.SHORT:
            return int(input_value)
        elif self.value == DataType.FLOAT:
            return float(input_value)
        elif self.value == DataType.BINARY:
            return struct.pack('<f', input_value)
        elif self.value == DataType.STRING:
            input_value.encode("utf8")

    def default_value(self) -> Any:
        """
        Returns default value for the data type
        :return: Defualt empty value for data type
        """
        if self.value == DataType.FLOAT:
            return self.cast(0.0)
        elif self.value == DataType.BINARY:
            return self.cast(b'')
        elif self.value == DataType.STRING:
            return self.cast("")
        else:
            return self.cast(0)

    def convert_bytes(self, input_value: Any) -> bytes:
        """
        Converts given input value to bytes according to DataType
        :param input_value: Input Value (Any)
        :return: byte array
        """
        if self.value == DataType.INT:
            return int(input_value).to_bytes(4, Constants.ENDIAN_TYPE)
        if self.value == DataType.SHORT:
            return int(input_value).to_bytes(2, Constants.ENDIAN_TYPE)
        if self.value == DataType.FLOAT:
            return struct.pack("<f", float(input_value))
        if self.value == DataType.BINARY:
            byte_array: List[bytes] = list([])
            byte_array.append(DataType.INT.convert_bytes(len(input_value)))
            byte_array.append(input_value)
            return b''.join(byte_array)
        if self.value == DataType.STRING:
            byte_array: List[bytes] = list([])
            byte_array.append(DataType.INT.convert_bytes(len(input_value)))
            byte_array.append(input_value.encode("utf8"))
            return b''.join(byte_array)


class InputAddress(TypeDef):
    """
    Defines input address type
    'GEO', # geodetic coordinates -123.36 43.22 20300 Roseburg
    'Q2DI', # quad number and (i, j) coordinates on that quad
    'SEQNUM', # DGGS index - linear address (1 to size-of-DGG), not supported for parameter
                input_address_type if dggs_aperture_type is SEQUENCE
    'Q2DD', # quad number and (x, y) coordinates on that quad
    'PROJTRI', # PROJTRI - triangle number and (x, y) coordinates within that triangle on the ISEA plane
    'VERTEX2DD', # vertex number, triangle number, and (x, y) coordinates on ISEA plane
    'AIGEN'  # Arc/Info Generate file format
    """
    NONE = 0
    GEO = 1
    Q2DI = 2
    SEQNUM = 3
    Q2DD = 4
    PROJTRI = 5
    VERTEX2DD = 6
    AIGEN = 7
    Z3 = 8,
    ZORDER = 9


class OutputAddress(TypeDef):
    """
    Output Address Type
    'GEO', # geodetic coordinates -123.36 43.22 20300 Roseburg
    'Q2DI', # quad number and (i, j) coordinates on that quad
    'SEQNUM', # DGGS index - linear address (1 to size-of-DGG), not supported for parameter input_address_type if dggs_aperture_type is SEQUENCE
    'INTERLEAVE', # digit-interleaved form of Q2DI, only supported for parameter output_address_type; only available for hexagonal aperture 3 and 4 grids
    'PLANE', # (x, y) coordinates on unfolded ISEA plane,  only supported for parameter output_address_type;
    'Q2DD', # quad number and (x, y) coordinates on that quad
    'PROJTRI', # PROJTRI - triangle number and (x, y) coordinates within that triangle on the ISEA plane
    'VERTEX2DD', # vertex number, triangle number, and (x, y) coordinates on ISEA plane
    'AIGEN'  # Arc/Info Generate file format
    """
    GEO = 1
    Q2DI = 2
    SEQNUM = 3
    INTERLEAVE = 4
    PLANE = 5
    Q2DD = 6
    PROJTRI = 7
    VERTEX2DD = 8
    AIGEN = 9
    Z3 = 10
    ZORDER = 11


class Topology(TypeDef):
    """
    Defines DGGS Topologies
    "HEXAGON" Hexagon
    "TRIANGLE" Tri
    "DIAMOND" Diamond
    """
    HEXAGON = 1
    TRIANGLE = 2
    DIAMOND = 3


class Aperture(TypeDef):
    """
    Defines DGGS Aperture types
    "PURE"
    "MIXED43"
    "SEQUENCE"
    """
    PURE = 1
    MIXED43 = 2
    SEQUENCE = 3


class ClipMethod(TypeDef):
    """
    POLY_INTERSECT = Polygonal Intersect
    """
    POLY_INTERSECT = 1


class ClipType(TypeDef):
    """
    WHOLE_EARTH
    AIGEN
    SHAPEFILE
    GDAL
    SEQNUMS
    ADDRESSES
    POINTS
    COARSE_CELLS
    INPUT_ADDRESS_TYPE
    """
    WHOLE_EARTH: int = 1
    AIGEN: int = 2
    SHAPEFILE: int = 3
    GDAL: int = 4
    SEQNUMS: int = 5
    ADDRESSES: int = 6
    POINTS: int = 7
    COARSE_CELLS: int = 8
    INPUT_ADDRESS_TYPE: int = 9


class DGGSType(TypeDef):
    """
    "CUSTOM",  # parameters will be specified manually
    "SUPERFUND",  # Superfund_500m grid
    "PLANETRISK",
    "ISEA3H",  # ISEA projection with hexagon cells and an aperture of 3
    "ISEA4H",  # ISEA projection with hexagon cells and an aperture of 4
    "ISEA4T",  # ISEA projection with triangle cells and an aperture of 4
    "ISEA4D",  # ISEA projection with diamond cells and an aperture of 4
    "ISEA43H",  # ISEA projection with hexagon cells and a mixed sequence of aperture 4 resolutions followed by aperture 3 resolutions
    "ISEA7H",  # ISEA projection with hexagon cells and an aperture of 7
    "FULLER3H",  # FULLER projection with hexagon cells and an aperture of 3
    "FULLER4H",  # FULLER projection with hexagon cells and an aperture of 4
    "FULLER4T",  # FULLER projection with triangle cells and an aperture of 4
    "FULLER4D",  # FULLER projection with diamond cells and an aperture of 4
    "FULLER43H",  # FULLER projection with hexagon cells and a mixed sequence of aperture 4 resolutions followed by aperture 3 resolutions
    "FULLER7H",  # FULLER projection with hexagon cells and an aperture of 7
    """
    CUSTOM = 0
    SUPERFUND = 1
    PLANETRISK = 2
    ISEA3H = 3
    ISEA4H = 4
    ISEA4T = 5
    ISEA4D = 6
    ISEA43H = 7
    ISEA7H = 8
    FULLER3H = 9
    FULLER4H = 10
    FULLER4T = 11
    FULLER4D = 12
    FULLER43H = 13
    FULLER7H = 14
    IGEO7 = 15


class DGGSPoly(TypeDef):
    """
    ICOSAHEDRON
    """
    ICOSAHEDRON = 1


class Operation(TypeDef):
    """
    GENERATE_GRID
    GENERATE_GRID_FROM_POINTS
    BIN_POINT_VALS
    BIN_POINT_PRESENCE
    TRANSFORM_POINTS
    OUTPUT_STATS
    """
    CUSTOM = 0
    GENERATE_GRID = 1
    GENERATE_GRID_FROM_POINTS = 2
    BIN_POINT_VALS = 3
    BIN_POINT_PRESENCE = 4
    TRANSFORM_POINTS = 5
    OUTPUT_STATS = 6


class DGGSProjection(TypeDef):
    """
    dggs_proj <ISEA | FULLER | GNOMONIC>
    ISEA
    FULLER
    GNOMONIC
    """
    ISEA = 1
    FULLER = 2
    GNOMONIC = 3


class RandomGenerator(TypeDef):
    """
    RAND
    MOTHER
    """
    RAND = 1
    MOTHER = 2


class ProjectionDatum(TypeDef):
    """
    proj_datum <WGS84_AUTHALIC_SPHERE WGS84_MEAN_SPHERE CUSTOM_SPHERE>
    WGS84_AUTHALIC_SPHERE
    WGS84_MEAN_SPHERE
    CUSTOM_SPHERE
    """
    WGS84_AUTHALIC_SPHERE = 1
    WGS84_MEAN_SPHERE = 2
    CUSTOM_SPHERE = 3


class OrientationType(TypeDef):
    """
    dggs_orient_specify_type <RANDOM | SPECIFIED | REGION_CENTER>
    RANDOM
    SPECIFIED
    REGION_CENTER
    """
    RANDOM = 1
    SPECIFIED = 2
    REGION_CENTER = 3


class ResolutionType(TypeDef):
    """
    <SPECIFIED | CELL_AREA | INTERCELL_DISTANCE>
    SPECIFIED
    CELL_AREA
    INTERCELL_DISTANCE
    """
    SPECIFIED = 1
    CELL_AREA = 2
    INTERCELL_DISTANCE = 3


class AddressField(TypeDef):
    """
    FIRST_FIELD | NAMED_FIELD | GEO_POINT
    FIRST_FIELD
    NAMED_FIELD
    GEO_POINT
    """
    FIRST_FIELD = 1
    NAMED_FIELD = 2
    GEO_POINT = 3


class PointDataType(TypeDef):
    """
    NONE | TEXT | GDAL
    NONE
    TEXT
    GDAL
    """
    NONE = 1
    TEXT = 2
    GDAL = 3
    GEOJSON = 4


class BinCoverage(TypeDef):
    """
    BinCoverage
    GLOBAL
    PARTIAL
    """
    GLOBAL = 1
    PARTIAL = 2


class OutputControl(TypeDef):
    """
    cell_output_control <OUTPUT_ALL | OUTPUT_OCCUPIED>
    OUTPUT_ALL
    OUTPUT_OCCUPIED
    """
    OUTPUT_ALL = 1
    OUTPUT_OCCUPIED = 2


class OutputType(TypeDef):
    """
     output_file_type <NONE | TEXT >
    """
    NONE = 1
    TEXT = 2


class LongitudeWrap(TypeDef):
    """
    longitude_wrap_mode < WRAP | UNWRAP_WEST | UNWRAP_EAST >
    WRAP
    UNWRAP_WEST
    UNWRAP_EAST
    """
    WRAP = 1
    UNWRAP_WEST = 2
    UNWRAP_EAST = 3


class CellLabel(TypeDef):
    """
    output_cell_label_type <GLOBAL_SEQUENCE | ENUMERATION | SUPERFUND | OUTPUT_ADDRESS_TYPE >
    GLOBAL_SEQUENCE
    ENUMERATION
    SUPERFUND
    OUTPUT_ADDRESS_TYPE
    """
    GLOBAL_SEQUENCE = 1
    ENUMERATION = 2
    SUPERFUND = 3
    OUTPUT_ADDRESS_TYPE = 4


class CellOutput(TypeDef):
    """
    cell_output_type <NONE | AIGEN | GDAL | KML | GEOJSON | SHAPEFILE | GDAL_COLLECTION>
    NONE
    AIGEN
    GDAL
    KML
    GEOJSON
    SHAPEFILE
    GDAL_COLLECTION
    """
    NONE = 1
    AIGEN = 2
    GDAL = 3
    KML = 4
    GEOJSON = 5
    SHAPEFILE = 6
    GDAL_COLLECTION = 7


class PointOutput(TypeDef):
    """
    point_output_type <NONE | AIGEN | GDAL | KML | GEOJSON | SHAPEFILE | TEXT | GDAL_COLLECTION>
    NONE
    AIGEN
    GDAL
    KML
    GEOJSON
    SHAPEFILE
    GDAL_COLLECTION
    """
    NONE = 1
    AIGEN = 2
    GDAL = 3
    KML = 4
    GEOJSON = 5
    SHAPEFILE = 6
    GDAL_COLLECTION = 7


class ReadMode(TypeDef):
    """
    ReadMode <NONE | AIGEN | GDAL | KML | GEOJSON | SHAPEFILE | GDAL_COLLECTION>
    NONE
    AIGEN
    GDAL
    KML
    GEOJSON
    SHAPEFILE
    GDAL_COLLECTION
    """
    NONE = 1
    AIGEN = 2
    GDAL = 3
    KML = 4
    GEOJSON = 5
    SHAPEFILE = 6
    GDAL_COLLECTION = 7
    SEQUENCE = 8
    FRAME = 9


class RandPointOutput(TypeDef):
    """
    randpts_output_type <NONE | AIGEN | GDAL | KML | GEOJSON | SHAPEFILE | TEXT>
    NONE
    AIGEN
    GDAL
    KML
    GEOJSON
    SHAPEFILE

    """
    NONE = 1
    AIGEN = 2
    GDAL = 3
    KML = 4
    GEOJSON = 5
    SHAPEFILE = 6
    TEXT = 7


class NeighborOutput(TypeDef):
    """
    neighbor_output_type <NONE | TEXT | GEOJSON_COLLECTION>
    NONE
    TEXT
    GEOJSON_COLLECTION
    """
    NONE = 1
    TEXT = 2
    GEOJSON_COLLECTION = 3
    GDAL_COLLECTION = 4


class ChildrenOutput(TypeDef):
    """
    children_output_type <NONE | TEXT | GEOJSON_COLLECTION>
    NONE
    TEXT
    GEOJSON_COLLECTION
    """
    NONE = 1
    TEXT = 2
    GEOJSON_COLLECTION = 3
    GDAL_COLLECTION = 4


class GDALFormat(TypeDef):
    """
    GDAL Format for GDAL outputs
    KML = 1
    GEOJSON = 2
    """
    KML = 4
    GEOJSON = 5
    # these should be more performant acttually
    # FlatGeobuf = 6
    # GPKG = 7
