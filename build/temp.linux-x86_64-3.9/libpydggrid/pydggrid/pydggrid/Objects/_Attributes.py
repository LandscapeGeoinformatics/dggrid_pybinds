import importlib
import inspect
import os.path
import pathlib
import struct
import sys
from collections.abc import Callable
from typing import Dict, Any, List

import pydggrid.Objects
from pydggrid.Objects._Options import Object as OptionsObject


class Object:
    """
    Attributes class allows for the storage of data attributes for configuration classes
    _data: Data container
    _text: Text container
    _dictionary: Type container
    _options: Used for options types otherwise None
    _callbacks: Used for validation callbacks
    """

    def __init__(self):
        self._def: Dict[str, Any] = {}
        self._data: Dict[str, Any] = {}
        self._text: Dict[str, str] = {}
        self._dictionary: Dict[str, type] = {}
        self._callbacks: Dict[str, Callable] = {}
        self._on_save: Dict[str, Callable] = {}
        self._options: Dict[str, OptionsObject] = {}

    def type(self, name: str) -> type:
        """
        Returns Parameter Type
        :param name: Parameter Name String
        :return: Parameter Type
        """
        return self._dictionary[name]

    def define(self, name: str,
               data_type: type,
               data_options: [OptionsObject, None] = None,
               data_default: [Any, None] = None,
               on_verify: Callable[[Any], bool] = None,
               text: str = None) -> None:
        """
        Defines a field type
        :param name: Field Name
        :param data_type: Field Type
        :param data_default: Default value or None
        :param data_options: Used for option sets, an Options object
        :param on_verify: Callback function
        :param text: Optional text definition
        :return: None
        """
        if not self.exists(name):
            self._text[name] = text
            self._data[name] = None
            self._def[name] = data_default
            self._dictionary[name] = data_type
            self._callbacks[name] = on_verify
            self._options[name] = data_options

    def on_save(self, name: str, callback: Callable) -> None:
        """
        Assigns a callback to a parameter name
        :param name: Parameter Name
        :param callback: Callback
        :return: None
        """
        self._on_save[name] = callback

    def save_str(self, name: str, data: str) -> None:
        """
        Saves a parameter from a given value
        :param name: Parameter Name
        :param data: Parameter String data
        :return: None
        """
        if not self.exists(name):
            raise Exception(f"Invalid parameter {name}.")
        #
        if self.type(name) == int:
            self.save(name, int(data))
        elif self.type(name) == float:
            self.save(name, float(data))
        elif self.type(name) == str:
            self.save(name, str(data))
        elif self.type(name) == pydggrid.Objects.Options:
            self.save(name, self._options[name].code(data))
        else:
            raise Exception(f"Invalid parameter type for {name}.")

    def save(self, name: str, data: [Any]) -> None:
        """
        Saves a value to the attributes set
        :param name: Name string
        :param data: Data value
        :return: None
        """
        if not self.exists(name):
            raise Exception(f"Invalid parameter {name}.")
        if not isinstance(data, self.type(name)) and self.type(name) != pydggrid.Objects.Options:
            raise Exception(f"Invalid parameter type {name}")
        if isinstance(data, OptionsObject):
            option_records: OptionsObject = self._options[name]
            if not option_records.exists(data):
                raise Exception(f"Invalid parameter option for {name}")
        if self._callbacks[name] is not None:
            if self._callbacks[name](data) is False:
                raise Exception(f"Invalid parameter value, failed check {name}")
        self._data[name] = data
        if name in self._on_save:
            self._on_save[name]()

    def names(self) -> List[str]:
        """
        Returns an array of parameter names
        :return: Parameter names array
        """
        return list(self._data.keys())

    def text(self, name: str) -> [str, None]:
        """
        Returns text value of a string or None if it doesnt exist
        :param name: Parameter Name
        :return: Parameter Text String
        """
        return None if not self.exists(name) \
            else "" \
            if self._text[name] is None else self._text[name]

    def string(self) -> str:
        """
        Returns meta string
        :return:
        """
        elements: List[str] = list([])
        parameters: List[str] = self.names()
        dictionary: Dict = self.dict()
        for parameter in parameters:
            if self.modified(parameter) is False:
                continue
            elements.append(f"{parameter}={dictionary[parameter]}")
        return os.linesep.join(elements)

    def __str__(self) -> str:
        """
        Returns a description of the attributes as a string
        :return: Attribute description
        """
        string_array: List[str] = list()
        parameters: List[str] = self.names()
        base_module: Any = importlib.import_module("pydggrid.Types")
        #
        for parameter in parameters:
            if self.modified(parameter) is False:
                continue
            type_string: str = str(self.type(parameter))
            text_string: str = str(self.text(parameter))
            type_string = type_string.replace("<class '", "").replace("'>", "")
            #
            string_array.append(f"{parameter} ({type_string}):")
            string_array.append(f"\tType: {type_string}")
            string_array.append(f"\tValue: {self._data[parameter]}")
            string_array.append(f"\tDefault: {self._def[parameter]}")
            if len(text_string) > 0:
                string_array.append(f"\tDescription: {text_string}")
            #
            if self._callbacks[parameter] is not None:
                function_string: str = inspect.getsource(self._callbacks[parameter])
                function_string = function_string.replace("on_verify=lambda value: ", "").strip()
                string_array.append(f"\tCallback: {function_string}")
            #
            if self.type(parameter) == pydggrid.Objects.Options:
                type_name = str(self._options[parameter].type()).replace("<enum '", "").replace("'>", "")
                object_map: Dict[str, int] = getattr(base_module, type_name).map()
                string_array.append(f"\tOption Type: {type_name}")
                string_array.append(f"\tOptions:")
                [string_array.append(f"\t\t{object_map[n]}: {n}") for n in object_map]
            #
            string_array.append("")

        return "\n".join(string_array)

    def __bytes__(self) -> bytes:
        """
        Returns meta data as a byte array
        :return: Metadata Array
        """
        elements: List[bytes] = list([])
        parameters: List[str] = self.names()
        for parameter in parameters:
            if self.modified(parameter) is True:
                elements.append(parameter.encode())
                elements.append(self.to_bytes(parameter))
        return b''.join(elements)

    def dict(self) -> Dict[str, str]:
        """
        Returns the parameters as a {str, str} dictionary
        :return: [Str, Str] Dictionary
        """
        parameters: List[str] = self.names()
        dictionary: Dict[str, str] = dict({})
        for parameter in parameters:
            if self.modified(parameter):
                parameter_value: str =  self.get(parameter).__str__() \
                        if self.type(parameter) != pydggrid.Objects.Options else \
                        str(self.get(parameter).__str__()).split(".")[-1]
                parameter_value = parameter_value.lower() if self.type(parameter) == bool else parameter_value
                dictionary[parameter] = parameter_value
        return dictionary

    def print(self, show_empty: bool = True) -> None:
        """
        Prints the attribute set
        :param show_empty If enabled unset variables will be printed
        :return: None
        """
        print(self.__str__())

    def exists(self, name: str) -> bool:
        """
        Returns true if the name is a parameter false otherwise
        :param name: Parameter Name
        :return: True if parameter exists
        """
        return False if name not in self._dictionary else True

    def modified(self, name: str) -> bool:
        """
        Returns true if the value has been modified
        :param name: Parameter Name
        :return: True if modified
        """
        if self.exists(name):
            return True if self._data[name] is not None else False
        return False

    def get(self, name: str) -> Any:
        """
        Returns data as blind variable
        :param name: Parameter name
        :return: Parameter Data
        """
        if not self.exists(name):
            return None
        return self._def[name] if self._data[name] is None else self._data[name]

    def as_string(self, name: str) -> str:
        """
        Returns the requested parameter as string
        :param name: Parameter Name
        :return: Parameter value as string
        """
        return str(self.get(name)) if self.exists(name) else ""

    def as_int(self, name: str) -> int:
        """
        Returns parameter as an integer or 0 if invalid
        :param name: Parameter Name
        :return: Parameter value as integer
        """
        if isinstance(self.type(name), int):
            return int(self.get(name))
        try:
            return int(self.get(name))
        except ValueError:
            return 0

    def as_float(self, name: str) -> float:
        """
        Returns parameter as a float or epsilon if invalid
        :param name: Parameter Name
        :return: Parameter value as float
        """
        if isinstance(self.type(name), float):
            return float(self.get(name))
        try:
            return float(self.get(name))
        except ValueError:
            return sys.float_info.epsilon

    def set_default(self, name: str) -> None:
        """
        Sets a given variable to its default value and marks it as modified
        :param name: Parameter Name
        :return: None
        """
        return self.save(name, self._def[name])

    def to_bytes(self, name: str) -> bytes:
        """
        Converts the given attribute to byte array
        :param name: Parameter Name
        :return: Parameter bytes
        """
        if self.type(name) == int:
            return self.as_int(name).to_bytes(4, "little")
        elif self.type(name) == float:
            return struct.pack("f", self.as_float(name))
        elif self.type(name) == str:
            return self.as_string(name).encode()
        elif self.type(name) == bool:
            return self.as_int(name).to_bytes(4, "little")
        elif self.type(name) == pydggrid.Objects.Options:
            return self.as_int(name).to_bytes(4, "little")
        else:
            raise AttributeError(f"Unrecognized parameter type {name} which is {self.type(name)}")

    def load(self, source: [str, pathlib.Path, Dict[str, str]]) -> None:
        """
        Loads meta-data from string or provided path
        :param source: Source data
            - a pathlib.Path object
            - a string that contains meta-data
            - a path string that points to a meta-data file
        :return: None
        """
        if isinstance(source, pathlib.Path):
            file = open(source.absolute(), "rt")
            meta_string: str = "\n".join(file.readlines())
            file.close()
            return self.load(meta_string)
        elif isinstance(source, dict):
            elements: List[str] = [f"{k} {v}" for k, v in source]
            return self.load("\n".join(elements))
        elif isinstance(source, str):
            if "\n" not in source:
                if os.path.isfile(source):
                    return self.load(pathlib.Path(source))
            lines: List[str] = source.split("\n")
            for line in lines:
                line_t: str = line.strip()
                if line_t.startswith("#"):
                    continue
                elif line_t.startswith("/"):
                    continue
                elif len(line_t.strip()) == 0:
                    continue
                else:
                    name, value = tuple(line.strip().split(" "))
                    if self.exists(name):
                        self.save_str(name, value)
