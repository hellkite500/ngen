from abc import ABC, abstractmethod
from typing import List
from configurations import Formulation, Forcing, Time, Routing

class Realization():
    """_summary_

    """

    def __init__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        pass

    @property
    def formulations(self) -> List(Formulation):
        """_summary_

        Returns:
            dict: _description_
        """
        return self._formulations

    @property
    def forcing(self) -> Forcing:
        """_summary_

        Returns:
            dict: _description_
        """
        return self._forcing
    
    @property
    def time(self) -> Time:
        """_summary_

        Returns:
            dict: _description_
        """
        return self._time

    @property
    def routing(self) -> Routing:
        """_summary_

        Returns:
            dict: _description_
        """
        return self._routing


class NgenRealization(ABC):

    @property
    @abstractmethod
    def global_config(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        pass

    @property
    @abstractmethod
    def catchments(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        pass