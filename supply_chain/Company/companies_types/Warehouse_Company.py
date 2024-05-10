from typing import Callable

from supply_chain.Company.stock_manager.warehouse_stock_manager import WarehouseStockManager

from supply_chain.sim_event import SimEvent



from supply_chain.sim_environment import SimEnvironment
from supply_chain.products.product import Product
from supply_chain.Company.registrers.registers__Please_dont_use_that_is_the_old import *
from supply_chain.company import Company, TypeCompany
from supply_chain.Company.companies_types.Producer_Company import *


class WarehouseCompany(CompanyWrapped):

    def __init__(self,
                 name: str,
                 get_time: Callable[[], int],
                 add_event: Callable[[SimEvent], None],
                 stock_manager: WarehouseStockManager,

                 ):
        super().__init__(name, get_time, add_event, stock_manager)
        self.register = Registry()
        self.stock_manager = stock_manager
    def start(self):
        #Inicializar el stock
        self.stock_manager.restock()
       #firts_restock_event= CompanyRestockSimEvent(0,1,self.stock_manager.restock)
       #self.add_event(firts_restock_event)

    @property
    def tag(self):
        return TypeCompany.Warehouse

    def stock(self):

        return self.stock_manager.get_list_products_by_company()

    def get_cost_by_product_and_unit_time(self, product_name: str):
        return self.stock_manager.get_cost_by_product_and_unit_time(product_name)

    def add_product_in_storage(self, product: Product, matrix_name: str):
        self.add_list_product_in_storage([product], matrix_name)

    def add_list_product_in_storage(self, list_product: list[Product], matrix_name: str):
        self.stock_manager.add_products(matrix_name, list_product)

    def get_list_products_by_company(self, matrix_name: str, product_name: str):
        """

        :param matrix_name:
        :param product_name:
        :return:
        """
        return self.stock_manager.get_list_products_by_company(matrix_name, product_name)

    def get_how_can_storage_a_company(self, matrix_name: str, product_name: str):
        """Devuelve cero si no hay en stock"""
        return self.stock_manager.get_how_can_storage_a_company(matrix_name, product_name)
