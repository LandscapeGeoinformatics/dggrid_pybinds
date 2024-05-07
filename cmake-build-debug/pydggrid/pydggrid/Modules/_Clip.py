import os
from typing import Any, List

from pydggrid.Types import ClipType
from pydggrid.Input import InputTemplate, Auto, Sequence
from pydggrid.Modules._Template import Template as ModuleTemplate


class Module(ModuleTemplate):

    def __init__(self, clip_type: [ClipType, int]):
        """
        Default clip constructor
        :param clip_type: ClipType definition
        """
        super().__init__()
        self._type: ClipType = ClipType(clip_type)
        self.set(self._type)

    def type(self) -> ClipType:
        """
        Returns clip type definition
        :return: ClipType Enum
        """
        return self._type

    def set(self, clip_type: [ClipType, InputTemplate]) -> None:
        """
        Sets the clip object
        :param clip_type: ClipType object
        :return: None
        """
        if isinstance(clip_type, ClipType):
            self._type = clip_type
            if self._type == ClipType.WHOLE_EARTH:
                self._input = Auto()
            elif self._type == ClipType.SEQNUMS:
                self._input = Sequence()
            else:
                raise AttributeError("Invalid clip type for query")

    # override
    def save(self, data: Any, column: Any = None) -> None:
        """
        Saves data into the input object
        :param data: Data to save
        :param column: Column information determined by input type
        :return: None
        """
        self._input.save(data, column)

    def __str__(self) -> str:
        """
        Returns default description of the object
        :return: Description String
        """
        elements: List[str] = list([])
        elements.append(f"\tClip Type: {self._type.__str__()}")
        elements.append(super().__str__())
        return os.linesep.join(elements)
