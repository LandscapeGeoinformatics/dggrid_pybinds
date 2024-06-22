from typing import Any, Dict

import libpydggrid

import pydggrid.Output
from pydggrid.Input import Auto, InputTemplate, GeoJSON, Location
from pydggrid.Types import Operation, ReadMode, PointDataType
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
        super().__init__(Operation.BIN_POINT_VALS)
        self.input: InputTemplate = Auto()
        self.points: pydggrid.Output.Sequence = pydggrid.Output.Sequence()
        self.dgg_meta: str = ""
        self.Meta.save("input_delimiter", "\"|\"")
        # Set defaults

    def __bytes__(self) -> bytes:
        """
        Returns query bytes
        :return: Clip Bytes
        """
        return self.input.__bytes__()

    def set_input(self,
                  point_type: [PointDataType, int, None] = None,
                  input_data: [Any, None] = None,
                  column: [Dict[str, str], Dict[str, int], None] = None) -> None:
        """
        Sets the point presence input query.
        :param point_type: PointDataType definition
        :param column: Column name mapping, should be a dictionary, as
            In the case of PointDataType.TEXT
                {
                    "lat": "<lat-equivalent-field>",
                    "long": "<lat-equivalent-field>",
                    "id": "<id-equivalent-field>",
                    "label": "<label-equivalent-field>"
                }

                .. or, a dictionary of indexes as:
                {
                    "lat": 1,
                    "long": 2,
                    "id": 0,
                    "label": 3
                }
                this field can be left as none, in which case default mapping as described above will be used.
            for PointDataType.GDAL
                The column value is ignored for GDAL PointPresence Queries
        :param input_data: Input data to process to the input element.
        :return:
        """
        if point_type == PointDataType.TEXT:
            self.input = Location()
        elif point_type == PointDataType.GDAL:
            self.input = GeoJSON()
            self.Meta.save("point_input_file_type", "GDAL")
        else:
            raise Exception("Unsupported PointDataType")
        if input_data is not None:
            self.input.save(input_data, column)

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadPayload(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        return libpydggrid.UnitTest_ReadPayload(self.Meta.dict(), self.input.__bytes__())

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytearray = bytearray(self.input.__bytes__())
        return libpydggrid.UnitTest_ReadQuery(dictionary, list(payload))

    # Override
    # noinspection PyPep8Naming
    def UnitTest_RunQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytearray = bytearray(self.input.__bytes__())
        return libpydggrid.UnitTest_RunQuery(dictionary, list(payload))

    # Override
    def run(self, byte_data: [bytes, None] = None) -> None:
        """
        Runs the query
        :param byte_data byte payload, if left blank Input.__bytes__() will be used
        :return: None
        """
        byte_data: Dict[str, bytes] = super().exec(self.input.__bytes__())
        self.dgg_meta = bytearray(byte_data["meta"]).decode() if "meta" in byte_data else ""
        self.points.save(byte_data["points"], ReadMode.SEQUENCE)

    # INTERNAL
