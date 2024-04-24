try:
    from supply_chain.agents.order import Order
    from supply_chain.sim_environment import SimEnvironment

    from supply_chain.Company.registrers.registers import *
    from supply_chain.company_protocol import Company, TypeCompany
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

   #TODO:Carla aca tienes el ambiente
    @property
    def get_environment(self):
        """
        :return: El env de la simulación
        """
        return self.environment

   #TODO:Carla aca tienes como saber el tiempo actual
    @property
    def get_time(self):
        """
        Retorna el tiempo actual en que se está
        :return:
        """
        return self.environment.get_time()


class BaseProducer(CompanyWrapped):
    """Productor de productos base"""
    def __init__(self, name: str, environment: SimEnvironment, agent: Agent, env: SimEnvironment,
                 initial_balance: float):
        super().__init__(name, environment, agent, env, initial_balance)

        self._stock: dict[Product, int] = {}
        self._product_price: dict[Product, float] = {}

        # TODO: Tengo que añadir la funcion de dar el precio

    #TODO:Carla aca tienes para saber cual es el stock de productos osea producto:cant
    @property
    def get_stock(self):
        return self._stock

    @property
    def tag(self):
        return TypeCompany.BaseProducer


    def restock(self):
        """
        Se llama a esta función para reabastecerse de productos bajo cierta lógica
        :return:
        """
        pass



    def _add_sell_record(self, time: int, amount_asked: int, amount_sold: int):
        self.register.add_sell_record(time, amount_asked, amount_sold)

    def _add_stock_record(self, time: int, amount: int):
        self.register.add_stock_record(time, amount)

    #TODO:Carla aca tienes para conocer el precio de un producto
    def get_product_price(self, product: Product) -> float:
        """
        Retorna por cada producto el precio de estos
        :param product:
        :return:
        """
        if product not in self._stock:
            return float('inf')
        return self._product_price[product]

    #TODO:Carla aca tienes para Si no vas a vender mandas como que es infinito el precio de venta
    def sell(self, order:Order, gain_money: float):
        """
            Refleja la venta de un producto
        :param count_:
        :param product:
        :param gain_money:
        :return:
        """
        count_: int=order.quantity
        product: Product=order.product
        if not product in self._stock:
            raise Exception(f'The product {product} don´t exists')
        self._stock[product] -= count_
        # TODO: Actualizar el registro de venta de un articulo

        if self._stock[product] == 0:
            # Eliminar el precio del producto
            del self._product_price[product]
            # Eliminar el producto del stock
            del self._stock[product]
        total_money = gain_money - self.get_product_price(product) * count_
        self.balance += total_money



    def deliver(self,order:Order):
        pass





class SecondaryCompany(BaseProducer):

    @property
    def tag(self):
        return TypeCompany.SecondaryProvider

    def __init__(self, name: str, environment: SimEnvironment, agent: Agent, env: SimEnvironment):
        super().__init__(name, environment, agent, env)

        self._process_product_price: dict[Product, float] = {}
    #TODO:Carla aca tienes el dic de producto con el precio que se procesan porfa
    @property
    def process_products_price(self)->dict[Product,float]:
        """
        Devuelve el diccionario que tiene por producto que se procesa su precio de venta por procesar
        :return:
        """
        return self._process_product_price
    #TODO:Aca tienes  el precio de procesar un elemento
    def get_price_process_product(self, product: Product):
        """
        Devuelve el precio del producto
        :param product:
        :return:
        """
        if not product in self._process_product_price:
            raise Exception(f"El producto: {product.name} no se encuentra entre los productos a procesar")
        return self._process_product_price[product]

   #TODO:Carla aca es para que llames cuando se vende un servicio de manufactura osea que
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


    def in_storage_product(self,order:Order):
        """
        Cuando se entra a guardar un producto
        :param order:
        :return:
        """
        pass


    # TODO: Crear el send recibe un Order
    def out_storage_product(self,order:Order):
        """
        Cuando se saca un producto del almacen
        :return:
        """

class LogisticCompany(CompanyWrapped):
    """
    Class for the logistic Company
    """

    @property
    def tag(self):
        return TypeCompany.Logistic
