import os
import pathlib
import sys
from typing import Any, List

import geojson
import geopandas

from pydggrid.Input._ShapeFIle import Input as ShapeInput
from pydggrid.Input._GeoJSON import Input as GeoJSONInput
from pydggrid.Input._Template import Template as InputTemplate
from pydggrid.Types import DataType


class Input(InputTemplate):

    def __init__(self):
        super(Input, self).__init__()
        self._root: InputTemplate = ShapeInput()
        self.data: List[geopandas.GeoDataFrame] = list([])

    def geo_json(self, data: Any) -> None:
        """
        Reads geojson into memory
        :param data: GeoJSON object this can be any of the following objects:
            str, (Path string or geojson string)
            pathlib.Path,
            geojson.GeoJSON,
            dict
        :return: None
        """
        if isinstance(data, geojson.GeoJSON):
            self.data.append(geopandas.GeoDataFrame.from_features(data))
            self.records.save(geojson.dumps(data), DataType.STRING)
            return
        elif isinstance(data, dict):
            self.data.append(geopandas.GeoDataFrame.from_dict(data))
            self.records.save(geojson.dumps(geojson.GeoJSON(data)), DataType.STRING)
            return
        elif isinstance(data, pathlib.Path):
            file = open(data.absolute(), "rt")
            text: str = file.read()
            file.close()
            #
            self.data.append(geopandas.read_file(text, driver="GeoJSON"))
            self.records.save(text, DataType.STRING)
            file.close()
            return
        elif isinstance(data, str):
            if data.strip().startswith("{"):
                return self.geo_json(geojson.loads(data))
            elif os.path.isfile(data.strip()):
                return self.geo_json(pathlib.Path(data.strip()))
        else:
            raise ValueError(f"Unrecognized GeoJSON data {data}")
        # self._root = GeoJSONInput()
        # self._root.save(geo_json)
        # self.records = self._root.records

    def shape_file(self, path: [str, pathlib.Path]) -> None:
        """
        Sets the input into shape file mode
        :param path: Path to read shapefile from
        :return: None
        """
        self._root = ShapeInput()
        self._root.read(path)
        self.records = self._root.records

    # Override
    def save(self, data: [str, pathlib.Path], column: None = None) -> None:
        """
        Save data override
        :param data: Path to or a path object pointing to a shape file
        :param column: Ignored for this interface
        :return: None
        """
        if isinstance(data, str):
            return self.save(pathlib.Path(data))
        elif isinstance(data, pathlib.Path):
            elements: List[bytes] = list([])
            file_base: str = str(data.absolute())[:-3]
            elements.append(self._get_bytes(f"{file_base}shp", "shp"))
            elements.append(self._get_bytes(f"{file_base}shx", "shx"))
            elements.append(self._get_bytes(f"{file_base}shx", "dbf"))
            elements.append(self._get_bytes(f"{file_base}shx", "prj"))
            elements.append(self._get_bytes(f"{file_base}shx", "sbn"))
            elements.append(self._get_bytes(f"{file_base}shx", "sbx"))
            self.records.save(b''.join(elements), DataType.SHAPE_BINARY)
        else:
            raise ValueError(f"Unrecognized shape file {data}")

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
        else:
            raise AttributeError("Unrecognized input object type.")

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
