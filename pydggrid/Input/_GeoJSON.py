import os.path
import pathlib
from typing import Any, List
import geojson
import shapely.wkt

from pydggrid.Input._Template import Template as InputTemplate
from pydggrid.Types import DataType


class Input(InputTemplate):

    def __init__(self):
        super(Input, self).__init__()
        self.data: List[geojson.GeoJSON] = list([])

    # Override
    def save(self, data: [str, pathlib.Path, geojson.GeoJSON, dict], column: None = None) -> None:
        """
        Save data override
        :param data: Path to or a path object pointing to a shape file
        :param column: Ignored for this interface
        :return: None
        """
        if isinstance(data, geojson.GeoJSON):
            self.data.append(data)
            self.records.save(geojson.dumps(data), DataType.STRING)
            return
        elif isinstance(data, dict):
            self.data.append(geojson.GeoJSON(data))
            self.records.save(geojson.dumps(geojson.GeoJSON(data)), DataType.STRING)
            return
        elif isinstance(data, pathlib.Path):
            file = open(data.absolute(), "rt")
            self.data.append(geojson.loads(file.read()))
            self.records.save(geojson.dumps(self.data[-1]), DataType.STRING)
            file.close()
            return
        elif isinstance(data, str):
            if data.strip().startswith("{"):
                return self.save(geojson.loads(data))
            elif os.path.isfile(data.strip()):
                return self.save(pathlib.Path(data.strip()))
        else:
            raise ValueError(f"Unrecognized GeoJSON data {data}")

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

    def _to_bytes(self, index: int) -> bytes:
        """
        Converts a dataframe point into a byte array
        :param index: Point Index
        :return: Byte Array of data point
        """
        elements: List[bytes] = list([])
        for _, element in self.data[index].iterrows():
            coordinate_string: str = str(shapely.wkt.dumps(element["geometry"]))
            elements.append(DataType.INT.convert_bytes(int(element[0])))
            elements.append(DataType.STRING.convert_bytes(coordinate_string))
        return b''.join(elements)
