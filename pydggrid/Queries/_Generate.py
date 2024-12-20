import pathlib
import sys
from typing import Dict, List

import geojson
import geopandas
import libpydggrid
import numpy
import pandas
import pyarrow

from pydggrid.Modules import Clip
from pydggrid.Output import Locations
from pydggrid.System import Constants
from pydggrid.Types import Operation, ClipType, ReadMode, CellOutput, ChildrenOutput, NeighborOutput, \
    InputAddress, PointOutput, GDALFormat, DataType, OutputAddress, CellLabel
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
        super().__init__(Operation.GENERATE_GRID)
        self.clip: Clip = Clip()
        self.cells: Locations = Locations()
        self.points: Locations = Locations()
        self.collection: Locations = Locations()
        self.dgg_meta: str = ""
        # Set defaults
        self.Meta.set_default("clip_cell_densification")
        self.Meta.set_default("clipper_scale_factor")
        self.Meta.set_default("clip_using_holes")
        self.Meta.set_default("clip_cell_res")
        self.Meta.on_save("cell_output_type", lambda: self._run_fixes())
        self.Meta.on_save("point_output_type", lambda: self._run_fixes())
        self.Meta.save("point_output_type", PointOutput.GEOJSON)
        self.Meta.save("cell_output_type", CellOutput.GEOJSON)

    def set_crs(self, crs_type: [str, None] = None) -> None:
        """
        Sets the read crs pf the generated query
        :param crs_type: Crs String
        :return: None
        """
        self.cells.set_crs(crs_type)
        self.points.set_crs(crs_type)
        self.collection.set_crs(crs_type)

    def cell_type(self, address_type: [OutputAddress, None] = None) -> None:
        """
        Sets output address type
        :param address_type: Address type identifier
        :return: None
        """
        self.Meta.save("output_address_type", address_type)
        self.Meta.save("output_cell_label_type", CellLabel.OUTPUT_ADDRESS_TYPE)

    def set_collection(self, enabled: bool = True) -> None:
        """
        Puts the generator into collection mode
        :return: None
        """
        if enabled:
            self.Meta.save("cell_output_type", CellOutput.GDAL_COLLECTION)
            self.Meta.save("point_output_type", PointOutput.GDAL_COLLECTION)
            self.Meta.save("children_output_type", ChildrenOutput.GDAL_COLLECTION)
            self.Meta.save("neighbor_output_type", NeighborOutput.GDAL_COLLECTION)
        else:
            self.Meta.save("point_output_type", PointOutput.GEOJSON)
            self.Meta.save("cell_output_type", CellOutput.GEOJSON)
            self.Meta.save("point_output_type", PointOutput.NONE)
            self.Meta.save("cell_output_type", CellOutput.NONE)

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
        self.Meta.save("clip_subset_type", ClipType.GDAL)
        return self.clip.geometry(records)

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
                   cell_type: InputAddress = InputAddress.SEQNUM) -> None:
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
        :param cell_type: Input cell type, by default this value is set to SEQNUM
        :return:
        """
        self.clip.cells(records, definition)
        self.Meta.save("clip_subset_type", ClipType.COARSE_CELLS)
        self.Meta.save("clip_cell_addresses", self.clip.object.integer_list(" "))
        self.Meta.save("input_address_type", cell_type)

    def __bytes__(self) -> bytes:
        """
        Returns query bytes
        :return: Clip Bytes
        """
        return self.clip.__bytes__()

    # def set_points(self):
    #     pass
    #
    # def set_clip(self,
    #              clip_type: [ClipType, int, None] = None,
    #              data: [Any, None] = None,
    #              columns: [List[Any], None] = None) -> None:
    #     """
    #     Sets the query clip
    #     :param clip_type: ClipType definition from pydggrid.Types
    #     :param data: Data to use with the clipping this is optional and can be set after the clip type has been
    #         configured
    #     :param columns: Used to send column information with the clip options, this field is optional but allows you to
    #         customize the order and index of columns to choose from using pandas dataframes, numpy ndarray objects and
    #         dictionaries.
    #     :return: None
    #     """
    #     if clip_type is not None:
    #         type_t: ClipType = ClipType(clip_type)
    #         if type_t == ClipType.WHOLE_EARTH:
    #             self.clip = Auto()
    #         elif type_t == ClipType.SEQNUMS:
    #             self.clip = Sequence()
    #         elif type_t == ClipType.SHAPEFILE:
    #             self.clip = ShapeFile()
    #         elif type_t == ClipType.INPUT_ADDRESS_TYPE:
    #             self.clip = Array()
    #         elif type_t == ClipType.GDAL:
    #             self.clip = GDAL()
    #         elif type_t == ClipType.AIGEN:
    #             self.clip = AIGen()
    #         elif type_t == ClipType.COARSE_CELLS:
    #             self.clip = Cells()
    #         elif type_t == ClipType.GEOARROW:
    #             self.clip = Arrow()
    #             clip_type = ClipType.GDAL
    #         else:
    #             raise AttributeError(f"Requested clip type({clip_type}) is not supported")
    #     self.Meta.save("clip_subset_type", clip_type)
    #     return self.clip.save(data, columns) if data is not None else None

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadPayload(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        return libpydggrid.UnitTest_ReadPayload(self.Meta.dict(), self.clip.__bytes__())

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytearray = bytearray(self.clip.__bytes__())
        return libpydggrid.UnitTest_ReadQuery(dictionary, list(payload))

    # Override
    # noinspection PyPep8Naming
    def UnitTest_RunQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytearray = bytearray(self.clip.__bytes__())
        return libpydggrid.UnitTest_RunQuery(dictionary, list(payload))

    # Override
    def run(self, byte_data: [bytes, None] = None) -> None:
        """
        Runs the query
        :param byte_data byte payload, if left blank Input.__bytes__() will be used
        :return: None
        """
        byte_data: Dict[str, bytes] = super().exec(self.clip.__bytes__())
        self.dgg_meta = bytearray(byte_data["meta"]).decode() if "meta" in byte_data else ""
        self.cells.save(byte_data["cells"], self._read_mode("cells"))
        self.points.save(byte_data["points"], self._read_mode("points"))
        self.collection.save(byte_data["collection"], self._read_mode("collection"))

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

    # def _alter_payload(self) -> None:
    #     """
    #     Makes final changes to the parameter payload
    #     :return: None
    #     """
    #     self.Meta.save("clip_subset_type", self.clip.type)
    #     if self.clip.type == ClipType.COARSE_CELLS:
    #         self.Meta.save("clip_cell_addresses", self.clip.object.integer_list(" "))
    #         self.Meta.save("input_address_type", self.clip.address_type)
