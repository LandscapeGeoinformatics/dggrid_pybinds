import os
import pathlib
import sys
from io import StringIO
from typing import Any, List

import geopandas
import numpy
import pyarrow
import shapely.wkt
# import geoarrow.pyarrow as arrow
import pyarrow as pa

from pydggrid.Input._Template import Template as InputTemplate
from pydggrid.System import Library
from pydggrid.Types import DataType
from pyarrow import csv as csv_arrow


class Input(InputTemplate):

    def __init__(self):
        super(Input, self).__init__()
        self.data: List[Any] = list([])

    # Override
    def save(self, data: [str,
                          pathlib.Path,
                          pa.Array,
                          pa.Table,
                          geopandas.GeoSeries,
                          numpy.ndarray,
                          List[str]], column: None = None) -> None:
        """
        Save data override
        :param data:
            - a path to a valid .arrow file
            - a pathlib object that points to an .arrow file
            - a geopandas GeoSeries object.
            - a geopandas dataframe with a geometry
            - A numpy ndarray
            - An array of geometric WKT text definitions i.e. "POINT (0 1)"
            - A geoarrow array of shapes
            - A geoarrow table containing a geometry field, which in this case the column argument must be a string
            presenting the name of the geometry column.
        :param column: Ignored for this interface
        :return: None
        """
        if isinstance(data, str):
            if os.path.isfile(data):
                return self.save(pathlib.Path(data))
            if Library.is_csv_string(data):
                return self.save(csv_arrow.read_csv(StringIO(data)))
            else:
                raise ValueError("unrecognized string type while reading GeoArrow data")
        elif isinstance(data, pathlib.Path):
            if Library.is_csv_file(data):
                return self.save(csv_arrow.read_csv(data))
            with pa.memory_map(data.absolute().__str__(), 'r') as source:
                return self.save(pa.ipc.open_file(source).read_all())
        # elif isinstance(data, geopandas.GeoSeries):
            # return self.save(arrow.as_geoarrow(data))
        # elif isinstance(data, geopandas.GeoDataFrame):
        #     return self.save(data.geometry)
        # elif isinstance(data, list):
            # return self.save(arrow.as_geoarrow(data))
        # elif isinstance(data, pyarrow.Array):
        #     self.data.append(data)
            # self.records.save(arrow.to_geopandas(data).to_json(), DataType.STRING)
        # elif isinstance(data, pyarrow.Table):
            # return self.save(arrow.array(data[column]), column)
        else:
            raise ValueError(f"Unrecognized GeoArrow data {type(data)}")

    def read(self, source_file: [str, pathlib.Path]) -> None:
        """
        Reads a file into memory routes for save
        :param source_file: Source File
        :return: None
        """
        return self.save(source_file)

    # Override
    def copy(self, source_object: Any) -> None:
        """
        Copies the source object to local
        :return:
        """
        if isinstance(source_object, Input):
            self.data.clear()
            self.records.clear()
            self.records.copy(source_object.records)
            [self.data.append(n) for n in source_object.data]
        return super(Input, self).copy(source_object)

    # INTERNAL
    def _un_static(self) -> None:
        """
        Un-statics a function
        :return: None
        """
        pass

    def _get_bytes(self, file_name: str, header_ident: str) -> bytes:
        """
        Returns byte packet of given file name
        :param file_name: File Name
        :param header_ident: Header identifier (shp, shx...)
        :return: Bytes array
        """
        self._un_static()
        elements: List[bytes] = list([])
        file = open(file_name, "rb")
        elements.append(DataType.STRING.convert_bytes(header_ident))
        elements.append(DataType.BINARY.convert_bytes(file.read()))
        file.close()
        return b''.join(elements)
