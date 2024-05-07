import os
from typing import Any

from pydggrid.Input._Template import Template as InputTemplate


class Input(InputTemplate):

    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    # Override
    def save(self, data: Any, column: Any = None) -> None:
        """
        Saves data into the input object
        :param data: Data to save
        :param column: Column information determined by input type
        :return: None
        """
        pass

    # Override
    def copy(self, source_object: Any) -> None:
        """
        Copies the source object to local
        :return:
        """
        pass

    # Override
    def __str__(self) -> str:
        """
        __str__ override
        :return: Item description
        """
        return f"RECORDS:{os.linesep}\tNONE{os.linesep}"
