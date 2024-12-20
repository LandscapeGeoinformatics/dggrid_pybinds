import sys
from typing import List, Any, Dict, Tuple

import geopandas
import numpy
import pandas
from pydggrid.Output._Template import Template as OutputTemplate

pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)


class Output(OutputTemplate):

    def __init__(self, columns: [List[str], None] = None):
        super().__init__()
        self._crs: str = "epsg:4326"
        self._cols: List[str] = list(["point", "count", "total", "mean", "classes", "vector"]) if columns is None \
            else list(columns)

    # Override
    def get_aigen(self) -> str:
        """
        AI Gen text override
        :return: String
        """
        raise ReferenceError("AI Gen text not supported for this output.")

    # Override
    def get_frame(self) -> [pandas.DataFrame, None]:
        """
        Returns the record as a data frame
        :return: Pandas DataFrame or None if not available
        """
        if self._type is None:
            return pandas.DataFrame()
        elif self._type == pandas.DataFrame:
            return self._data
        elif self._type == geopandas.GeoDataFrame:
            elements: List[Dict[str, Any]] = list([])
            frame: pandas.DataFrame({"id": [], "lat": [], "long": []})
            for data_node in self._data.itertuples():
                points: List[Tuple[float, float]] = self._list_points(data_node.geometry)
                [elements.append({self._cols[index]: n[index] for index in range(0, len(self._cols))}) for n in points]
            return pandas.DataFrame(elements)
        elif self._type == list:
            elements: Dict[str, list] = {k: list([]) for k in self._cols}
            elements[list(elements.keys())[0]] = self._data
            return pandas.DataFrame(elements)
        else:
            raise NotImplementedError(f"This collection cannot be exported as a DataFrame [ {self._type} ]")

    # Override
    def get_geoframe(self) -> geopandas.GeoDataFrame:
        """
        Returns the record as a geo data frame
        :return: Geo Pandas Data Frame
        """
        if self._type is None:
            return geopandas.GeoDataFrame()
        elif self._type == pandas.DataFrame:
            return geopandas.GeoDataFrame(self._data)
        elif self._type == geopandas.GeoDataFrame:
            return self._data
        elif self._type == list:
            return geopandas.GeoDataFrame(self.get_frame())
        else:
            raise NotImplementedError("This collection cannot be exported as a GeoDataFrame")

    # Override
    def get_xml(self) -> str:
        """
        Returns the XML string of the content
        :return: XML String
        """
        if self._type == pandas.DataFrame:
            return self._data.to_xml()
        else:
            raise NotImplementedError("This collection cannot be exported as XML")

    # Override
    def get_kml(self) -> str:
        """
        Returns the XML string of the content
        :return: XML String
        """
        if self._type == geopandas.GeoDataFrame:
            return self._content["kml"]
        else:
            raise NotImplementedError("This collection cannot be exported as XML")

    # Override
    def get_numpy(self) -> numpy.ndarray:
        """
        Returns the record as a numpy ndarray
        :return: Numpy ND Array
        """
        if self._type is None:
            return numpy.array([])
        if self._type == pandas.DataFrame:
            return self._data.to_numpy()
        elif self._type == geopandas.GeoDataFrame:
            return self.get_frame().to_numpy()
        elif self._type == list:
            return numpy.array(self._data)
        else:
            raise NotImplementedError("This collection cannot be exported as Numpy NDArray")
