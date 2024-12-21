import os
import pathlib
import sys
from io import StringIO
from typing import List, Dict, Any

import geopandas
import numpy
import pandas

import pyarrow

from pydggrid.Interfaces import Dataset
from pydggrid.System import Library
from pydggrid.Types import DataType


class Input(Dataset):

    def __init__(self):
        super(Input, self).__init__()
        super().register_call(list, self._List)
        super().register_call(str, self._String)
        super().register_call(dict, self._Dictionary)
        super().register_call(numpy.ndarray, self._Numpy)
        super().register_call(pandas.DataFrame, self._DataFrame)
        super().register_call(geopandas.GeoDataFrame, self._GeoFrame)
        super().register_extension("csv", self._CsvFile)
        super().register_extension("json", self._JsonFile)
        super().register_extension("arrow", self._ArrowFile)
        super().register_extension("txt", self._TextFile)

    def save(self, records: [Any], definition: Any) -> None:
        """
        Saves records into dataset
        :param records: Records to save into the buffer, this parameter can be:
            - A list of strings comprised of integers or float values
            - A line seperated list of strings comprised of integer or float values
            - A dictionary of lists which should be accompanied by the dictionary key name to use.
            - A pandas data frame which should be accompanied by the dictionary key name to use.
            - A geopandas data frame which should be accompanied by the dictionary key name to use.
            - An arrow table which should be accompanied by the dictionary key name to use.
            - A numpy single dimensional array
            - a csv string which should be accompanied by the dictionary key name to use.
        :param definition: Depending on object passed, but normally accompanies the field name to use for the list
        values
        :return: None
        """
        return super().save(records, definition)

    def read(self, file_path: [str, pathlib.Path], definition: [str, None]) -> None:
        """
        Reads data from a file
        :param file_path: File path as string or a pathlib.Path object which points to:
            - a CSV File, which should be accompanied by the dictionary key name to use.
            - an arrow file which should be accompanied by the dictionary key name to use.
            - A line seperated file which should contain integers or float values per line
        :param definition: Depending on file type, this argument must contain the oclumn name to get the list from.
        :return: None
        """
        return super().read(file_path, definition)

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

    def _TextFile(self, file_path: pathlib.Path, file_bytes: bytes, definition: Any) -> None:
        """
        Processes Text File
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
            - A CSV string, containing fields that pertain to or mapped to in the definition argument as "lat", "long",
            "id", "name"
            - A space or tab seperated file containing fields in the order of "lat", "long", "id", "name"
        :param definition: Dictionary based field definition:
            {
                "id": <id-field>,
                "name" <label-field>,
                "lat": <latitude-field>,
                "long": <longitude-field>
            }
        :return:
        """
        if Library.is_csv_string(records):
            # noinspection PyTypeChecker
            data_frame: pandas.DataFrame = pandas.read_csv(StringIO(records))
            return self._DataFrame(data_frame, definition)
        else:
            lines: List[str] = records.split(os.linesep)
            elements: List[str] = [str(n).strip() for n in lines if n.strip() != ""]
            return self._List(elements, None)

    def _Numpy(self, records: numpy.ndarray, definition: None = None):
        """
        List processor
        :param records: List of records, this could be:
            - List of dictionaries containing "lat", "long", "id", "name" fields or mapping defined in the definition
            file to those fields.
            - A Dictionary of arrays with columns containing "lat", "long", "id", "name" or mapping defined in the
            definition argument mapping "lat", "long", "id", "name" fields.
        :param definition: Dictionary based field definition:
            {
                "id": <id-field>,
                "name" <label-field>,
                "lat": <latitude-field>,
                "long": <longitude-field>
            }
        :return: None
        """
        return self._List(records.tolist(), None)

    def _List(self, records: [List[str], List[int], List[float]], definition: None = None):
        """
        List processor
        :param records: List of records, this could be:
            - List of dictionaries containing "lat", "long", "id", "name" fields or mapping defined in the definition
            file to those fields.
            - A Dictionary of arrays with columns containing "lat", "long", "id", "name" or mapping defined in the
            definition argument mapping "lat", "long", "id", "name" fields.
        :param definition: Dictionary based field definition:
            {
                "id": <id-field>,
                "name" <label-field>,
                "lat": <latitude-field>,
                "long": <longitude-field>
            }
        :return: None
        """
        if isinstance(records, list) and len(records) > 0:
            self._WriteOut([str(n).strip() for n in records if str(n).strip() is not ""])
        else:
            raise ValueError(f"List of types {type(records)} is not recognized.")

    def _Dictionary(self, records: [Dict[str, List]], definition: [str, None] = None) -> None:
        """
        Dictionary Processor
        :param records: A dictionary object this could be:
            - A dictionary of arrays with a geometry field defined by the `definition` argument.
            - A list of dictionary with field pointing to geometry field defined in the `definition` argument.
        :param definition: Dictionary field pointing to a geometry field
        :return: None
        """
        if isinstance(records, dict):
            column: str = definition if isinstance(definition, str) \
                                        and definition in records.keys() else records.keys()[0]
            if column in records.keys() and isinstance(records[column], list):
                return self._List(records[column])
        raise ValueError("Dictionary object must contain an array to pass onto a List Object.")

    def _ArrowTable(self, records: pyarrow.Table, definition: [Dict[str, str], None] = None) -> None:
        """
        Arrow Table processor
        :param records: Arrow Table object
        :param definition: Column definition for geometry field, by default this is set to "geometry"
        :return: None
        """
        if records.shape[0] > 0:
            column: str = definition if isinstance(definition, str) \
                                        and definition in records.columns else records.columns[0]
            return self._List(list(records[column].to_list()))

    def _GeoFrame(self, records: geopandas.GeoDataFrame, definition: None = None) -> None:
        """
        GeoSeries save override
        :param records: geopandas.GeoSeries record
        :param definition: Ignored for geodata frames, but must include a geometry field.
        :return: None
        """
        return self._DataFrame(pandas.DataFrame(records), definition)

    def _DataFrame(self, records: pandas.DataFrame, definition: [List[str], None] = None) -> None:
        """
        Dataframe save override
        :param records: pandas DataFrame record
        :param definition: Definition must point to a single field containing
        :return: None
        """
        if records.shape[0] > 0:
            column: str = definition if isinstance(definition, str) \
                                        and definition in records.columns else records.columns[0]
            return self._List(list(records[column].to_list()), None)

    def _WriteOut(self, records: List[str]) -> None:
        """
        Writes records to buffer
        :param records: Records DataFrame
        :return: None
        """
        self.write(os.linesep.join(records), DataType.STRING)

    def _anti_static(self) -> None:
        """
        Anti-static function
        :return: None
        """
        pass
