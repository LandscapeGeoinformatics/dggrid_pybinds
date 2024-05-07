import os
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
    def save(self, data: Any, column: [Any, None] = None) -> None:
        """
        Save data override
        :param data: Data Save, defined by input object
        :param column: Column name defined by input object
        :return: None
        """
        pass

    @abstractmethod
    def copy(self, source_object: Any) -> None:
        """
        Copies the source object to local
        :return:
        """
        if isinstance(source_object, Template):
            self.records.clear()
            self.records.copy(source_object.records)

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
