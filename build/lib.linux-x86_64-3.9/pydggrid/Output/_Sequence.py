from typing import List, Any, Dict

import geopandas
import numpy
import pandas
import lxml.etree as xml

from pydggrid.Output._Template import Template as OutputTemplate


class Output(OutputTemplate):

    def __init__(self):
        super().__init__()

    def get_frame(self) -> [pandas.DataFrame, None]:
        """
        Returns the record as a data frame
        :return: Pandas DataFrame or None if not available
        """
        if self._type == list:
            elements: List[Dict[str, Any]] = list([])
            [elements.append({"id": int(n)}) for n in self._data]
            return pandas.DataFrame(elements)
        else:
            raise NotImplementedError(f"This collection cannot be exported as a DataFrame [ {self._type} ]")

    def get_geoframe(self) -> geopandas.GeoDataFrame:
        """
        Returns the record as a geo data frame
        :return: Geo Pandas Data Frame
        """
        if self._type == list:
            return geopandas.GeoDataFrame(self.get_frame())
        else:
            raise NotImplementedError("This collection cannot be exported as a GeoDataFrame")

    def get_numpy(self) -> numpy.ndarray:
        """
        Returns the record as a numpy ndarray
        :return: Numpy ND Array
        """
        if self._type is list:
            return numpy.array(self._data)
        else:
            raise NotImplementedError("This collection cannot be exported as Numpy NDArray")

    def get_xml(self) -> str:
        """
        Returns the XML string of the content
        :return: XML String
        """
        if self._type == list:
            root = xml.Element("points")
            for point in self._data:
                xml.SubElement(root, "point").text = str(point)
            return bytes(xml.tostring(root, encoding="UTF8")).decode()
        else:
            raise NotImplementedError("This collection cannot be exported as XML")

    def un_static(self) -> None:
        """
        Un Statics a method
        :return: None
        """
        pass

    # INTERNAL
