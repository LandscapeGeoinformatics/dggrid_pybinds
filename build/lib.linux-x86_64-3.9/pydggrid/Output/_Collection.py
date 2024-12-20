from typing import List, Any, Dict, Tuple

import fiona
import geopandas
import numpy
import pandas
from pydggrid.Output._Template import Template as OutputTemplate

fiona.drvsupport.supported_drivers['kml'] = 'rw'  # enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['KML'] = 'rw'  # enable KML support which is disabled by default
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)


class Output(OutputTemplate):

    def __init__(self):
        super().__init__()
        self._crs: str = "epsg:4326"
        self._cols: List[str] = list(["id", "lat", "long"])

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
                index_id = data_node.id if hasattr(data_node, "id") else data_node.Name
                [elements.append({
                    self._cols[0]: str(index_id),
                    self._cols[1]: n[0],
                    self._cols[2]: n[1]
                }) for n in points]
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
        else:
            raise NotImplementedError("This collection cannot be exported as a GeoDataFrame")

    # Override
    def get_kml(self) -> str:
        """
        Returns the XML string of the content
        :return: XML String
        """
        if self._type == pandas.DataFrame:
            return self._data.to_xml()
        elif self._type == geopandas.GeoDataFrame:
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
        else:
            raise NotImplementedError("This collection cannot be exported as Numpy NDArray")