import os
import pathlib
from typing import Any

from pydggrid.Input._Template import Template as InputTemplate


class Input(InputTemplate):

    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    # Override
    def save(self, data: Any, columns: Any = None) -> None:
        """
        Saves data into the input object
        :param data: Data to save
        :param columns: Column information determined by input type
        :return: None
        """
        raise NotImplementedError("save() is not supported by this input type")

    # Overrid
    def copy(self, source_object: Any) -> None:
        """
        Copies the source object to local
        :param source_object: Source Object should be Template compatible
        :return: None
        """
        return super(Input, self).copy(source_object)

    # Override
    def read(self, source: [str, pathlib.Path]) -> None:
        """
        Reads records into data set, this could be:
            1. String pointing to a valid source path
            2. pathlib.Path object
        :param source: Source Path
        :return: None
        """
        raise NotImplementedError("read() is not supported by this input type")

    # Override
    def __str__(self) -> str:
        """
        __str__ override
        :return: Item description
        """
        return f"RECORDS:{os.linesep}\tNONE{os.linesep}"
