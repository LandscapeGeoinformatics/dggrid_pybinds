import sys
from abc import ABC, abstractmethod

import geopandas
import pandas

from pydggrid.Types import ReadMode


class Template(ABC):

    def __init__(self):
        pass

    def read(self, byte_data: bytes, read_mode: [ReadMode, int]) -> None:
        """
        Reads data from a bytes query array
        :param byte_data: Byte Data
        :param read_mode: Query Read Mode
        :return: None
        """
        self.un_static()
        mode: ReadMode = ReadMode(int(read_mode))
        if mode == ReadMode.AIGEN:
            print(byte_data)
            sys.exit(0)

    @abstractmethod
    def get_frame(self) -> pandas.DataFrame:
        """
        Returns the record as a data frame
        :return: Pandas DataFrame
        """
        pass

    @abstractmethod
    def get_geoframe(self) -> geopandas.GeoDataFrame:
        """
        Returns the record as a geo data frame
        :return: Geo Pandas Data Frame
        """
        pass

    @abstractmethod
    def get_text(self) -> str:
        """
        Returns the record as a string
        :return: Record String
        """
        pass

    @abstractmethod
    def get_numpy(self) -> str:
        """
        Returns the record as a numpy ndarray
        :return: Numpy ND Array
        """
        pass

    def un_static(self) -> None:
        """
        Un Statics a method
        :return: None
        """
        pass
