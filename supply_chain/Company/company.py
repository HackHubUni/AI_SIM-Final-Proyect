import copy
from typing import Callable, List

from supply_chain.Company.Sell_order import SellOrder, ProduceOrder
from supply_chain.Company.delivery_order import DeliveryOrder
from supply_chain.Company.stock_manager import CompanyStockBase, BaseCompanyStock, ManufacturingStock
from supply_chain.products.ingredient import Ingredient
from supply_chain.sim_event import SimEvent

try:
    from supply_chain.agents.order import Order
    from supply_chain.sim_environment import SimEnvironment
    from supply_chain.products.product import Product
    from supply_chain.Company.registrers.registers import *
    from supply_chain.company import Company, TypeCompany
except:

    from agent import Agent
    from products.product import Product


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


class LogisticCompany(CompanyWrapped):
    """
    Class for the logistic Company
    """

    @property
    def tag(self):
        return TypeCompany.Logistic


class BaseProducer(CompanyWrapped):
    """Productor de productos base"""

    def __init__(self,
                 name: str,
                 get_time: Callable[[], int],
                 add_event: Callable[[SimEvent], None],
                 stock_manager: BaseCompanyStock):
        super().__init__(name, get_time, add_event, stock_manager)
        self.stock_manager = stock_manager
        self._orders_to_delivery: dict[str, dict[str, list[Product]]] = {}
        # Empresa matriz : [nombre producto:lista de productos reservados]

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
            time=self.time,
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

    def create_list_ProductRecord(self, list_products: List[Product]) -> list[ProductRecords]:
        """
        Dado una serie de instancias de productos devuelve su product record
        :param list_products: Lista de productos hacer su ProductRecords
        :return:list[ProductRecords]
        """
        list_products_records: List[ProductRecords] = []
        for item in list_products:
            assert isinstance(item, Product), "Item in list_products is not a Product"
            temp = ProductRecords(name=item.name, quality_now=item.get_quality(self.time), )
            list_products_records.append(temp)

        return list_products_records

    def _create_order_to_delivery(self, matrix_name: str, product_name: str, products: list[Product]):
        """
        Se crea un delivery de productos a una empresa matriz
        :param matrix_name:str
        :param product_name:str
        :param products:list[Product]
        :return:
        """
        # Si no esta la empresa matriz ponerle un diccionario
        if not matrix_name in self._orders_to_delivery:
            self._orders_to_delivery[matrix_name] = {}
        # Extraer el diccionario por empresa matriz
        dic_Temp = self._orders_to_delivery[matrix_name]
        # Si no existe ese producto para esa empresa matriz añadir dicha lista
        if not product_name in dic_Temp:
            dic_Temp[product_name] = list(products)
        else:
            # Si ya existen añadirlos al combo
            dic_Temp[product_name] += products

    def sell(self, sellOrder: SellOrder
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
        :return: Lanza un evento
        """

        count_in_stock: int = self.stock_manager.get_count_product_in_stock(sellOrder.product_name)

        assert sellOrder.amount_sold <= count_in_stock, f"Se trata de vender {sellOrder.amount_sold} unidades del producto {product_name} cuando hay stock {count_in_stock} en la empresa {self.name} "
        # Se verifica que nunca se venda una cant que no hay en el stock
        amount_sold = sellOrder.amount_sold if sellOrder.amount_sold <= count_in_stock else count_in_stock

        return_list = self.stock_manager.get_products_by_name(sellOrder.product_name, amount_sold)

        # Actualizar estadísticas

        self.register.add_sell_record(time=self.time,
                                      product_name=sellOrder.product_name,
                                      price_sold=sellOrder.price_sold,
                                      matrix_name=sellOrder.matrix_name,
                                      amount_asked=sellOrder.amount_asked,
                                      from_company_name=self.name,
                                      from_company_tag=self.tag,
                                      to_company_name=sellOrder.to_company.name,
                                      to_company_tag=sellOrder.to_company.tag,
                                      normal_price=sellOrder.normal_price_per_unit,
                                      amount_sold=amount_sold,
                                      list_products_records=self.create_list_ProductRecord(return_list)
                                      )
        #TODO: Leisma aca esta donde se guarda la bolsa para cada proveedor
        #Se guardan los productos en una "bolsa" para cada empresa matriz a esperar a ser enviado
        self._create_order_to_delivery(matrix_name=sellOrder.matrix_name,product_name=sellOrder.product_name,return_list)


    def get_product_price(self, product_name: str) -> float:
        return self.stock_manager.get_product_price_per_unit(product_name)

    def deliver(self,delivery_Order:DeliveryOrder ):
        # TODO:leismael Esto es para hacer el delivery
        pass


class SecondaryCompany(BaseProducer):

    @property
    def tag(self):
        return TypeCompany.SecondaryProvider

    def __init__(self, name: str, get_time: Callable[[], int], agent: Agent, stock_manager: ManufacturingStock):
        super().__init__(name, get_time, agent, stock_manager)
        self.stock_manager = stock_manager

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
        products= self.stock_manager.process_a_list_of_new_products_from_his_ingredients(produce_order.product_name,
                                                                                      produce_order.ingredients,
                                                                                      produce_order.amount_sold)

        #Se guarda a la bolsa de ordenes para recoger de esa compañia matriz
        self._create_order_to_delivery(matrix_name=produce_order.matrix_name,
                                       product_name=produce_order.product_name,
                                       products=products)

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
        Cuando se saca un producto del almacén
        :return:
        """
