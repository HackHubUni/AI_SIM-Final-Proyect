from typing import Callable

class ProductSaleRecord:
    def __init__(self,
                 product_name: str,
                 amount_asked: int,
                 amount_sold: int,
                 total_cost: float,

                 ):
        self.product_name: str=product_name
        self.amount_asked: int=amount_asked
        self.amount_sold: int=amount_sold
        self.total_cost: float=total_cost

class ClientRecord:
    def __init__(self,
                 id_: str,
                 time_arrival: int,

                 get_time: Callable[[], int]

                 ):
        self.get_time: Callable[[], int]=get_time
        self.id_: str = id_
        """
        Id del cliente
        """
        self.time_arrival: int = time_arrival
        """
        Unidad de tiempo en que llegó
        """
        self.time_exit_the_line: int = time_arrival
        """
        Unidad de tiempo en que salio de la cola
        """
        self.time_decide: int = time_arrival
        """
        Unidad de tiempo en el que tomo la decision
        """
        self.buy_product:ProductSaleRecord=None
        """
        Producto que compro
        """
        self.client_departure_time=self.time_decide
        """
        Tiempo en que el cliente se fue de la tienda
        """
        self._how_good_is_the_product: list[float] = []
        """
        Dice que tan bueno es ese producto
        """

    def exit_the_line(self):
        """

        Llamar cuando se saque el cliente de la cola
        :return:
        """
        self.time_exit_the_line=self.get_time()
    def client_buy_food(self,
                        product_name: str,
                        amount_asked: int,
                        amount_sold: int,
                        total_cost: float,

                        ):
        """
        LLamar cuando el cliente se decida
        :param product_name:
        :param amount_asked:
        :param amount_sold:
        :param total_cost:
        :param how_good_is_the_product:
        :return:
        """
        self.time_decide=self.get_time()
        self.buy_product=ProductSaleRecord(product_name,amount_asked,amount_sold, total_cost)

    def how_good_is_the_product(self,product_name:str,how_good:float):
        self._how_good_is_the_product.append(how_good)
    def client_departure(self,time:int):
        """
        Si se la pasa un tiempo menor que el actual toma el tiempo de ida como el actual
        sino el que se le dio
        :param time:
        :return:
        """
        if time<self.get_time():

            self.client_departure_time=self.get_time()
        else:
            self.client_departure_time=time


class ShopRecord:
    def __init__(self, get_time: Callable[[], int]):
        self.get_time: Callable[[], int] = get_time
        self._product_count_sale: dict[str, int] = {}
        self._client_record:dict[str,ClientRecord]={}
    def arrival_new_cliente(self,
                            id_: str,
                            ):
        if id_ in self._client_record:
            raise Exception(f'No se puede atender ds veces al mismo cliente {id_}')

        self._client_record[id_]=ClientRecord(id_,self.get_time(),self.get_time)

    def get_client_record_by_name(self,client_name:str):
        if not client_name in self._client_record:
            raise Exception(f'El cliente {client_name} no existe en el diccionario osea no ha llegado')

        return self._client_record[client_name]
    def process_client(self,client_name:str):
        """
        Decir que el cliente salio de la cola
        :param client_name:
        :return:
        """
        client=self.get_client_record_by_name(client_name)
        #Se fue de la cola
        client.exit_the_line()

    def process_client_buy(self,
                        client_name:str,
                        product_name: str,
                        amount_asked: int,
                        amount_sold: int,
                        total_cost: float,
                        how_good_is_the_product: float,):
        client=self.get_client_record_by_name(client_name)
        client.client_buy_food(product_name,amount_asked,amount_sold, total_cost, how_good_is_the_product)

class Register:
    def __init__(self, get_time: Callable[[], int]):
        self.get_time: Callable[[], int] = get_time

        self._shops_records: dict[str, ShopRecord] = {}
        """
        Registros de actividad por cada tienda
        """
