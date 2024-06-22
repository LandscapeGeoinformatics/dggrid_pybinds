import os
import pathlib
import sys
from typing import List, Tuple, Dict, Any

import geopandas
import pandas

from pydggrid.Input._Template import Template as InputTemplate
from pydggrid.Types import DataType


class Input(InputTemplate):

    def __init__(self):
        super(Input, self).__init__()
        self.data: Dict[int, List[Tuple[float, float]]] = dict({})
        self.cols: List[str] = ["id", "lat", "long"]

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
            ["id, "lat", "long"].  These values can be remapped by utilizing the column argument, the data
            itself must be one of:
                - A list of dictionaries containing the required fields
                - A list of lists with values corresponding to the required fields
                - A dataframe containing the required fields, these can be remapped by providing the column parameter
                - A geo dataframe containing the required fields, these can be remapped by providing the column
                    parameter
                - A numpy array, which should follow the indexing of the required fields, this can be remapped by using
                    the column argument
            Similar to coordinate entries this function will group the data by id field.
        :param column: Column name mapping, should be a dictionary, as
            {
                "id": "<id>",
                "lat": "<lat-equivalent-field>",
                "long": "<lat-equivalent-field>",
            }

            .. or, a dictionary of indexes as:
            {
                "id": 0,
                "lat": 1,
                "long": 2
            }
        :return: None
        """
        if isinstance(data, pandas.DataFrame) or \
                isinstance(data, geopandas.GeoDataFrame):
            return self.save_frame(data, column)
        if isinstance(data, list):
            return self.save_list(data[0][0], data, column)
        if isinstance(data, dict):
            return self.save_dict(data, column)
        raise ValueError("Invalid data passed to location input.")

    # Override
    def copy(self, source_object: Any) -> None:
        """
        Copies the source object to local
        :return:
        """
        if isinstance(source_object, Input):
            self.data = source_object.data
            self.cols = source_object.cols
            super().copy(source_object)

    def insert(self, index_id: int, lat: float, long: float) -> None:
        """
        Inserts a record
        :param lat: Latitude
        :param long: Longitude
        :param index_id: Index ID
        :return: None
        """
        if index_id not in self.data:
            self.data[index_id] = list()
        self.data[index_id].append((lat, long))
        self._export_frame()

    def save_frame(self,
                   data: [pandas.DataFrame, geopandas.GeoDataFrame],
                   columns: [Dict[str, str], Dict[int, str]]):
        """
        Inserts a dataframe into the buffer
        :param data: Data Frame objects this can be a pandas or geopandas dataframe object
        :param columns: Columns map, this is optional, should be as:
            {
                "id": <id number>
                "lat": <Column Name for latitude in data argument>,
                "long": <Column Name for longitude in data argument>,
            }
            otherwise it will be assumed the columns of the dataframe contain ["lat", "long", "id", "name"] columns,
            columns can be labelled with integers as well, where the integer points to the column index from data frame
            {
                "id": 0,
                "lat": 1,
                "long": 2
            }
            entries will be grouped by ID
        :return:
        """
        map_t: Dict[str, str] = dict(zip(self.cols, self.cols)) if columns is None else \
            {k: columns[k] for k in self.cols}
        for index, row in data.iterrows():
            self.insert(index_id=row[map_t["id"]], lat=float(row[map_t["lat"]]), long=float(row[map_t["long"]]))

    def save_list(self,
                  index_id: int,
                  data: [List[List[float]],
                         List[Dict[str, Any]]],
                  columns: [List[int], None] = None):
        """
        Reads data into the location frame using a list
        :param index_id: index ID list of the coordinate set
        :param data: List of Lists or a list of dictionaries following the lat, long index.  This indexing can be
            altered by providing a `columns` argument.
        :param columns: Columns index, needs to represent the order of "lat", "long" appears in the list array.
        :return: None
        """
        if len(data) > 0:
            columns_t: List[int] = list(range(0, len(self.cols))) if columns is None else columns
            if isinstance(data[0], list):
                indexes: List[int] = list(range(0, len(data)))
                for index in indexes:
                    record: Dict[str, Any] = {self.cols[n]: data[index][n] for n in columns_t}
                    self.insert(index_id=index_id, lat=float(record["lat"]), long=float(record["long"]))
                return
            if isinstance(data[0], dict):
                return self.save_dict(data, columns)

    def save_dict(self,
                  data: [Dict[str, Any], List[Dict[str, Any]]],
                  columns: [Dict[str, str], Dict[str, int]]) -> None:
        """
        Saves dictionary data to the records, note that each dictionary item needs to follow the "lat", "long" format.
        :param data: Either a single dictionary or a list of dictionaries containing data following the "lat", "long"
            format
        :param columns: Columns mapping this must contain the fields "lat", "long" or their indexes as integers.
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
            self.insert(index_id=int(data[map_t["id"]]),
                        lat=float(data[map_t["lat"]]),
                        long=float(data[map_t["long"]]))
            return

    def read(self,
             file_path: [str, pathlib.Path],
             ignore_header: bool = False,
             delimiter: str = " ") -> None:
        """
        Saves a file to a data array,
        :param file_path: File path to read
        :param ignore_header If set to true the first line of file will be ignored
        :param delimiter The delimiter string, by default this is set to " " (Space)
        :return: None
        """
        if isinstance(file_path, str):
            return self.read(pathlib.Path(file_path), ignore_header, delimiter)
        if isinstance(file_path, pathlib.Path):
            # index_array: List[int] = list(range(0, len(self.cols)))
            with open(file_path.absolute(), 'r', encoding='UTF-8') as file:
                text: str = file.read()
                elements: List[str] = list([])
                elements_d: List[List[str]] = list([list([]), list([]), list([])])
                elements_t: List[str] = text.split("END")
                [elements_d[0].extend(n.split(os.linesep)) for n in elements_t]
                [elements_d[1].extend(n.split(" ")) for n in elements_d[0]]
                [elements.append(str(n)) for n in elements_d[1] if n.strip() != ""]
                # traverse
                index_id: int = -1
                last_node: str = "long"
                dictionary: Dict[str, Any] = dict({})
                record_set: List[Dict[str, Any]] = list()
                for node in elements:
                    if "." not in node and node.isnumeric():
                        index_id = int(node)
                        dictionary["id"] = index_id
                        continue
                    if "." in node and index_id != -1:
                        node_n: str = "long" if last_node == "lat" else "lat"
                        last_node = node_n
                        dictionary[node_n] = float(node)
                        if node_n == "long":
                            record_set.append(dictionary.copy())
                # group by id
                record_data: Dict[int, List[List[float]]] = {n["id"]: [] for n in record_set}
                [record_data[n["id"]].append(list(n.values())) for n in record_set]
                [self.save_list(n, record_data[n]) for n in record_data]

    # Override
    def __str__(self) -> str:
        """
        Returns description of input object
        :return: Description String
        """
        elements: List[str] = list([])
        elements.append("DATA:")
        index_range: List[int] = list(range(0, len(self.data)))
        elements.append(os.linesep.join([f"{self.data[n][0]}: {self.data[n][1]}, {self.data[n][2]}"
                                         for n in index_range]))
        elements.append(super().__str__())
        return os.linesep.join(elements)

    # INTERNAL

    def _export_frame(self) -> None:
        """
        Exports the current frame to byte records
        :return: None
        """
        elements: List[str] = list([])
        for index_id in self.data:
            elements.append(f"{index_id}")
            for x, y in self.data[index_id]:
                elements.append(f"\t{x} {y}")
            elements.append("END")
        elements.append("END")
        self.records.clear()
        self.records.save(os.linesep.join(elements), DataType.STRING)
