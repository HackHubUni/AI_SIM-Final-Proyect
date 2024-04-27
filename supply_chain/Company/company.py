import copy

try:
    from supply_chain.agents.order import Order
    from supply_chain.sim_environment import SimEnvironment

    from supply_chain.Company.registrers.registers import *
    from supply_chain.company import Company, TypeCompany
except:

    from agent import Agent
    from products.product import Product


class CompanyWrapped(Company):

    def __init__(self, name: str, environment: SimEnvironment, agent: Agent, env: SimEnvironment,
                 inicial_balance: float):
        super().__init__(name, environment)
        self.agent: Agent = agent
        self.environment: SimEnvironment = env
        self.balance = inicial_balance
        self.register = Registry()

        self.start()
        """
        Call the start function
        """

    # TODO:Carla aca tienes el ambiente
    @property
    def get_environment(self):
        """
        :return: El env de la simulación
        """
        return self.environment

    # TODO:Carla aca tienes como saber el tiempo actual
    @property
    def get_time(self):
        """
        Retorna el tiempo actual en que se está
        :return:
        """
        return self.environment.get_time()

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

    def __init__(self, name: str, environment: SimEnvironment, agent: Agent, env: SimEnvironment,
                 initial_balance: float, lis_sales_products_name: list[str]):
        super().__init__(name, environment, agent, env, initial_balance)
        self._stock: dict[str, list[Product]] = {}
        # Por cada producto tengo la lista de las instancias de estos

        self._product_price: dict[str, float] = {}
        """
        nombre del producto: precio
        """
        self.lis_sales_products_name: list[str]

    def _restock(self):

        """
        Reabastecimiento mágico que va a tener ,a empresa
        """


    def start(self):
        self._restock()

    # TODO:Carla aca tienes para saber cual es el stock de productos osea nombre_producto:cant
    @property
    def get_stock(self) -> dict[str, int]:
        """
         nombre de producto: lista de los productos en stock son instancias de Product
        :return:
        """
        dic = {}
        for key in self._stock.keys():
            dic[key] = len(self._stock[key])

        return dic

    @property
    def tag(self):
        return TypeCompany.BaseProducer

    def restock(self):
        """
        Se llama a esta función para reabastecerse de productos bajo cierta lógica
        :return:
        """
        pass

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

    # TODO:Carla aca tienes para conocer el precio de un producto
    def get_product_price(self, product_name: str) -> float:
        """
        Retorna por cada producto el precio de estos
        :param product_name: nombre del producto
        :return:float precio de venta del producto
        """
        if product_name not in self._stock:
            return float('inf')
        return self._product_price[product_name]

    def _delete_product_stock(self, product_name: str, count: int) -> list[Product]:
        """
        Es para tener la logica de como  se quita producto del stock en una cant dada
        :param product_name:
        :param count:
        :return: lista de productos a devolver para la venta
        """
        if product_name not in self._stock:
            raise Exception(f"The product {product_name} in the company {self.name} type {self.tag} don´t exists")

        # Chequear que la cant de producto que se tiene en stock es suficiente
        count_in_stock: int = self.get_stock[product_name]
        if count_in_stock < count:
            raise Exception(
                f"Don t have {count} of the product {product_name} only have {count_in_stock} in the company {self.name} type {self.tag}")
        lis = self._stock[product_name]
        temp = copy.deepcopy(lis)
        # elimina los n primeros elementos de la lista
        self._stock[product_name] = lis[count:]

        return temp[0:count]

    # TODO:Carla aca tienes para Si no vas a vender mandas como que es infinito el precio de venta

    def sell(self, product_name: str,
             price_sold: float,
             amount_asked: int,
             amount_sold: int,
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
        self._delete_product_stock(product_name, amount_sold)

    def deliver(self, order: Order):
        pass


class SecondaryCompany(BaseProducer):

    @property
    def tag(self):
        return TypeCompany.SecondaryProvider

    def __init__(self, name: str, environment: SimEnvironment, agent: Agent, env: SimEnvironment):
        super().__init__(name, environment, agent, env)

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

    def __init__(self, name: str, environment: SimEnvironment, agent: Agent, env: SimEnvironment,
                 inicial_balance: float):
        super().__init__(name, environment)
        self.agent: Agent = agent
        self.environment: SimEnvironment = env
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
