import os
import pathlib
from typing import Any

from pydggrid.Input._Template import Template as InputTemplate
from pydggrid.Interfaces import Dataset


class Input(Dataset):

    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    # Override
    def __str__(self) -> str:
        """
        __str__ override
        :return: Item description
        """
        return f"RECORDS:{os.linesep}\tNONE{os.linesep}"
