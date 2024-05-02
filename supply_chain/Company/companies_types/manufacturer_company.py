from typing import Callable

from supply_chain.Company.orders.Sell_order import ProduceOrder
from supply_chain.Company.stock_manager.manufacturing_stock_manager import ManufacturingStock

from supply_chain.products.ingredient import Ingredient
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




class ManufacturerCompany(ProducerCompany):

    @property
    def tag(self):
        return TypeCompany.SecondaryProvider

    def __init__(self,
                 name: str,
                 get_time: Callable[[], int],
                 add_event: Callable[[SimEvent], None],
                 stock_manager: ManufacturingStock
                 ):
        super().__init__(name,
                         get_time,
                         add_event,
                         stock_manager

                         )
        self.stock_manager: ManufacturingStock = stock_manager

    # TODO:Carla aca tienes el dic de producto con el precio que se procesan porfa
    @property
    def process_products_price(self) -> dict[str, float]:
        """
        Devuelve el diccionario que tiene por producto que se procesa su precio de venta por procesar
        :return:
        """
        return self.stock_manager.price_produce_product_per_unit

    @property
    def get_produce_products(self) -> list[str]:
        """
        Devuelve la lista de productos finales que puede
        dado sus ingredientes procesar esta empresa
        :return:
        """
        return list(self.process_products_price.keys())

    # TODO:Aca tienes  el precio de procesar un elemento
    def get_price_process_product(self, product_name: str):
        """
        Devuelve el precio del producto
        :param product_name:
        :return:
        """
        try:
            return self.stock_manager.get_product_price_per_unit(product_name)
        except Exception as e:
            raise Exception(f"En la empresa {self.name} se tiene el error {str(e)}")

    # TODO:Carla aca es para que llames cuando se vende un servicio de manufactura osea que
    # le di las papas y le empresa me hizo el puré

    def get_product_ingredients(self, product_name: str) -> list[Ingredient]:
        """
        Dado el nombre de un producto el cual dado sus ingredientes se brinda
        el servicio de procesar hasta este producto, devuelve los ingredientes
        :param product_name:
        :return:
        """
        return self.stock_manager.get_product_ingredients(product_name)

    def sell_process_product(self, produce_order: ProduceOrder):
        """
        Registra la venta de un producto procesado: Osea que la empresa matriz le da los ingredientes y la manufaturera
        elabora otro producto con esta
        :param produce_order:
        :return:
        """
        # TODO:AÑAdir estadísticas
        # TODO: Enviar evento
        products = self.stock_manager.process_a_list_of_new_products_from_his_ingredients(produce_order.product_name,
                                                                                          produce_order.ingredients,
                                                                                          produce_order.amount_sold)

        # Se guarda a la bolsa de ordenes para recoger de esa compañia matriz
        self._create_order_to_delivery(matrix_name=produce_order.matrix_name,
                                       product_name=produce_order.product_name,
                                       products=products)





