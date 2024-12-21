import os
from abc import ABC, abstractmethod
from typing import Any

from pydggrid.Input import InputTemplate


class Template(ABC):

    def __init__(self):
        """
        Default constructor
        """
        self._input: [InputTemplate, None] = None

    def get(self) -> InputTemplate:
        """
        Returns the input template object
        :return: Input template Object
        """
        return self._input

    @abstractmethod
    def save(self, data: Any, column: Any = None) -> None:
        """
        Saves data into the input object
        :param data: Data to save
        :param column: Column information determined by input type
        :return: None
        """
        pass

    def __str__(self) -> str:
        """
        Returns default description of the object
        :return: Description String
        """
        return "\t" + f"{os.linesep}\t".join(self._input.__str__().split(os.linesep))
