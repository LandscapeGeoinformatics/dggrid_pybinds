import os
import pathlib
from typing import List, Dict

import geojson
import geopandas
import libpydggrid
import numpy
import pandas
import pyarrow

from pydggrid.Modules import Input
from pydggrid.Output import Geometry, Records
from pydggrid.Types import Operation, ClipType, ReadMode, CellOutput, ChildrenOutput, NeighborOutput, \
    InputAddress, PointOutput, OutputAddress
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
        self._input: Input = Input(extended_fields=False)
        self.records: Records = Records()
        self.cells: Geometry = Geometry()
        self.points: Geometry = Geometry()
        self.collection: Geometry = Geometry()
        self.dgg_meta: str = ""
        # Set defaults
        self.Meta.set_default("clip_cell_densification")
        self.Meta.set_default("clipper_scale_factor")
        self.Meta.set_default("clip_using_holes")
        self.Meta.set_default("clip_cell_res")
        self.Meta.save("input_delimiter", "\" \"")
        self.Meta.save("output_delimiter", "\",\"")
        self.Meta.save("point_output_type", PointOutput.GEOJSON)
        self.Meta.save("cell_output_type", CellOutput.GEOJSON)
        self.Meta.save("output_address_type", OutputAddress.SEQNUM)
        self.Meta.save("input_address_type", InputAddress.GEO)

    def __bytes__(self) -> bytes:
        """
        Returns query bytes
        :return: Clip Bytes
        """
        return self._input.__bytes__()

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
        self._input.points(records, definition)

    def input_cells(self,
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
        self.Meta.save("input_address_type", address_type)
        self._input.cells(records, definition)

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadPayload(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        self._alter_payload()
        return libpydggrid.UnitTest_ReadPayload(self.Meta.dict(), self._input.__bytes__())

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        self._alter_payload()
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
        self._alter_payload()
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
        self._alter_payload()
        byte_data: Dict[str, bytes] = super().exec(self._input.__bytes__())
        self.dgg_meta = bytearray(byte_data["meta"]).decode() if "meta" in byte_data else ""
        self.cells.save(byte_data["cells"], self._read_mode("cells"))
        self.points.save(byte_data["points"], self._read_mode("points"))
        self.collection.save(byte_data["collection"], self._read_mode("collection"))
        # save table data
        content_string: str = bytearray(byte_data["dataset"]).decode()
        content_array: List[str] = content_string.split(os.linesep)
        if "|" not in content_string:
            self.records = Records(["INDEX"])
            self.records.save([n.strip() for n in content_array if n.strip() != ""], ReadMode.SEQUENCE)
        else:
            for content_point in content_array:
                if content_point.strip() != "":
                    data_points: List[str] = content_point.split("|")
                    vector_points: List[str] = data_points[0].split(",")
                    self.records.save([[str(vector_points[0]), str(vector_points[1]), str(data_points[1])]],
                                      ReadMode.SEQUENCE)

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
