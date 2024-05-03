from typing import Callable

from supply_chain.Company.stock_manager.warehouse_stock_manager import WarehouseStockManager

from supply_chain.sim_event import SimEvent

try:
    from supply_chain.agents.old.order import Order
    from supply_chain.sim_environment import SimEnvironment
    from supply_chain.products.product import Product
    from supply_chain.Company.registrers.registers import *
    from supply_chain.company import Company, TypeCompany
    from supply_chain.Company.companies_types.Producer_Company import *
except:

    pass

class WarehouseCompany(CompanyWrapped):

    def __init__(self,
                 name: str,
                 get_time: Callable[[], int],
                 add_event: Callable[[SimEvent], None],
                 stock_manager: WarehouseStockManager, ):
        super().__init__(name, get_time, add_event, stock_manager)
        self.register = Registry()

    @property
    def tag(self):
        return TypeCompany.Warehouse

    def stock(self):
        pass

    def is_in_storage_product(self, product_name:str):
        """

        :param order:
        :return:
        """
        return self.stock_manager.

    # TODO: Crear el send recibe un Order
    def out_storage_product(self, order: Order):
        """
        Cuando se saca un producto del almacén
        :return:
        """
