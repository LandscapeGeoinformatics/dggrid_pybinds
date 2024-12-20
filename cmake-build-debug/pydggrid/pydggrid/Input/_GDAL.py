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
        self.extensions: List[str] = list(["shp", "shx", "dbf", "prj", "sbn", "sbx"])

    # Override
    def save(self, data: [str,
                          pathlib.Path,
                          geojson.GeoJSON,
                          dict], column: None = None) -> None:
        """
        Save data override
        :param data: GDAL Data to save into buffer, this can be
            - A string to a file that is a *.geojson or *.shp (shape file).
            - A pathlib.path to a file that is a *.geojson or *.shp (shape file).
            - A dictionary that is geojson compatible
            - A geojson.GeoJSON object
        :param column: Ignored for this interface
        :return: None
        """
        if isinstance(data, str):
            return self.save(pathlib.Path(data))
        elif isinstance(data, geojson.GeoJSON):
            return self.geo_json(data)
        elif isinstance(data, dict):
            return self.geo_json(dict)
        elif isinstance(data, pathlib.Path):
            extension: str = str(data.suffix).lower()
            if extension == ".shp":
                return self.shape_file(data)
            if extension == ".json" or extension == ".geojson":
                return self.geo_json(data)
        else:
            raise ValueError(f"Unrecognized shape file {data}")

    # Override
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

    def shape_file(self, data: [str, pathlib.Path]) -> None:
        """
        Sets the input into shape file mode
        :param data: Path to read shapefile from which can be
            - a string to a shape file
            - a pathlib.Path to a file location
        :return: None
        """
        if isinstance(data, str):
            return self.shape_file(pathlib.Path(data))
        elif isinstance(data, pathlib.Path):
            elements: List[bytes] = list([])
            file_base: str = str(data.absolute())[:-3]
            for extension in self.extensions:
                file_name: str = f"{file_base}{extension}"
                if os.path.isfile(file_name):
                    elements.append(self._get_bytes(file_name, extension))
            return_elements: List[bytes] = list([])
            return_elements.append(DataType.INT.convert_bytes(len(elements)))
            [return_elements.append(e) for e in elements]
            self.records.save(b''.join(return_elements), DataType.SHAPE_BINARY)

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
