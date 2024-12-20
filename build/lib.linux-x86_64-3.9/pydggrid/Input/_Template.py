import os
import pathlib
import textwrap
from abc import ABC, abstractmethod
from typing import List, Any, Dict


class Template(ABC):

    def __init__(self):
        """
        Default constructor
        """
        pass

    @abstractmethod
    def save(self, data: Any, columns: [Any, None] = None) -> None:
        """
        Save data override
        :param data: Data Save, defined by input object
        :param columns: Column name defined by input object
        :return: None
        """
        pass

