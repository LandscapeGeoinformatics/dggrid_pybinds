import sys
from typing import List, Any, Dict, Tuple

import geopandas
import numpy
import pandas
from pydggrid.Output._Template import Template as OutputTemplate
from pydggrid.Types import DataType, ReadMode;

pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)


class Output(OutputTemplate):

    def __init__(self, columns: List[str], types: List[DataType]):
        super().__init__()
        self.definition: Dict[str, Any] = {}
        for column_index, column_name in enumerate(columns):
            self.definition[column_name] = types[column_index]
        self._cols = list(self.definition.keys())
        self._data: pandas.DataFrame = pandas.DataFrame(columns=columns)

    def save(self, data: [List[List[Any]], pandas.DataFrame], read_mode: ReadMode = ReadMode.NONE) -> None:
        """
        Saves data to frame
        :param data: Data Set
        :param read_mode: Read Mode should be None
        :return: None
        """
        if isinstance(data, pandas.DataFrame):
            if self._data.shape[0] == 0:
                self._data = pandas.DataFrame(data)
            else:
                self._data = pandas.concat([self._data, data])
        elif isinstance(data, list):
            data_frame: pandas.DataFrame = pandas.DataFrame(columns=self.definition.keys(), data=data)
            return self.save(data_frame)

    # Override
    def get_frame(self) -> [pandas.DataFrame, None]:
        """
        Returns the record as a data frame
        :return: Pandas DataFrame or None if not available
        """
        return self._data

    # Override
    def get_geoframe(self) -> geopandas.GeoDataFrame:
        """
        Returns the record as a geo data frame
        :return: Geo Pandas Data Frame
        """
        return geopandas.GeoDataFrame(self._data)

    # Override
    def get_xml(self) -> str:
        """
        Returns the XML string of the content
        :return: XML String
        """
        raise NotImplementedError("This collection cannot be exported as XML")

    # Override
    def get_numpy(self) -> numpy.ndarray:
        """
        Returns the record as a numpy ndarray
        :return: Numpy ND Array
        """
        return self._data.to_numpy()