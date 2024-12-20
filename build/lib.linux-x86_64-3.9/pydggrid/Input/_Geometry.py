import os
import pathlib
import sys
from io import StringIO
from typing import List, Dict, Any, Callable

import geojson
import geopandas
import numpy
import pandas

import pyarrow
import geoarrow.pyarrow as PyArrow
from shapely import wkt

from pydggrid.Interfaces import Dataset
from pydggrid.System import Library
from pydggrid.Types import DataType


class Input(Dataset):

    def __init__(self):
        super(Input, self).__init__()
        super().register_call(list, self._List)
        super().register_call(str, self._String)
        super().register_call(dict, self._Dictionary)
        super().register_call(geojson.GeoJSON, self._GeoJSON)
        super().register_call(pyarrow.Array, self._ArrowArray)
        super().register_call(pandas.DataFrame, self._DataFrame)
        super().register_call(geopandas.GeoSeries, self._GeoSeries)
        super().register_call(geopandas.GeoDataFrame, self._GeoFrame)
        super().register_call(numpy.ndarray, self._Numpy)
        super().register_extension("csv", self._CsvFile)
        super().register_extension("gen", self._GenFile)
        super().register_extension("txt", self._TextFile)
        super().register_extension("json", self._JsonFile)
        super().register_extension("geojson", self._JsonFile)
        super().register_extension("shp", self._ShapeFile)
        super().register_extension("arrow", self._ArrowFile)

    def save(self, records: [Any], definition: Any) -> None:
        """
        Saves records into dataset
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
        :param definition: Columns definition data, for most items this is a string declaring the geometry columns used.
        :return: None
        """
        return super().save(records, definition)

    def read(self, file_path: [str, pathlib.Path], definition: [List[str], List[int], str, None]) -> None:
        """
        Reads data from a file
        :param file_path: File path as string or a pathlib.Path object which points to:
            - a CSV File, which in this case you must provide the definition as the field name of the geometry data
            - a GeoJson file
            - an arrow file containing polygons
            - a pandas dataframe, with the definition provided as a string containing the geometry column name.  By
            default, this argument is set to `geometry`.
            - An arrow file containing an array or table, if table the definition argument can be provided to declare
            the geometry column, by default, this argument is `geometry`.
        :param definition: Definition base
        :return: None
        """
        return super().read(file_path, definition)

    # OVERRIDE
    def __bytes__(self) -> bytes:
        """
        Returns geometry bytes
        :return: Geometry Byte Array
        """
        return super().__bytes__()

    # INTERNAL

    def _ArrowFile(self, file_path: pathlib.Path, file_bytes: bytes, definition: Any) -> None:
        """
        Processes arrow file
        :param file_path:  File path to process
        :param file_bytes:  Binary Data
        :param definition: Definition data, dynamic according to processor
        :return: None
        """
        with pyarrow.memory_map(str(file_path.absolute()), 'r') as source:
            return self.save(pyarrow.ipc.open_file(source).read_all(), None)

    def _ShapeFile(self, file_path: pathlib.Path, file_bytes: bytes, definition: Any) -> None:
        """
        Processes shape file
        :param file_path:  File path to process
        :param file_bytes:  Binary Data
        :param definition: Definition data, dynamic according to processor
        :return: None
        """
        return self.save(geopandas.read_file(file_path.absolute()), None)

    def _JsonFile(self, file_path: pathlib.Path, file_bytes: bytes, definition: Any) -> None:
        """
        Processes json file
        :param file_path:  File path to process
        :param file_bytes:  Binary Data
        :param definition: Definition data, dynamic according to processor
        :return: None
        """
        return self._String(file_bytes.decode(), None)

    def _CsvFile(self, file_path: pathlib.Path, file_bytes: bytes, definition: Any) -> None:
        """
        Processes CSV File
        :param file_path:  File path to process
        :param file_bytes:  Binary Data
        :param definition: Definition data, dynamic according to processor
        :return: None
        """
        return self._String(file_bytes.decode(), definition)

    def _GenFile(self, file_path: pathlib.Path, file_bytes: bytes, definition: Any) -> None:
        """
        Processes AI Gen File
        :param file_path:  File path to process
        :param file_bytes:  Binary Data
        :param definition: Definition data, dynamic according to processor
        :return: None
        """
        return self._GeoFrame(Library.aigen_frame(file_bytes.decode()), definition)

    def _TextFile(self, file_path: pathlib.Path, file_bytes: bytes, definition: Any) -> None:
        """
        Processes AI Gen File
        :param file_path:  File path to process
        :param file_bytes:  Binary Data
        :param definition: Definition data, dynamic according to processor
        :return: None
        """
        return self._String(file_bytes.decode(), definition)

    def _String(self, records: str, definition: [str, None] = None) -> None:
        """
        Processes string input
        :param records: String records, this could be:
            - A GeoJSON String
            - A CSV string, in which the definition must point to a column or index that points to the geometry column.
            - A space delimited string in the format lat, long, ID, Label, the string must at least contain an X, Y column
        :param definition: Definition argument must contain the mappings for lat, long, ID, Label
               {
                    "lat": "<lat-equivalent-field>",
                    "long": "<lat-equivalent-field>",
                    "id": "<id-equivalent-field>",
                    "label": "<label-equivalent-field>"
                }

                .. or, a dictionary of indexes as:
                {
                    "lat": 1,
                    "long": 2,
                    "id": 0,
                    "label": 3
                }
        :return:
        """
        if Library.is_geojson(records):
            return self._GeoJSON(geojson.loads(records))
        elif Library.is_csv_string(records):
            column_name: str = "geometry" if definition is None else definition
            data_frame: geopandas.GeoDataFrame = geopandas.read_file(StringIO(records))
            data_frame[column_name] = data_frame[column_name].apply(wkt.loads)
            return self._GeoSeries(data_frame.geometry, None)
        else:
            elements: List[Dict[str, Any]] = list([])
            line_set: List[str] = records.split(os.linesep)
            for index, line_element in enumerate(line_set):
                element_id: str = index
                line_node: List[str] = line_element.split(" ")
                line_nodes: List[str] = [n.strip() for n in line_node if n.strip() != ""]
                #
                node_size: int = len(line_nodes)
                if node_size >= 2 and Library.is_float(line_nodes[0]) and Library.is_float(line_nodes[1]):
                    elements.append({
                        "lat": float(line_nodes[0]),
                        "long": float(line_nodes[0]),
                        "id": str(index) if node_size < 3 else line_nodes[2].strip(),
                        "label": str(index) if node_size < 4 else line_nodes[3].strip(),
                    })
            data_frame: pandas.DataFrame = pandas.DataFrame(elements)
            geo_frame: geopandas.GeoDataFrame = geopandas.GeoDataFrame(data_frame,
                                                                       geometry=geopandas.points_from_xy(
                                                                           data_frame.long,
                                                                           data_frame.lat),
                                                                       crs=self.crs)
            return self._GeoFrame(geo_frame, None)

    def _GeoSeries(self, records: geopandas.GeoSeries, definition: None = None) -> None:
        """
        GeoSeries save override
        :param records: geopandas.GeoSeries record
        :param definition: Ignored in this instance, used strictly for geometry
        :return: None
        """
        return self._GeoJSON(records.to_json(), definition)

    def _GeoFrame(self, records: geopandas.GeoDataFrame, definition: None = None) -> None:
        """
        GeoSeries save override
        :param records: geopandas.GeoSeries record
        :param definition: Ignored for geodata frames, but must include a geometry field.
        :return: None
        """
        return self._GeoSeries(records.geometry, definition)

    def _DataFrame(self, records: pandas.DataFrame, definition: [str, None] = None) -> None:
        """
        Dataframe save override
        :param records: pandas DataFrame record
        :param definition: Definition must point to a column that points to the geometry field of the dataframe
        :return: None
        """
        column: str = "geometry" if definition is None else str(definition)
        return self._GeoFrame(geopandas.GeoDataFrame(records, geometry=column), None)

    def _List(self, records: [List[str], List[numpy.ndarray], List[List[float]]], definition: None = None):
        """
        List processor
        :param records: List of records, this could be:
            - List of geometry WKT strings ie. ["POINT (0 1)"]
            - List of numpy array points which should include a x, y and optional z and m coordinates if m is not
            provided z will be assumed for m.
                Arrays are considered and interpeted as multipolygon data
        :param definition: No definition is required
        :return: None
        """
        if len(records) > 0:
            if isinstance(records[0], str):
                return self.save(PyArrow.as_geoarrow(records), definition)
            # TODO write sensor for polygon or multipolygon
            elif isinstance(records[0], List):
                x: list = records[0]
                y: [list, None] = None if len(records) == 1 else records[1]
                z: [list, None] = None if len(records) < 3 else records[2]
                m: [list, None] = None if len(records) < 4 else records[3]
                return self._ArrowArray(PyArrow.polygon().from_geobuffers(None, [], [], x, y, z, m), definition)
            elif isinstance(records[0], numpy.ndarray):
                x: numpy.ndarray = records[0]
                y: [numpy.ndarray, None] = None if len(records) == 1 else records[1]
                z: [numpy.ndarray, None] = None if len(records) < 3 else records[2]
                m: [numpy.ndarray, None] = None if len(records) < 4 else records[3]
                return self._ArrowArray(PyArrow.polygon().from_geobuffers(None, [], [], x, y, z, m), definition)
            else:
                raise ValueError(f"List of types {type(records)} is not recognized.")

    def _Dictionary(self,
                    records: [Dict[str, List[float]],
                              Dict[str, numpy.ndarray],
                              List[Dict]],
                    definition: str = "geometry") -> None:
        """
        Dictionary Processor
        :param records: A dictionary object this could be:
            - A dictionary of arrays with a geometry field defined by the `definition` argument.
            - A list of dictionary with field pointing to geometry field defined in the `definition` argument.
        :param definition: Dictionary field pointing to a geometry field
        :return: None
        """
        if isinstance(records, dict):
            if Library.is_geojson(records):
                return self._GeoJSON(records, None)
            if definition in records:
                return self._List(list(records[definition]), None)
        if isinstance(records, list):
            if len(records) > 0:
                elements: List[Any] = list([])
                for record in records:
                    if definition in record:
                        elements.append(record[definition])
                return self._Dictionary(elements, definition)
        raise ValueError("Invalid dictionary in geometry, this might not contain a field or might be of the wrong type")

    def _GeoJSON(self,
                 records: [dict, geojson.GeoJSON],
                 definition: None = None):
        """
        Geojson processor
        :param records: JSON or GeoJSON Data
        :param definition: No definition required for GeoJSON
        :return: None
        """
        if Library.is_geojson(records):
            json_string: str = geojson.dumps(records).encode('raw_unicode_escape').decode('unicode_escape')
            json_string = json_string[1:] if json_string.startswith("\"") else json_string
            json_string = json_string[:-1] if json_string.endswith("\"") else json_string
            self.write(json_string, DataType.STRING)

    def _ArrowArray(self,
                    records: pyarrow.Array,
                    definition: None = None) -> None:
        """
        GeoArrow Array processor
        :param records: Arrow Array of geometries
        :param definition: None
        :return: None
        """
        return self._GeoJSON(PyArrow.to_geopandas(records).to_json())

    def _ArrowTable(self,
                    records: pyarrow.Table,
                    definition: [str, None] = None) -> None:
        """
        Arrow Table processor
        :param records: Arrow Table object
        :param definition: Column definition for geometry field, by default this is set to "geometry"
        :return: None
        """
        column: str = "geometry" if definition is None else str(definition)
        return self._ArrowArray(records.column(column))

    def _Numpy(self,
               records: numpy.ndarray,
               definition: None = None):
        """
        Numpy array processor
        :param records: Numpy array of geometries
        :param definition: None
        :return: None
        """
        return self._List(list([records]), None)
