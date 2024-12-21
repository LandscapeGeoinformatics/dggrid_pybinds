import pathlib
from typing import Dict, List

import geojson
import geopandas
import numpy
import pandas
import pyarrow

from pydggrid.Input import Auto, Geometry, ArrayList
from pydggrid.Types import InputAddress


class Module:

    def __init__(self):
        """
        Default constructor
        """
        self.object: Auto = Auto()

    def auto(self) -> None:
        """
        Puts the clip mode into WHOLE_EARTH mode
        :return: None
        """
        self.object: Auto = Auto()

    def geometry(self,
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
        if not isinstance(self.object, Geometry): self.object: Geometry = Geometry()
        return self.object.save(records, definition) if records is not None else None

    def cells(self,
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
        if not isinstance(self.object, ArrayList): self.object: ArrayList = ArrayList()
        return self.object.save(records, definition) if records is not None else None

    def __bytes__(self) -> bytes:
        """
        Return clip bytes
        :return: Clip Bytes
        """
        return self.object.__bytes__()
