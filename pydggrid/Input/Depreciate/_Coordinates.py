import os
import pathlib
from io import StringIO
from typing import List, Dict, Any, Callable

import geojson
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
        self.fields: List[str] = list(["lat", "long", "id", "name"])
        super().register_call(list, self._List)
        super().register_call(str, self._String)
        super().register_call(dict, self._Dictionary)
        super().register_call(geojson.GeoJSON, self._GeoJSON)
        super().register_call(pandas.DataFrame, self._DataFrame)
        super().register_call(geopandas.GeoDataFrame, self._GeoFrame)
        super().register_extension("csv", self._CsvFile)
        super().register_extension("json", self._JsonFile)
        super().register_extension("arrow", self._ArrowFile)
        super().register_extension("text", self._TextFile)

    def save(self, records: [Any], definition: Any) -> None:
        """
        Saves records into dataset
        :param records: Records to save into the buffer, this parameter can be:
            - A path string or a pathlib.Path object point to file that is readable by the read parameter.
            - A List of dictionaries or a Dictionary of lists containing connecting data fields provided in the
            definition argument.
            - A string value containing either geojson or csv data
            - a pandas dataframe, with columns matching the "lat", "long", "id", "name" layout or mapped in the
            definition argument.
            - a geopandas dataframe, with columns matching the "lat", "long", "id", "name" layout or mapped in the
            definition argument.
            - a geojson dictionary object
            - a pyarrow table, with columns matching the "lat", "long", "id", "name" layout or mapped in the definition
            argument.
        :param definition: Dictionary based field definition:
            {
                "id": <id-field>,
                "name" <label-field>,
                "lat": <latitude-field>,
                "long": <longitude-field>
            }
        :return: None
        """
        return super().save(records, definition)

    def read(self, file_path: [str, pathlib.Path], definition: [List[str], List[int], str, None]) -> None:
        """
        Reads data from a file
        :param file_path: File path as string or a pathlib.Path object which points to:
            - a CSV File, with columns matching the "id", "name", "lat", "long" layout or mapped in the definition
            argument.
            - a GeoJson file.
            - an arrow file containing a table with columns matching the "lat", "long", "id", "name" layout or mapped
            in the definition argument.
            - a pandas dataframe, with columns matching the "lat", "long", "id", "name" layout or mapped in the
            definition argument.
        :param definition: Dictionary based field definition:
            {
                "id": <id-field>,
                "name" <label-field>,
                "lat": <latitude-field>,
                "long": <longitude-field>
            }
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
        if Library.is_geojson(records):
            return self._GeoJSON(geojson.loads(records))
        elif Library.is_csv_string(records):
            # noinspection PyTypeChecker
            data_frame: pandas.DataFrame = pandas.read_csv(StringIO(records))
            return self._DataFrame(data_frame, definition)
        else:
            lines: List[str] = records.split(os.linesep)
            field_names: List[str] = self._GetFields(definition)
            elements: Dict[str, List[Any]] = {n: [] for n in field_names}
            for line in lines:
                record_set_t: List[str] = line.split(" ")
                record_set: List[str] = [n.strip() for n in record_set_t if n.strip() != ""]
                if len(record_set) >= len(field_names):
                    for index, field_name in enumerate(field_names):
                        elements[field_name].append(record_set[index])

    def _List(self, records: [List[Dict, List]], definition: None = None):
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
            if isinstance(records[0], dict):
                return self._DataFrame(pandas.DataFrame(records), definition)
            elif isinstance(records[0], list):
                elements: List[Dict] = []
                field_names: List[str] = self._GetFields(definition)
                for record in records:
                    elements.append({field_names[index]: value for index, value in enumerate(record)})
                return self._List(elements, definition)
        else:
            raise ValueError(f"List of types {type(records)} is not recognized.")

    def _Dictionary(self,
                    records: [Dict[str, List[Any]],
                              Dict[str, numpy.ndarray],
                              List[Dict]],
                    definition: [List[str], None] = None) -> None:
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
            field_names: List[str] = self._GetFields(definition)
            drop_fields: List[str] = [n for n in records.keys() if n in field_names]
            for n in drop_fields:
                del records[n]
            return self._DataFrame(pandas.DataFrame.from_dict(records), None)
        if isinstance(records, list):
            return self._List(records, definition)
        raise ValueError("Invalid dictionary in Coordinates, this might not contain a field or might be "
                         "of the wrong type")

    def _GeoJSON(self, records: [dict, geojson.GeoJSON], definition: None = None):
        """
        Geojson processor
        :param records: JSON or GeoJSON Data
        :param definition: No definition required for GeoJSON
        :return: None
        """
        if Library.is_geojson(records):
            self._GeoFrame(geopandas.GeoDataFrame.from_features(geojson.loads(records)["features"]))

    def _ArrowTable(self, records: pyarrow.Table, definition: [Dict[str, str], None] = None) -> None:
        """
        Arrow Table processor
        :param records: Arrow Table object
        :param definition: Column definition for geometry field, by default this is set to "geometry"
        :return: None
        """

        field_set: List[str] = self._GetFields(definition)
        drop_list: List[str] = [n for n in records.columns if str(n) not in field_set]
        [records.drop_columns(n) for n in drop_list]
        return self._DataFrame(records.to_pandas(), None)

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
        :param definition: Definition must point to a column that points to the geometry field of the dataframe
        :return: None
        """
        field_set: List[str] = self._GetFields(definition)
        drop_list: List[str] = [n for n in records.columns if str(n) not in field_set]
        [records.drop_columns(n) for n in drop_list]
        return self._WriteOut(records)

    def _GetFields(self, definition: [Dict, None] = None) -> List[str]:
        """
        Field Mapping from definition
        :param definition: Definition dictionary
        :return: List of fields pertaining to latitude, longitude, id and name
        """
        if definition is None:
            return self.fields
        field_names: List[str] = list([])
        for field_name in self.fields:
            field_names.append(definition[field_name] if field_name in definition else field_name)
        return field_names

    def _CheckDefinition(self, definition: Dict) -> None:
        """
        Checks definition dictionary for parameters
        :param definition: Definition Dictionary
        :return: None
        """
        if "latitude" not in definition:
            raise AttributeError("You must include a `lat` field within your field definition.")
        if "longitude" not in definition:
            raise AttributeError("You must include a `long` field within your field definition.")
        if "id" not in definition:
            raise AttributeError("You must include an `id` field within your field definition.")
        if "label" not in definition:
            raise AttributeError("You must include an `label` field within your field definition.")
        self._anti_static()

    def _WriteOut(self, records: pandas.DataFrame) -> None:
        """
        Writes records to buffer
        :param records: Records DataFrame
        :return: None
        """
        byte_array: List[bytes] = list()
        record_size: int = records.shape[0]
        byte_array.append(DataType.INT.convert_bytes(record_size))
        for index, record in records.iterrows():
            byte_array.append(DataType.FLOAT.convert_bytes(record["lat"]))
            byte_array.append(DataType.FLOAT.convert_bytes(record["long"]))
            byte_array.append(DataType.INT.convert_bytes(record["id"]))
            byte_array.append(DataType.INT.convert_bytes(len(str(record["label"]))))
            byte_array.append(str(record["label"]).encode())
        return self.write(b''.join(byte_array), DataType.LOCATION)

    def _anti_static(self) -> None:
        """
        Anti-static function
        :return: None
        """
        pass
