import os.path
import pathlib
from typing import List, Tuple, Any

import geopandas
import numpy
import pandas

from pydggrid.Types import DataType
from pydggrid.Input._Template import Template as InputTemplate


class Input(InputTemplate):

    def __init__(self):
        super(Input, self).__init__()
        self.data: List[List[str]] = list([])

    # Override
    def copy(self, source_object: Any) -> None:
        """
        Copies the source object to local
        :return:
        """
        if isinstance(source_object, Input):
            self.data = source_object.data
            super().copy(source_object)

    def save(self, data: [List[int],
                          numpy.ndarray,
                          pandas.DataFrame,
                          geopandas.GeoDataFrame,
                          Tuple[str, str],
                          Tuple[str, str, str]],
             column: [int, str, None] = None) -> None:
        """
        Saves a sequence into the data array
        :param data: Data to save this can be:
            - List of integers used as a sequence
            - A numpy.ndarray, in which the column value must be provided as a numeric index, if not provided this index
                will default to `0`.
            - A pandas dataframe, in which the column parameter must be provided as a string or numeric index, by
                default this index is set to 0, or first column.
            - A Geo pandas dataframe, in which the column parameter must be provided as a string or numeric index, by
                default this index is set to 0, or first column.
            - A tuple with two elements to generate a range from (start, end)
            - A tuple with three elements to generate a range from (start, end, step)
        :param column: Column index or name, depending on data provided
            - Integer column index which works for numpy and data-frames.
            - String index which is only used for data frames
        :return: None
        """
        if isinstance(data, tuple):
            if len(data) == 2:
                return self.save_range(data[0], data[1])
            elif len(data) == 3:
                return self.save_range(data[0], data[1], data[2])
            else:
                raise ValueError("Invalid sequence range provided in input")
        elif isinstance(data, list):
            return self.save_list(data)
        elif isinstance(data, numpy.ndarray):
            return self.save_numpy(data, column)
        elif isinstance(data, pandas.DataFrame) or isinstance(data, geopandas.GeoDataFrame):
            return self.save_frame(data, column)

    def read(self, file_path: [str, pathlib.Path]) -> None:
        """
        Reads a file and saves into sequence records
        :param file_path: File path to read, this target file must be a text file containing a sequence number for
            each individual line.
        :return: None
        """
        if isinstance(file_path, str):
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"Invalid file path {file_path}'")
            return self.read(pathlib.Path(file_path))
        elif isinstance(file_path, pathlib.Path):
            elements: List[str] = list([])
            with open(file_path.absolute(), 'r', encoding='UTF-8') as file:
                while line := file.readline():
                    line_t: str = line.strip()
                    if line_t:
                        elements.append(str(line_t))
            if len(elements) > 0:
                self.save_list(elements)

    def save_range(self, start: int, end: int, step: int = 1) -> None:
        """
        Inserts a range of numbers
        :param start: Start Integer
        :param end: End Integer
        :param step: Step per integer, default is set to 1
        :return: None
        """
        self.save_list([str(n) for n in list(range(start, end, step))])

    def save_list(self, data: List[str]) -> None:
        """
        Inserts a list of integers into the payload
        :param data: List of integers
        :return: None
        """
        self.data.append([str(n) for n in data])
        self.records.save(self.data[len(self.data) - 1], DataType.STRING)

    def save_numpy(self, data: numpy.ndarray, column: [int, None] = None) -> None:
        """
        Inserts a numpy column into the collection
        :param data: Numpy Array
        :param column: Column index, must be an integer pointing to column #
        :return: None
        """
        column_t: int = 0 if column is None else column
        self.save_list(list(data[:, column_t].tolist()))

    def save_frame(self, data: [pandas.DataFrame, geopandas.GeoDataFrame], column: [int, str] = 0) -> None:
        """
        Inserts a column from a data frame object
        :param data: DataFrame object can be a GeoDataFrame or a standard DataFrame
        :param column: Column name or numeric index to retrieve sequence from
        :return: None
        """
        index_t: int = column if isinstance(column, int) else data.columns.get_loc(column)
        self.save_list(list(data.iloc[:, index_t].tolist()))

    # Override
    def __str__(self) -> str:
        """
        Returns description of input object
        :return: Description String
        """
        elements: List[str] = list([])
        elements.append("DATA:")
        [elements.append(f"\t{n}") for n in self.data]
        elements.append(super().__str__())
        return os.linesep.join(elements)
