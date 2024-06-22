import os
import pathlib
import textwrap
from abc import ABC, abstractmethod
from typing import List, Any, Dict

from pydggrid.Objects import Records


class Template(ABC):

    def __init__(self):
        """
        Default constructor
        """
        self.records: Records = Records()

    @abstractmethod
    def save(self, data: Any, columns: [Any, None] = None) -> None:
        """
        Save data override
        :param data: Data Save, defined by input object
        :param columns: Column name defined by input object
        :return: None
        """
        pass

    @abstractmethod
    def copy(self, source_object: Any) -> None:
        """
        Copies the source object to local
        :param source_object: Source Object should be Template compatible
        :return: None
        """
        if isinstance(source_object, Template):
            self.records.clear()
            self.records.copy(source_object.records)

    @abstractmethod
    def read(self, source: [str, pathlib.Path]) -> None:
        """
        Reads records into data set, this could be:
            1. String pointing to a valid source path
            2. pathlib.Path object
        :param source: Source Path
        :return: None
        """
        pass

    # override
    def __bytes__(self) -> bytes:
        """
        Returns input data bytes
        :return: Data Bytes
        """
        return self.records.__bytes__()

    # override
    def __str__(self) -> str:
        """
        __str__ override
        :return: Item description
        """
        elements: List[str] = list([])
        elements.append("")
        elements.append("RECORDS:")
        elements.append("\t" + f"{os.linesep}\t".join(self.records.__str__().split(os.linesep)))
        elements.append("")
        elements.append("BYTES:")
        elements.append("\t" + f"{os.linesep}\t".join(textwrap.wrap(self.records.__bytes__().hex(), 64)))
        return os.linesep.join(elements)
