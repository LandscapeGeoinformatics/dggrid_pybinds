import sys
from abc import abstractmethod
from typing import List, Dict

import libpydggrid

from pydggrid.Types import Operation, ClipType, InputAddress

from pydggrid.Queries._Template import Template as QueryTemplate
from pydggrid.Input import Template as InputTemplate, Auto


class Query(QueryTemplate):

    def __init__(self,
                 operation: Operation = Operation.CUSTOM,
                 input_object: [InputTemplate, None] = None) -> None:
        """
        Default constructor
        :param operation Operation definition
        :param input_object default input object
        """
        super().__init__(operation, input_object)

    # Override
    def __bytes__(self) -> bytes:
        """
        Returns query bytes
        :return: Query Byte Array
        """
        elements: List[bytes] = list([])
        elements.append(super().__bytes__())
        return b''.join(elements)

    # Override
    def __str__(self) -> str:
        """
        Describes the query
        :return: Query Description
        """
        return super().__str__()

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadPayload(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        return super().UnitTest_ReadPayload()

    # Override
    # noinspection PyPep8Naming
    def UnitTest_ReadQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        return super().UnitTest_ReadQuery()

    # Override
    # noinspection PyPep8Naming
    def UnitTest_RunQuery(self) -> str:
        """
        Runs a unit test to pybinds11 layer
        :return: Test response string
        """
        return super().UnitTest_RunQuery()

    @abstractmethod
    def run(self) -> None:
        """
        Runs the query
        :return: None
        """
        raise NotImplementedError("run() must be implemented for individual query types.")


