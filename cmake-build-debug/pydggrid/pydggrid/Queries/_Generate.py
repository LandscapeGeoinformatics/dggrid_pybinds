import sys
from typing import Any, List, Dict

import libpydggrid

from pydggrid.Input import Auto, InputTemplate, Sequence, ShapeFile, Array
from pydggrid.Objects import Collection
from pydggrid.Types import Operation, ClipType, ReadMode
from pydggrid.Queries._Custom import Query as BaseQuery


class Query(BaseQuery):
    """
    Base Generate Grid Query
    - clip: clip settings configured with set_clip, by default set to WHOLE_EARTH, AKA. "Auto()"
    - cells: Cells response from DGGRID
    - points: Points response from DGGRID
    - Meta: Query meta-data object
    """

    def __init__(self):
        """
        Default constructor
        """
        super().__init__(Operation.GENERATE_GRID)
        self.clip: InputTemplate = Auto()
        self.cells: Collection = Collection()
        self.points: Collection = Collection()
        self.set_clip(ClipType.WHOLE_EARTH)
        # Set defaults
        self.Meta.set_default("clip_cell_densification")
        self.Meta.set_default("clipper_scale_factor")
        self.Meta.set_default("clip_using_holes")
        self.Meta.set_default("clip_cell_res")

    def __bytes__(self) -> bytes:
        """
        Returns query bytes
        :return: Clip Bytes
        """
        return self.clip.records.__bytes__()

    def set_points(self):
        pass

    def set_clip(self,
                 clip_type: [ClipType, int, None] = None,
                 data: [Any, None] = None,
                 columns: [List[Any], None] = None) -> None:
        """
        Sets the query clip
        :param clip_type: ClipType definition from pydggrid.Types
        :param data: Data to use with the clipping this is optional and can be set after the clip type has been
            configured
        :param columns: Used to send column information with the clip options, this field is optional but allows you to
            customize the order and index of columns to choose from using pandas dataframes, numpy ndarray objects and
            dictionaries.
        :return: None
        """
        if clip_type is not None:
            type_t: ClipType = ClipType(clip_type)
            if type_t == ClipType.WHOLE_EARTH:
                self.clip = Auto()
            elif type_t == ClipType.SEQNUMS:
                self.clip = Sequence()
            elif type_t == ClipType.SHAPEFILE:
                self.clip = ShapeFile()
            elif type_t == ClipType.INPUT_ADDRESS_TYPE:
                self.clip = Array()
            else:
                raise AttributeError(f"Requested clip type({clip_type}) is not supported")
        self.Meta.save("clip_subset_type", clip_type)
        return self.clip.save(data, columns) if data is not None else None

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadPayload(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        return libpydggrid.UnitTest_ReadPayload(self.Meta.dict(), self.clip.__bytes__())

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytearray = bytearray(self.clip.__bytes__())
        return libpydggrid.UnitTest_ReadQuery(dictionary, list(payload))

    # Override
    # noinspection PyPep8Naming
    def UnitTest_RunQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        dictionary: Dict[str, str] = self.Meta.dict()
        payload: bytearray = bytearray(self.clip.__bytes__())
        return libpydggrid.UnitTest_RunQuery(dictionary, list(payload))

    # Override
    def run(self, byte_data: [bytes, None] = None) -> None:
        """
        Runs the query
        :param byte_data byte payload, if left blank Input.__bytes__() will be used
        :return: None
        """
        byte_data: Dict[str, bytes] = super().exec(self.clip.__bytes__())
        self.cells.save(byte_data["cells"], ReadMode(self.Meta.as_int("cell_output_type")))
        self.points.save(byte_data["points"], ReadMode(self.Meta.as_int("point_output_type")))
