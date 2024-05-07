import os
import pathlib
from typing import Dict, Any, List

import geopandas
import pandas

from pydggrid.Input._Template import Template as InputTemplate
from pydggrid.Types import DataType


class Input(InputTemplate):

    def __init__(self):
        super(Input, self).__init__()
        self.frame: pandas.DataFrame = pandas.DataFrame({
            "lat": list([0.0]),
            "long": list([0.0]),
            "id": list([0]),
            "label": list([""])
        })
        self.cols: List[str] = list(self.frame.columns.tolist())
        self.frame = self.frame.iloc[0:0]

    # Override
    def copy(self, source_object: Any) -> None:
        """
        Copies the source object to local
        :return:
        """
        if isinstance(source_object, Input):
            self.frame = source_object.frame
            self.cols = source_object.cols
            super().copy(source_object)

    # Override
    def save(self,
             data: [pandas.DataFrame,
                    geopandas.GeoDataFrame,
                    Dict[str, Any],
                    List[List[Any]],
                    List[Dict[str, Any]]],
             column: [Dict[str, int], Dict[str, str], None] = None) -> None:
        """
        Save data override
        :param data: Saves data to the object, all data must follow the indexing and naming of
            ["lat", "long", "id", "label"].  These values can be remapped by utilizing the column argument, the data
            itself must be one of:
                - A list of dictionaries containing the required fields
                - A list of lists with values corresponding to the required fields
                - A dataframe containing the required fields, these can be remapped by providing the column parameter
                - A geo dataframe containing the required fields, these can be remapped by providing the column
                    parameter
                - A numpy array, which should follow the indexing of the required fields, this can be remapped by using
                    the column argument
        :param column: Column name mapping, should be a dictionary, as
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
        :return: None
        """
        if isinstance(data, pandas.DataFrame) or \
                isinstance(data, geopandas.GeoDataFrame):
            return self.save_frame(data, column)
        if isinstance(data, list):
            return self.save_list(data, column)
        if isinstance(data, dict):
            return self.save_dict(data, column)
        raise ValueError("Invalid data passed to location input.")

    def insert(self, lat: float, long: float, index_id: int, label: str = "UNKNOWN") -> None:
        """
        Inserts a record
        :param lat: Latitude
        :param long: Longitude
        :param index_id: Index ID
        :param label: Location label
        :return: None
        """
        self.frame.loc[-1] = [lat, long, index_id, label]
        self.frame.index = self.frame.index + 1
        self.frame = self.frame.sort_index()
        self._export_frame()

    def save_frame(self,
                   data: [pandas.DataFrame, geopandas.GeoDataFrame],
                   columns: [Dict[str, str], Dict[int, str]]):
        """
        Inserts a dataframe into the buffer
        :param data: Data Frame objects this can be a pandas or geopandas dataframe object
        :param columns: Columns map, this is optional, should be as:
            {
                "lat": <Column Name for latitude in data argument>,
                "long": <Column Name for longitude in data argument>,
                "id": <Column Name for column index in data argument>,
                "name": <Column Name for location name in data argument>
            }
            otherwise it will be assumed the columns of the dataframe contain ["lat", "long", "id", "name"] columns,
            columns can be labelled with integers as well, where the integer points to the column index from data frame
            {
                "lat": 1,
                "long": 2
                ...
            }
        :return:
        """
        map_t: Dict[str, str] = dict(zip(self.cols, self.cols)) if columns is None else \
            {k: columns[k] for k in self.cols}
        for index, row in data.iterrows():
            self.insert(lat=float(row[map_t["lat"]]),
                        long=float(row[map_t["long"]]),
                        index_id=int(row[map_t["id"]]),
                        label=str(row[map_t["label"]]))

    def save_list(self, data: [List[List[Any]], List[Dict[str, Any]]], columns: [List[int], None] = None):
        """
        Reads data into the location frame using a list
        :param data: List of Lists or a list of dictionaries following the lat, long, id, name index.  This indexing can
            be altered by providing a columns argument.
        :param columns: Columns index, needs to represent the order of "lat", "long", "id", "label" appears in the
            list array.
        :return: None
        """
        if len(data) > 0:
            columns_t: List[int] = list(range(0, len(self.cols))) if columns is None else columns
            if isinstance(data[0], list):
                indexes: List[int] = list(range(0, len(data)))
                for index in indexes:
                    record: Dict[str, Any] = {self.cols[n]: data[index][n] for n in columns_t}
                    self.insert(lat=float(record["lat"]),
                                long=float(record["long"]),
                                index_id=int(record["id"]),
                                label=str(record["lat"]))
                return
            if isinstance(data[0], dict):
                return self.save_dict(data, columns)

    def save_dict(self,
                  data: [Dict[str, Any], List[Dict[str, Any]]],
                  columns: [Dict[str, str], Dict[str, int]]) -> None:
        """
        Saves dictionary data to the records, note that each dictionary item needs to follow the "lat", "long", "id",
        "label" format.
        :param data: Either a single dictionary or a list of dictionaries containing data following the "lat", "long",
        "id", "label" format
        :param columns: Columns mapping this must contain the fields "lat", "long", "id", "label" or their indexes as
            integers.
        :return: None
        """
        if isinstance(data, list):
            [self.save_dict(n, columns) for n in data]
            return
        if isinstance(data, dict):
            map_t: Dict[str, str] = dict(zip(self.cols, self.cols))
            if columns is not None and isinstance(columns, dict):
                index_array: List[int] = list(range(0, len(self.cols)))
                if isinstance(columns["lat"], int):
                    map_t: Dict[str, str] = {self.cols[n]: data.keys()[n] for n in index_array}
                if isinstance(columns["lat"], str):
                    map_t: Dict[str, str] = dict(columns)
            self.insert(lat=float(data[map_t["lat"]]),
                        long=float(data[map_t["long"]]),
                        index_id=int(data[map_t["id"]]),
                        label=str(data[map_t["label"]]))
            return

    def read(self,
             file_path: [str, pathlib.Path],
             ignore_header: bool = False,
             delimiter: str = " ",
             column_order: [List[int], None] = None) -> None:
        """
        Saves a file to a data array,
        :param file_path: File path to read
        :param ignore_header If set to true the first line of file will be ignored
        :param delimiter The delimiter string, by default this is set to " " (Space)
        :param column_order the order of the ["lat", "long", "id", "label"] fields within file, must be a list of
            integers corresponding to the default fields, if none is provided it will be assuemd as [0, 1, 2, 3] for
            lat, long, id, label
        :return: None
        """
        if isinstance(file_path, str):
            return self.read(pathlib.Path(file_path), ignore_header, delimiter, column_order)
        if isinstance(file_path, pathlib.Path):
            index_array: List[int] = list(range(0, len(self.cols))) if column_order is None else column_order
            with open(file_path.absolute(), 'r', encoding='UTF-8') as file:
                while line := file.readline():
                    line_t: str = line.strip()
                    if not line_t.startswith("#") and not line_t.startswith("/"):
                        try:
                            nodes: List[str] = line_t.split(delimiter)
                            elements: Dict[str, Any] = {self.cols[n]: nodes[n].strip() for n in index_array}
                            self.insert(lat=float(elements["lat"]),
                                        long=float(elements["long"]),
                                        index_id=int(elements["id"]),
                                        label=str(elements["label"]))
                        except Exception:
                            continue

    # Override
    def __str__(self) -> str:
        """
        Returns description of input object
        :return: Description String
        """
        elements: List[str] = list([])
        elements.append("DATA:")
        max_columns: int = pandas.get_option("display.max_columns")
        pandas.set_option("display.max_columns", None)
        elements.append(self.frame.__str__())
        pandas.set_option("display.max_columns", max_columns)
        elements.append(super().__str__())
        return os.linesep.join(elements)

    # INTERNAL

    def _export_frame(self) -> None:
        """
        Exports the current frame to byte records
        :return: None
        """
        lat_bytes: List[bytes] = [DataType.FLOAT.convert_bytes(float(n)) for n in list(self.frame["lat"])]
        long_bytes: List[bytes] = [DataType.FLOAT.convert_bytes(float(n)) for n in list(self.frame["long"])]
        id_bytes: List[bytes] = [DataType.INT.convert_bytes(int(n)) for n in list(self.frame["id"])]
        label_bytes: List[bytes] = [str(n).encode() for n in list(self.frame["label"])]
        self.records.clear()
        self.records.save(b''.join(lat_bytes), DataType.FLOAT)
        self.records.save(b''.join(long_bytes), DataType.FLOAT)
        self.records.save(b''.join(id_bytes), DataType.INT)
        self.records.save(b''.join(label_bytes), DataType.STRING)
