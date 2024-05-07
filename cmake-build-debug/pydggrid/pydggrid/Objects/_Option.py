from typing import List, Any, Dict


class Object:
    """
    Allows for primitive type choice options
    """

    def __init__(self, options: List[Any]):
        """
        Default constructor
        :param options: Option types
        """
        self._options = options

    def is_option(self, option_data: Any) -> bool:
        """
        Returns true if the given option exists in choice list
        :param option_data: Option Data
        :return: True if option exists
        """
        return option_data in self._options
