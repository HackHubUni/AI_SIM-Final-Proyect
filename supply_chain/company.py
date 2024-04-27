from typing import Callable

from supply_chain.sim_environment import SimEnvironment
from abc import ABC, abstractmethod, abstractproperty
from enum import Enum


class TypeCompany(Enum):
    Matrix = 1
    BaseProducer = 2
    SecondaryProvider = 3
    Logistic = 4
    Warehouse = 5
    Store = 6


class Company(ABC):
    """Base class for all the companies in the supply chain"""

    def __init__(self, name: str, get_time: Callable[[], int]) -> None:
        super().__init__()
        self.name: str = name
        """The name of the company"""
        self.get_time: Callable = get_time
        """The reference to the environment of the simulation"""
        # TODO: Paco, remember that companies offer services. Think in how to model this

    @property
    @abstractmethod
    def tag(self) -> TypeCompany:
        """
        Devuelve el tag del tipo de compañía que es
        :return:
        """
        pass

    @abstractmethod
    def start(self):
        """
        Esta función es para inicializar las acciones de la empresa
        :return:
        """
        pass
