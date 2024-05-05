from supply_chain.Company.companies_types.company_wrapped import *
from supply_chain.Company.orders.Sell_order import SellOrder
from supply_chain.Company.registrers.product_history import *
from supply_chain.Company.stock_manager.productor_stock_manager import *
from supply_chain.Company.stock_manager.productor_stock_manager import ProductorCompanyStock
from supply_chain.Mensajes.ask_msg import HacerServicioDeDistribucion
from supply_chain.events.RecibirProductosEvent import SendProductEvent
from supply_chain.sim_event import SimEvent


class ProducerCompany(CompanyWrapped):
    """Productor de productos base"""

    def __init__(self,
                 name: str,
                 get_time: Callable[[], int],
                 add_event: Callable[[SimEvent], None],
                 stock_manager: ProductorCompanyStock):
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

    def get_count_product_in_stock(self, product_name: str):
        """
        Devuelve cuantas unidades tengo en stock
        :param product_name:
        :return:
        """
        return self.stock_manager.get_count_product_in_stock(product_name)

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
            temp = ProductRecords(name=item.name, quality_now=item.get_quality(self.time),
                                  price_produce=self.get_product_price(item.name))
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
        :param sellOrder:
        :return:
        """

        count_in_stock: int = self.stock_manager.get_count_product_in_stock(sellOrder.product_name)

        assert sellOrder.amount_sold <= count_in_stock, f"Se trata de vender {sellOrder.amount_sold} unidades del producto {sellOrder.product_name} cuando hay stock {count_in_stock} en la empresa {self.name} "
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
        # TODO: Leisma aca esta donde se guarda la bolsa para cada proveedor
        # Se guardan los productos en una "bolsa" para cada empresa matriz a esperar a ser enviado
        self._create_order_to_delivery(matrix_name=sellOrder.matrix_name, product_name=sellOrder.product_name,
                                       products=return_list)

    def get_product_price(self, product_name: str) -> float:
        """
        Devuelve el precio por unidad de un producto
        :param product_name:
        :return:
        """
        return self.stock_manager.get_product_price_per_unit(product_name)

    def is_product_in_stock(self, product_name: str) -> bool:
        """
        Retorna True o False en dependencia de si esta o no el producto en stock
        :param product_name:
        :return:
        """

        return self.stock_manager.is_product_in_stock(product_name)

    def deliver(self,comunication:Callable, delivery_Order: HacerServicioDeDistribucion):
        # TODO:REllenar AÑADir estadísticas
        matrix_name = delivery_Order.matrix_name
        if not matrix_name in self._orders_to_delivery:
            raise Exception(f'En la empresa {self.name} no hay ordenees para la compañia {matrix_name}')

        dict_temp = self._orders_to_delivery[matrix_name]

        product_name = delivery_Order.product_name

        if not product_name in dict_temp:
            raise Exception(
                f'En la empresa {self.name} no hay ordenees para la compañia {matrix_name} del producto {product_name}')

        lis = dict_temp[product_name]

        count = delivery_Order.count_move

        len_lis = len(lis)
        if len_lis < count:
            raise Exception(
                f'En la empresa {self.name} no hay ordenees para la compañia {matrix_name} del producto {product_name} en la cant querida {count} sino que hay {len_lis}')
        #Lista de productos a retornar
        list_return=lis[:count]
        #Lista de la nueva bolsa en stock
        list_nueva=lis[count:]
        #Actualizar el diccionario
        dict_temp[product_name]=list_nueva

        #Añadir antes de enviar el evento

        delivery_Order.set_list_product(list_return)

        time_=self.time+delivery_Order.time_demora_logistico
        event=SendProductEvent(time_,
                               1,
                               comunication,
                               delivery_Order)
        self.add_event(event)

    def get_name_products_in_stock_now(self) -> list[str]:
        """Devuelve el nombre de los productos que hay en stock ahora"""

        return self.stock_manager.get_name_products_in_stock_now()
