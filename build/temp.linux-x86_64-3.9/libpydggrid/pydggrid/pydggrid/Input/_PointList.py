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
from pydggrid.Types import DataType, PointDataType


class Input(Dataset):

    def __init__(self):
        super(Input, self).__init__()
        super().register_call(list, self._List)
        super().register_call(str, self._String)
        super().register_call(dict, self._Dictionary)
        super().register_call(geojson.GeoJSON, self._GeoJSON)
        super().register_call(pandas.DataFrame, self._DataFrame)
        super().register_call(geopandas.GeoSeries, self._GeoSeries)
        super().register_call(geopandas.GeoDataFrame, self._GeoFrame)
        super().register_extension("csv", self._CsvFile)
        super().register_extension("txt", self._TextFile)
        super().register_extension("geo", self._TextFile)
        super().register_extension("json", self._JsonFile)
        super().register_extension("geojson", self._JsonFile)
        super().register_extension("shp", self._ShapeFile)
        super().register_extension("arrow", self._ArrowFile)
        self.cols: Dict[str, Any] = dict({"x": "x",
                                          "y": "y",
                                          "id": "id",
                                          "label": "label"})
        self.type: PointDataType = PointDataType.TEXT

    def save(self, records: [Any], definition: Any) -> None:
        """
        Saves records into dataset
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
        return super().save(records, definition)

    def read(self, file_path: [str, pathlib.Path], definition: [List[str], List[int], str, None]) -> None:
        """
        Reads data from a file
        :param file_path: File path as string or a pathlib.Path object which points to:
            - a CSV File, which in this case you must provide the definition as the field name of the geometry data or
            x, y columns
            - a GeoJson file
            - an arrow file containing polygons
            - a pandas dataframe, with the definition provided as a string containing the geometry column name.  By
            default, this argument is set to `geometry`.
            - An arrow file containing an array or table, if table the definition argument can be provided to declare
            the geometry column, by default, this argument is `geometry`.
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
            - A space delimited string in the format x, y, id, Label, the string must at least contain an X, Y column
        :param definition: Definition argument must contain the mappings for lat, long, ID, Label
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
            columns: Dict[str, int] = self._GetColumns(definition, True)
            line_set: List[str] = records.split(os.linesep)
            for index, line_element in enumerate(line_set):
                line_node: List[str] = line_element.split(" ")
                line_nodes: List[str] = [n.strip() for n in line_node if n.strip() != ""]
                node_size: int = len(line_nodes)
                if columns["x"] < node_size and Library.is_float(line_nodes[columns["x"]]) \
                        and columns["y"] < node_size and Library.is_float(line_nodes[columns["y"]]):
                    elements.append({
                        "x": float(line_nodes[columns["x"]]),
                        "y": float(line_nodes[columns["y"]]),
                        "id": str(line_nodes[columns["id"]]) if columns["id"] < node_size else str(index),
                        ":label": str(line_nodes[columns["label"]]) if columns["label"] < node_size else f"P{index}"
                    })
            data_frame: pandas.DataFrame = pandas.DataFrame(elements)
            self._DataFrame(data_frame, None)

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
        columns: Dict[str, str] = self._GetColumns(definition, False)
        for column_name in columns:
            if columns[column_name] != column_name and column_name in records.columns:
                records.rename(columns={columns[column_name]: column_name}, inplace=True)
        return self.write(str(records.to_csv(sep=' ', index=False, header=False)), DataType.STRING)

    def _List(self,
              records: [List[str], numpy.ndarray, List[List[float]], List[Dict[str, Any]]],
              definition: None = None):
        """
        List processor
        :param records: List of records, this could be:
            - List of geometry WKT strings ie. ["POINT (0 1)"]
            - List of point tuples (float, float)
            - List of dictionaries containing definition mapped x, y, and optional id, label components
            - List of numpy array points which should include a x, y and optional id and label components
            provided z will be assumed for m.
                Arrays are considered and interpreted as point data
        :param definition: No definition is required
        :return: None
        """
        if len(records) > 0:
            if isinstance(records[0], str):
                return self.save(PyArrow.as_geoarrow(records), definition)
            # TODO write sensor for polygon or multipolygon
            elif isinstance(records[0], dict):
                return self._DataFrame(records, definition)
            elif isinstance(records[0], list) or isinstance(records, numpy.ndarray):
                list_size: int = len(records)
                columns: Dict[str, int] = self._GetColumns(definition, True)
                return self._DataFrame(pandas.DataFrame.from_dict({
                    "x": list(records[columns["x"]]),
                    "y": list(records[columns["y"]]),
                    "id": records[columns["id"]] if columns["id"] < list_size else list(range(0, list_size)),
                    "label": records[columns["label"]] if columns["label"] < list_size else list(range(0, list_size))
                }))
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
            return self._DataFrame(pandas.DataFrame.from_dict(records), definition)
        if isinstance(records, list):
            return self._DataFrame(pandas.DataFrame(records), definition)
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

    def _GetColumns(self, definition: [Dict[str, Any], List[str], List[int]],
                    as_integer: bool = False) -> Dict[str, Any]:
        """
        Gets column info for various systems
        :param definition: Dictionary definition
        :param as_integer: If enabled column assignments return as integers
        :return: List
        """
        elements: Dict[str, Any] = dict(self.cols)
        if isinstance(definition, dict):
            for column_index, column_name in enumerate(self.cols.keys()):
                if column_name in definition.keys():
                    elements[column_name] = int(definition[column_name]) if str(definition[column_name]).isnumeric() \
                        else str(definition[column_name])
        if as_integer is True:
            for column_index, column_name in enumerate(self.cols.keys()):
                elements[column_name] = int(elements[column_name]) \
                    if str(elements[column_name]).isnumeric() else column_index
        return elements

    def _un_static(self) -> None:
        """
        Un static function
        :return: None
        """
        pass
