from typing import Callable


from abc import ABC, abstractmethod, abstractproperty
from enum import Enum

from supply_chain.sim_event import SimEvent


class TypeCompany(Enum):
    Matrix = 1
    BaseProducer = 2
    SecondaryProvider = 3
    Logistic = 4
    Warehouse = 5
    Store = 6


class Company(ABC):
    """Base class for all the companies in the supply chain"""

    def __init__(
        self,
        name: str,
        get_time: Callable[[], int],
        add_event: Callable[[SimEvent], None],
    ) -> None:
        super().__init__()
        self.name: str = name
        """The name of the company"""
        self.get_time: Callable = get_time
        """The reference to the environment of the simulation"""
        self.add_event: Callable[[SimEvent], None] = add_event
        """The lambda to add a event to a env """
        self.position_in_map: tuple[float, float] = (0, 0)
        """The position of this company in te map"""

    @property
    @abstractmethod
    def tag(self) -> TypeCompany:
        """
        Devuelve el tag del tipo de compañía que es
        :return:
        """
        pass

    def set_new_position_in_map(self, new_position: tuple[float, float]):
        """This method changes the position of the company in the map for a new value"""
        self.position_in_map = new_position

    def get_position_in_map(self) -> tuple[float, float]:
        """This method returns the position of the company in the map"""
        return self.position_in_map

    @abstractmethod
    def start(self):
        """
        Esta función es para inicializar las acciones de la empresa
        :return:
        """
        pass

    @property

    def time(self) -> int:
        """
        Retorna el tiempo actual en que se está
        :return:
        """
        return self.get_time()


