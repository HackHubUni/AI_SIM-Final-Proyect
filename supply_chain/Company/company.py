import copy
from typing import Callable

from supply_chain.Company.company_helper import CompanyStockBase, BaseCompanyStock

try:
    from supply_chain.agents.order import Order
    from supply_chain.sim_environment import SimEnvironment

    from supply_chain.Company.registrers.registers import *
    from supply_chain.company import Company, TypeCompany
except:

    from agent import Agent
    from products.product import Product


class CompanyWrapped(Company):

    def __init__(self, name: str, get_time: Callable[[], int], agent: Agent, stock_manager: CompanyStockBase
                 ):
        super().__init__(name, get_time)
        self.agent: Agent = agent
        self.register = Registry()
        self.stock_manager = stock_manager

        self.start()
        """
        Call the start function
        """

    # TODO:Carla aca tienes como saber el tiempo actual
    @property
    def get_time(self):
        """
        Retorna el tiempo actual en que se está
        :return:
        """
        return self.get_time()

    def start(self):
        pass


class LogisticCompany(CompanyWrapped):
    """
    Class for the logistic Company
    """

    @property
    def tag(self):
        return TypeCompany.Logistic


class BaseProducer(CompanyWrapped):
    """Productor de productos base"""

    def __init__(self, name: str, get_time: Callable[[], int], agent: Agent, stock_manager: BaseCompanyStock):
        super().__init__(name, get_time, agent, stock_manager)
        self.stock_manager = stock_manager

    def start(self):
        """
        Inicializa la clase
        :return:
        """
        self.stock_manager.restock()

    # TODO:Carla aca tienes para saber cual es el stock de productos osea nombre_producto:cant

    @property
    def tag(self):
        return TypeCompany.BaseProducer

    def _add_sell_record(self,
                         product_name: str,
                         list_products_records: list[ProductRecords],
                         normal_price: float,
                         price_sold: float,
                         amount_asked: int,
                         amount_sold: int,
                         matrix_name: str,
                         from_company_name: str,
                         from_company_tag: TypeCompany,
                         to_company_name: str,
                         to_company_tag: TypeCompany
                         ):
        self.register.add_sell_record(
            # Tiempo en que se hace la venta
            time=self.get_time,
            product_name=product_name,
            list_products_records=list_products_records,
            normal_price=normal_price,
            price_sold=price_sold,
            amount_asked=amount_asked,
            amount_sold=amount_sold,
            matrix_name=matrix_name,
            from_company_name=from_company_name,
            from_company_tag=from_company_tag,
            to_company_name=to_company_name,
            to_company_tag=to_company_tag
        )

    def sell(self, product_name: str,
             price_sold: float,
             amount_asked: int,
             amount_sold: int,
             normal_price_per_unit:float,
             matrix_name: str,
             to_company: Company,
             logistic_company: LogisticCompany
             ):
        """
        Llamar para realizar la venta del producto
        :param product_name:str nombre del producto a vender
        :param price_sold:float precio de venta del lote de productos
        :param amount_asked:int cantidad que pidió comprar
        :param amount_sold:int cantidad que se le vendió
        :param matrix_name:str nombre de la empresa matriz que gestionó la compra
        :param to_company:Company compañía a la que hay que enviarle
        :param logistic_company:LogisticCompany company logística  que debe realizar el envío
        :return:
        """
        count_in_stock: int = self.stock_manager.get_count_product_in_stock(product_name)

        assert amount_sold <= count_in_stock,f"Se trata de vender {amount_sold} unidades del producto {product_name} cuando hay stock {count_in_stock} en la empresa {self.name} "
        # Se verifica que nunca se venda una cant que no hay en el stock
        amount_sold = amount_sold if amount_sold <= count_in_stock else count_in_stock
        #Actualizar estadísticas

        self.register.add_sell_record(time=self.get_time,
                                      product_name=product_name,
                                      price_sold=price_sold,
                                      matrix_name=matrix_name,
                                      amount_asked=amount_asked,
                                      from_company_name=self.name,
                                      from_company_tag=self.tag,
                                      to_company_name=to_company.name,
                                      to_company_tag=to_company.tag,
                                      normal_price=normal_price_per_unit,
                                      amount_sold=amount_sold,
                                      list_products_records=



                                      )


        return_list=self.stock_manager.get_products_by_name(product_name,amount_sold)

    def deliver(self, order: Order):
        pass


class SecondaryCompany(BaseProducer):

    @property
    def tag(self):
        return TypeCompany.SecondaryProvider

    def __init__(self, name: str, get_time: Callable[[], int], agent: Agent,stock_manager:):
        super().__init__(name, get_time, agent)

        self._process_product_price: dict[Product, float] = {}

    # TODO:Carla aca tienes el dic de producto con el precio que se procesan porfa
    @property
    def process_products_price(self) -> dict[Product, float]:
        """
        Devuelve el diccionario que tiene por producto que se procesa su precio de venta por procesar
        :return:
        """
        return self._process_product_price

    # TODO:Aca tienes  el precio de procesar un elemento
    def get_price_process_product(self, product: Product):
        """
        Devuelve el precio del producto
        :param product:
        :return:
        """
        if not product in self._process_product_price:
            raise Exception(f"El producto: {product.name} no se encuentra entre los productos a procesar")
        return self._process_product_price[product]

    # TODO:Carla aca es para que llames cuando se vende un servicio de manufactura osea que
    # le di las papas y le empresa me hizo el puré
    def sell_process_product(self, order: Order, sell_price: float):
        """
        Registra la venta de un producto procesado: Osea que la empresa matriz le da los ingredientes y la manufaturera
        elabora otro producto con esta
        :param order: orden del producto
        :param sell_price: precio al que se vendió el total de la orden
        :return:
        """
        pass

    def restock(self):
        """
        LLama a reabastecer un producto y una cantidad en específico
        :param product:
        :param count:
        :return:
        """
        # Todo:Implementar restock este es el que llama carla pq tiene que hacer restock no es el que tengo que hacer para que sea magicamente
        pass


class WarehouseCompany(CompanyWrapped):

    def __init__(self, name: str, get_time: Callable[[], int], agent: Agent,
                 inicial_balance: float):
        super().__init__(name, get_time)
        self.agent: Agent = agent
        self.balance = inicial_balance
        self.register = Registry()

    @property
    def tag(self):
        return TypeCompany.Warehouse

    def stock(self):
        pass

    def in_storage_product(self, order: Order):
        """
        Cuando se entra a guardar un producto
        :param order:
        :return:
        """
        pass

    # TODO: Crear el send recibe un Order
    def out_storage_product(self, order: Order):
        """
        Cuando se saca un producto del almacen
        :return:
        """
