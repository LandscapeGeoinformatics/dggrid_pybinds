import sys
from typing import Any, List, Dict

import libpydggrid

from pydggrid.Input import Auto, InputTemplate
from pydggrid.Output import Geometry, Table
from pydggrid.Types import Operation, ClipType, ReadMode, CellOutput, ChildrenOutput, NeighborOutput, \
    InputAddress, PointOutput, OutputAddress, DataType
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
        super().__init__(Operation.TRANSFORM_POINTS)
        self.input: InputTemplate = Auto()
        self.table: Table = Table(["A", "B", "Name"], [DataType.INT, DataType.INT, DataType.STRING])
        self.cells: Geometry = Geometry()
        self.points: Geometry = Geometry()
        self.collection: Geometry = Geometry()
        self.dgg_meta: str = ""
        # Set defaults
        self.Meta.set_default("clip_cell_densification")
        self.Meta.set_default("clipper_scale_factor")
        self.Meta.set_default("clip_using_holes")
        self.Meta.set_default("clip_cell_res")
        self.Meta.save("input_delimiter", "\"|\"")
        self.Meta.save("output_delimiter", "\",\"")
        self.Meta.save("point_output_type", PointOutput.GEOJSON)
        self.Meta.save("cell_output_type", CellOutput.GEOJSON)
        self.Meta.save("output_address_type", OutputAddress.SEQNUM)

    def __bytes__(self) -> bytes:
        """
        Returns query bytes
        :return: Clip Bytes
        """
        return self.input.records.__bytes__()

    def set_points(self):
        pass

    # def set_input(self,
    #               input_type: [InputAddress, int, None] = None,
    #               data: [Any, None] = None,
    #               columns: [List[Any], None] = None) -> None:
    #     """
    #     Sets the query clip
    #     :param input_type: ClipType definition from pydggrid.Types
    #     :param data: Data to use with the clipping this is optional and can be set after the clip type has been
    #         configured
    #     :param columns: Used to send column information with the clip options, this field is optional but allows you to
    #         customize the order and index of columns to choose from using pandas dataframes, numpy ndarray objects and
    #         dictionaries.
    #     :return: None
    #     """
    #     if input_type is not None:
    #         type_t: InputAddress = InputAddress(input_type)
    #         if type_t == InputAddress.SEQNUM:
    #             self.input = Sequence()
    #         elif type_t == InputAddress.GEO:
    #             self.input = Location()
    #         else:
    #             raise AttributeError(f"Requested clip type({input_type}) is not supported")
    #         self.Meta.save("input_address_type", type_t)
    #         return self.input.save(data, columns) if data is not None else None
    #     return None

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadPayload(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        self._alter_payload()
        return libpydggrid.UnitTest_ReadPayload(self.Meta.dict(), self.input.__bytes__())

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        self._alter_payload()
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
        self._alter_payload()
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
        self._alter_payload()
        byte_data: Dict[str, bytes] = super().exec(self.input.__bytes__())
        self.dgg_meta = bytearray(byte_data["meta"]).decode() if "meta" in byte_data else ""
        self.cells.save(byte_data["cells"], self._read_mode("cells"))
        self.points.save(byte_data["points"], self._read_mode("points"))
        self.collection.save(byte_data["collection"], self._read_mode("collection"))
        # save table data
        content_array: List[str] = bytearray(byte_data["dataset"]).decode().split("\n")
        for content_point in content_array:
            if content_point.strip() != "":
                if "|" in content_point:
                    data_points: List[str] = content_point.split("|")
                    vector_points: List[str] = data_points[0].split(",")
                    self.table.save([[str(vector_points[0]), str(vector_points[1]), str(data_points[1])]])
                else:
                    self.table.save(str(content_point))

    # INTERNAL

    def _read_mode(self, vector_id: str) -> ReadMode:
        """
        Returns read mode for the vector
        :param vector_id Vector ID To use
        :return: Read Mode Object
        """
        if vector_id == "cells":
            return ReadMode(self.Meta.as_int("cell_output_gdal_format")) \
                if self.Meta.as_int("cell_output_type") == CellOutput.GDAL \
                else ReadMode(self.Meta.as_int("cell_output_type"))
        elif vector_id == "points":
            return ReadMode(self.Meta.as_int("point_output_gdal_format")) \
                if self.Meta.as_int("point_output_type") == PointOutput.GDAL \
                else ReadMode(self.Meta.as_int("point_output_type"))
        elif vector_id == "collection":
            return ReadMode.NONE if self._is_collection() is False \
                else ReadMode(self.Meta.as_int("cell_output_gdal_format"))
        elif vector_id == "table":
            return ReadMode.FRAME

    def _is_collection(self) -> bool:
        """
        Returns true if collection query
        :return: True if collection
        """
        return self.Meta.get("cell_output_type") == CellOutput.GDAL_COLLECTION or \
               self.Meta.get("point_output_type") == PointOutput.GDAL_COLLECTION

    def _run_fixes(self):
        """
        Returns collection output type
        :return: Collection output type
        """
        if self._is_collection():
            self.Meta.save("children_output_type", ChildrenOutput.GDAL_COLLECTION)
            self.Meta.save("neighbor_output_type", NeighborOutput.GDAL_COLLECTION)
            self.Meta.set_default("cell_output_gdal_format")
            self.Meta.set_default("point_output_gdal_format")
            self.Meta.set_default("collection_output_gdal_format")

        if self.Meta.as_int("point_output_type") == PointOutput.GDAL:
            self.Meta.set_default("point_output_gdal_format")

        if self.Meta.as_int("cell_output_type") == PointOutput.GDAL:
            self.Meta.set_default("cell_output_gdal_format")

    def _alter_payload(self) -> None:
        """
        Makes final changes to the parameter payload
        :return: None
        """
        if self.Meta.as_int("clip_subset_type") == ClipType.COARSE_CELLS:
            # noinspection PyUnresolvedReferences
            self.Meta.save("clip_cell_addresses", " ".join([str(n) for n in self.input.data]))
            self.Meta.save("input_address_type", InputAddress.SEQNUM)
