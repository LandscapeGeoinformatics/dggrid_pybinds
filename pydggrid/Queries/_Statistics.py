import pathlib
from typing import Any, List, Dict

import geojson
import geopandas
import libpydggrid
import numpy
import pandas
import pyarrow

from pydggrid.Modules import Clip
from pydggrid.Output import Records
from pydggrid.Types import Operation, ClipType, ReadMode, CellOutput, ChildrenOutput, NeighborOutput, \
    InputAddress, PointOutput
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
        super().__init__(Operation.OUTPUT_STATS)
        self._clip: Clip = Clip()
        self.table: Records = Records(["Res", "Cells", "Area", "CLS"])
        self.dgg_meta: str = ""
        # Set defaults
        self.Meta.set_default("clip_cell_densification")
        self.Meta.set_default("clipper_scale_factor")
        self.Meta.set_default("clip_using_holes")
        self.Meta.set_default("clip_cell_res")
        self.Meta.on_save("cell_output_type", lambda : self._run_fixes())
        self.Meta.on_save("point_output_type", lambda : self._run_fixes())

    def __bytes__(self) -> bytes:
        """
        Returns query bytes
        :return: Clip Bytes
        """
        return self._clip.__bytes__()

    def clip_geometry(self,
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
        Clips to geometry
        :param records: Records to save into the buffer, this parameter can be:
            - A path string or a pathlib.Path object point to file that is readable by the read parameter.
            - A List of geometry strings, a polygon buffer which includes x, y, z, and optionally m points.
            - A string value containing either geojson or csv data
            - a pandas dataframe, which in this case must provide the name of the geometry column as a string, if
            this value is not provided the column name is assumed as `geometry`.
            - a geopandas dataframe, which in this case must provide the name of the geometry column as a string, if
            this value is not provided the column name is assumed as `geometry`.
            - a 2 dimensional numpy array which contains x, y, z, or m geometries.  Polygon offsets are sent as blank.
            - A dictionary or a list of dictionaries containing a geometry column declared by the definition argument
            as a string.
            - a geojson dictionary object
            - A pyarrow geometry Array
            - a pyarrow table with the geometry column defined as a string in the definition argument, by default this
            field is assumed as `geometry`.
            - None which in case dataset must be loaded with the save() or read() keywords.
        :param definition: Columns definition data, for most items this is a string declaring the geometry columns used.
        :return:
        """
        self._clip.geometry(records, definition)
        self.Meta.save("clip_subset_type", ClipType.GDAL)

    def clip_cells(self,
                   records: [str,
                             List[str],
                             List[int],
                             pathlib.Path,
                             pandas.DataFrame,
                             geopandas.geoseries,
                             geopandas.GeoDataFrame,
                             numpy.ndarray,
                             pyarrow.Array,
                             pyarrow.Table],
                   definition: [int, str, None] = None,
                   address_type: InputAddress = InputAddress.SEQNUM) -> None:
        """
        Clips to squence numbers
        :param records: Records to save into the buffer, this parameter can be:
            - A path string or a pathlib.Path object point to file that is readable by the read parameter.
            - A List of sequence numbers as string or integers
            - A string value containing a flat text file containing sequence numbers
            - a pandas dataframe, which in this case must provide the name of the sequence column as a string, if
            this value is not provided the column name is assumed as the first column.
            - a geopandas dataframe, which in this must provide the name of the sequence column as a string, if
            this value is not provided the column name is assumed as the first column.
            - a 1 dimensional numpy array containing sequence numbers
            - A pyarrow geometry Array containing sequence numbers
            - a pyarrow table with the sequence column defined as a string in the definition argument, by default this
            field is assumed as the first column name.
        :param definition: Column name or index, respectively as a string or an index
        :param address_type: Input cell type, by default this value is set to SEQNUM
        :return:
        """
        self._clip.cells(records, definition)
        self.Meta.save("clip_subset_type", ClipType.COARSE_CELLS)
        self.Meta.save("clip_cell_addresses", self._clip.object.integer_list(" "))
        self.Meta.save("input_address_type", address_type)

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadPayload(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        self._alter_payload()
        return libpydggrid.UnitTest_ReadPayload(self.Meta.dict(), self._clip.__bytes__())

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        self._alter_payload()
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytearray = bytearray(self._clip.__bytes__())
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
        payload: bytearray = bytearray(self._clip.__bytes__())
        return libpydggrid.UnitTest_RunQuery(dictionary, list(payload))

    # Override
    def run(self, byte_data: [bytes, None] = None) -> None:
        """
        Runs the query
        :param byte_data byte payload, if left blank Input.__bytes__() will be used
        :return: None
        """
        self._alter_payload()
        byte_data: Dict[str, bytes] = super().exec(self._clip.__bytes__())
        self.dgg_meta = bytearray(byte_data["meta"]).decode() if "meta" in byte_data else ""
        if "statistics" in byte_data.keys():
            statistics_string: str = ""
            statistics_array: List[Dict[Any]] = []
            for bit_char in byte_data["statistics"]:
                statistics_string += chr(bit_char)
            statistics_string = statistics_string.replace("\x00", "")
            element_lines: List[str] = statistics_string.split("\n")
            for element_line in element_lines:
                element_cells: List[str] = element_line.split("|")
                if element_cells[0] is not "":
                    statistics_array.append({
                        "Res": int(element_cells[0]),
                        "Cells": int(element_cells[1]),
                        "Area": float(element_cells[2]),
                        "CLS": float(element_cells[3])})
            self.table.save(statistics_array, ReadMode.FRAME)

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
            self.Meta.save("clip_cell_addresses", " ".join([str(n) for n in self._clip.data]))
            self.Meta.save("input_address_type", InputAddress.SEQNUM)

