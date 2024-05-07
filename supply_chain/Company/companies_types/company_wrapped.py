from abc import ABC, abstractmethod


from typing import Callable
from supply_chain.Company.registrers.registers__Please_dont_use_that_is_the_old import Registry
from supply_chain.Company.stock_manager.stock_manager import CompanyStockBase
from supply_chain.sim_event import SimEvent
from supply_chain.company import Company, TypeCompany




class CompanyWrapped(Company):

    def __init__(self,
                 name: str,
                 get_time: Callable[[], int],
                 add_event: Callable[[SimEvent], None],
                 stock_manager: CompanyStockBase,

                 ):
        super().__init__(name, get_time, add_event)
        self.register = Registry()
        self.stock_manager = stock_manager

        #self.start()
        """
        Call the start function
        """

    # TODO:Carla aca tienes como saber el tiempo actual
    @property
    def time(self) -> int:
        """
        Retorna el tiempo actual en que se está
        :return:
        """
        return self.get_time()

    @abstractmethod
    def start(self):
        """
        Esta función es para inicializar las acciones de la empresa
        :return:
        """
        pass

    @property
    @abstractmethod
    def tag(self) -> TypeCompany:
        """
        Devuelve el tag del tipo de compañía que es
        :return:
        """
        pass



