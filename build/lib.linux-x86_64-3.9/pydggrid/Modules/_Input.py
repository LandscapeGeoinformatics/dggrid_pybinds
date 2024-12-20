import pathlib
from typing import Dict

import geojson
import geopandas
import numpy
import pandas
import pyarrow
from fiona.ogrext import List

from pydggrid.Input import Auto, Geometry, ArrayList, PointList
from pydggrid.Types import ClipType


class Module:

    def __init__(self):
        """
        Default constructor
        """
        self.object: [Auto, PointList, ArrayList] = Auto()

    def auto(self) -> None:
        """
        Puts the clip mode into WHOLE_EARTH mode
        :return: None
        """
        self.object: Auto = Auto()

    def points(self,
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
        if not isinstance(self.object, PointList):
            self.object: PointList = PointList()
        return self.object.save(records, definition) if records is not None else None

    def List(self,
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
             definition: [int, str, None] = None) -> None:
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
        :return:
        """
        self.object: ArrayList = ArrayList()
        return self.object.save(records, definition) if records is not None else None

    def __bytes__(self) -> bytes:
        """
        Return clip bytes
        :return: Clip Bytes
        """
        return self.object.__bytes__()
