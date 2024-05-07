import os
import pathlib
import sys
from typing import List, Any, Tuple
from pydggrid.Types import DataType


class Object:

    def __init__(self):
        """
        Default constructor
        """
        self._data: List[bytes] = list([])
        self._type: List[DataType] = list([])

    def clear(self) -> None:
        """
        Clears all internal records
        :return: None
        """
        self._data.clear()
        self._type.clear()

    def size(self) -> int:
        """
        Returns number of data blocks available for record set
        :return: Record set count
        """
        return len(self._data)

    def source(self) -> Tuple[List[bytes], List[DataType]]:
        """
        Returns internal data as a tuple of byte arrays and their data tyes
        :return: Tuple of (byte arrays, Data types)
        """
        return tuple((self._data, self._type))

    def __bytes__(self) -> bytes:
        """
        Returns the payload as a bytes array
        :return: Payload Byte array
        """
        byte_array: List[bytes] = list()
        byte_array.append(DataType.INT.convert_bytes(self.size()))
        index_range: List[int] = list(range(0, len(self._data)))
        for index in index_range:
            byte_array.append(DataType.INT.convert_bytes(int(self._type[index])))
            byte_array.append(DataType.INT.convert_bytes(len(self._data[index])))
            byte_array.append(self._data[index])
        return b''.join(byte_array)

    def copy(self, source_object: Any) -> None:
        """
        Copies from a remote object if compatible
        :param source_object: Source Object
        :return: None
        """
        if isinstance(source_object, Object):
            elements: Tuple[List[bytes], List[DataType]] = source_object.source()
            self._data = list(elements[0])
            self._type = list(elements[1])

    def save(self, data: [bytes, str, pathlib.Path, List[Any]], data_type: DataType) -> None:
        """
        Saves bytes to the records set
        :param data: Data to save into buffer:
            - bytes will save directly into data set
            - str will encode string data and save into dataset
            - pathlib.Path object will load a file and save binary data into records
        :param data_type: Data Type definition
        :return: None
        """
        if isinstance(data, str):
            byte_data: List[bytes] = list([])
            byte_data.append(DataType.INT.convert_bytes(len(data)))
            byte_data.append(str(data).encode())
            return self.save(b''.join(byte_data), data_type)
        elif isinstance(data, pathlib.Path):
            file = open(pathlib.Path(data).absolute(), "rb")
            byte_data: bytes = file.read()
            file.close()
            return self.save(byte_data, data_type)
        elif isinstance(data, list):
            byte_array: List[bytes] = list([])
            byte_array.append(DataType.INT.convert_bytes(len(data)))
            [byte_array.append(data_type.convert_bytes(n)) for n in data]
            return self.save(b''.join(byte_array), data_type)
        elif isinstance(data, bytes):
            self._data.append(data)
            self._type.append(data_type)
        else:
            raise ValueError("Unrecognized input values")

    def __str__(self) -> str:
        """
        String output
        :return: String to output when records object is printed
        """
        elements: List[str] = list([])
        index_range: List[int] = list(range(0, len(self._data)))
        [elements.append(f"{n} ({len(self._data[n])}): {self._data[n].hex()}") for n in index_range]
        return os.linesep.join(elements)
