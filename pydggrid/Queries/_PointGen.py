import pathlib
from typing import Any, Dict, List

import geojson
import geopandas
import libpydggrid
import numpy
import pandas
import pyarrow

from pydggrid.Modules import Input
from pydggrid.Output import Records, Geometry
from pydggrid.Types import Operation, ReadMode, PointDataType, OutputType, OutputAddress, CellOutput, OutputControl, \
    BinCoverage, PointOutput
from pydggrid.Queries._Custom import Query as BaseQuery


class Query(BaseQuery):
    """
    Base Generate Grid Query
    - clip: clip settings configured with set_clip, by default set to WHOLE_EARTH, AKA. "Auto()"
    - cells: Cells response from DGGRID
    - points: Points response from DGGRID
    - Meta: Query meta-data object
    """

    def __init__(self):
        """
        Default constructor
        """
        super().__init__(Operation.GENERATE_GRID_FROM_POINTS)
        self._input: Input = Input()
        self.cells: Geometry = Geometry()
        self.points: Geometry = Geometry()
        self.indexes: Records = Records()
        self.dgg_meta: str = ""
        self.Meta.save("output_address_type", OutputAddress.SEQNUM)
        self.Meta.save("output_file_type", OutputType.TEXT)
        self.Meta.save("cell_output_type", CellOutput.GDAL)
        self.Meta.save("point_output_type", PointOutput.GDAL)
        self.Meta.save("bin_coverage", BinCoverage.GLOBAL)
        self.Meta.save("cell_output_control", OutputControl.OUTPUT_ALL)
        self.Meta.save("cell_output_gdal_format", "GeoJSON")
        self.Meta.save("point_output_gdal_format", "GeoJSON")

        # Set defaults

    def __bytes__(self) -> bytes:
        """
        Returns query bytes
        :return: Clip Bytes
        """
        return self._input.__bytes__()

    def set_output(self, mode: OutputControl = OutputControl.OUTPUT_ALL) -> None:
        """
        Sets output control mode
        :param mode: Output Control Mode
        :return:None
        """
        self.Meta.save("cell_output_control", mode)

    def set_coverage(self, mode: BinCoverage = BinCoverage.GLOBAL) -> None:
        """
        Sets the point coverage mode
        :param mode: Coverage control mode refers to Types.BinCoverage
        :return: None
        """
        self.Meta.save("bin_coverage", mode)

    def input_points(self,
                     records: [List,
                               Dict,
                               str,
                               pathlib.Path,
                               pandas.DataFrame,
                               geopandas.geoseries,
                               geopandas.GeoDataFrame,
                               numpy.ndarray,
                               pyarrow.Array,
                               pyarrow.Table,
                               geojson.GeoJSON],
                     definition: [List[str],
                                  List[int],
                                  str,
                                  None] = None) -> None:
        """
        Inputs point collection
        :param records: Records to save into the buffer, this parameter can be:
            - A path string or a pathlib.Path object point to file that is readable by the read parameter.
            - A List of X, Y points as tuples.
            - A string value containing either space delimited or csv data
            - a pandas dataframe, which should contain X, Y and optionally ID and Label fields.
            - a geopandas dataframe, which should contain a geometry field with points
            - a 2 dimensional numpy array which contains x, y coordinates
            - A dictionary or a list of dictionaries containing an x, y, and optionally an id and label column
            - a geojson dictionary object
            - A pyarrow geometry Array containing x, y coordinates
            - a pyarrow table with x, y coordinate columns with optional id and label columns
            field is assumed as `geometry`.
        :param definition: Columns definition data, for most items this is a string declaring the geometry columns used.
            Example:
                {
                    "x": <column index or name pointing to x field, default is 0 or "x" or "X">
                    "y": <column index or name pointing to y field, default is 1 or "y" or "Y">,
                    "id": <optional field pointing to an id column or column index, by default point index will be
                    used.>
                    "label": <optional field pointing to a label column or column index, by default 'point-(index + 1)
                    will be used.>,
                    "geometry": Geometry column to use, optionally this field can be provided in lue of x, y columns
                }
        :return: None
        """
        self.Meta.save("point_input_file_type", PointDataType.GDAL)
        self._input.points(records, definition)

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadPayload(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        return libpydggrid.UnitTest_ReadPayload(self.Meta.dict(), self._input.__bytes__())

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytearray = bytearray(self._input.__bytes__())
        return libpydggrid.UnitTest_ReadQuery(dictionary, list(payload))

    # Override
    # noinspection PyPep8Naming
    def UnitTest_RunQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytearray = bytearray(self._input.__bytes__())
        return libpydggrid.UnitTest_RunQuery(dictionary, list(payload))

    # Override
    def run(self, byte_data: [bytes, None] = None) -> None:
        """
        Runs the query
        :param byte_data byte payload, if left blank Input.__bytes__() will be used
        :return: None
        """
        byte_data: Dict[str, bytes] = super().exec(self._input.__bytes__())
        self.dgg_meta = bytearray(byte_data["meta"]).decode() if "meta" in byte_data else ""
        #
        self.cells.save(byte_data["cells"], ReadMode.GEOJSON)
        self.points.save(byte_data["points"], ReadMode.GEOJSON)
        #
        record_set: List[Dict[str, Any]] = list()
        elements: List[str] = bytearray(byte_data["dataset"]).decode().split("\n")
        for element_node in elements:
            if len(element_node.strip()) > 0:
                vectors: List[str] = element_node.split(" ")
                names: List[str] = self.indexes.get_columns()
                record_set.append({names[i]: self._get_value(i, vectors) for i in range(0, len(names))})
        self.indexes.save(pandas.DataFrame(record_set), ReadMode.FRAME)

    # noinspection PyMethodMayBeStatic
    def _get_value(self, index: int, data: List[str]) -> float:
        """
        Converts incoming value
        :param index: Node Index
        :param data:  Node Data
        :return: Node Value
        """
        if index < len(data):
            if len(str(data[index]).strip()) > 0:
                return float(str(data[index]).strip())
        return 0.0

    # INTERNAL
