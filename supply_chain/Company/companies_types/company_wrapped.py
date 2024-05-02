from abc import ABC
from typing import Callable

from supply_chain.Company.stock_manager.stock_manager import CompanyStockBase
from supply_chain.sim_event import SimEvent

try:
    from supply_chain.agents.old.order import Order
    from supply_chain.sim_environment import SimEnvironment
    from supply_chain.products.product import Product
    from supply_chain.Company.registrers.registers import *
    from supply_chain.company import Company, TypeCompany
except:

    pass


class CompanyWrapped(Company, ABC):

    def __init__(self,
                 name: str,
                 get_time: Callable[[], int],
                 add_event: Callable[[SimEvent], None],
                 stock_manager: CompanyStockBase,

                 ):
        super().__init__(name, get_time, add_event)
        self.register = Registry()
        self.stock_manager = stock_manager

        self.start()
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

    def start(self):
        pass



