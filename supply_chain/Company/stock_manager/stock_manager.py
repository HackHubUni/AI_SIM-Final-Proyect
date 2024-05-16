
from typing import Callable, Dict, List, Any, Tuple
from abc import ABC, abstractmethod, abstractproperty
from supply_chain.sim_event import SimEvent


class BaseCompanyReStockException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class CompanyStockBase(ABC):

    def __init__(self,
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int]
                 ):
        self.add_event: Callable[[SimEvent], None] = add_event
        """
        función que brinda poder añadir un evento al simulador
        """
        self.get_time: Callable[[], int] = get_time
        """
        función que brinda el tiempo actual
        """

    @property
    def time(self) -> int:
        """
        Da el tiempo actual
        :return:
        """
        return self.get_time()

    @abstractmethod
    def restock(self):
        """
        Se reabastece mágicamente la empresa
        :return: el precio de reabastecerse
        """
        pass







