import enum
from typing import Dict, Any, Type

from pydggrid.Types import TypeDef


class Object:
    """
    Defines option sets for Attributes and other objects
    _type: option type identifier
    _data: Object [name, pointer] pair
    """

    def __init__(self, object_type: Type[TypeDef] = None):
        """
        Default constructor
        :param object_type: Object Type (Enum) definition, can be nulled
        """
        self._type: Type[TypeDef] = object_type
        self._data: Dict[str, int] = {}
        self.read(self._type)

    def define(self, name: str, data: Any = None) -> None:
        """
        Defines an internal option
        :param name: Option String Name
        :param data: Option Data
        :return: None
        """
        self._data[name] = data if data is not None else len(self._data) + 1

    def type(self) -> Any:
        """
        Returns object option type definition
        :return: Object Type Definition
        """
        return self._type

    def exists(self, identifier: [str, int]) -> bool:
        """
        Returns true if the identifier (Name or Integer) exists in the options
        :param identifier: Name or Integer code of option
        :return: True
        """
        if isinstance(identifier, str):
            return identifier in self._data
        if isinstance(identifier, int):
            return identifier in self._data.values()
        return False

    def code(self, name: str) -> [int, None]:
        """
        Returns option code by name
        :param name: Option Name
        :return: Option code or None if it doesnt exist
        """
        return None if not self.exists(name) else self._data[name]

    def name(self, code: int) -> [str, None]:
        """
        Returns option name by option value
        :param code: Option Value Code
        :return: Option Name
        """
        return None if not self.exists(code) else list(self._data.keys())[list(self._data.values()).index(code)]

    def read(self, definition: Type[TypeDef]) -> None:
        """
        Reads a type object and saves it into options memory
        :param definition: Enum object
        :return: None
        """
        if isinstance(definition, enum.EnumMeta):
            self._data.clear()
            self._type = definition
            keys: list = definition.keys()
            values: list = definition.values()
            for index, key in enumerate(keys):
                self.define(key, values[index])
