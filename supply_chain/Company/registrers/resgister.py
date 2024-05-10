from typing import Callable

from supply_chain.company import TypeCompany


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
    def __init__(self,
                 shop_name: str,

                 get_time: Callable[[], int]):
        self.shop_name = shop_name
        """
        Nombre de la tienda que el revisa
        """
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

    def get_all_clients_record(self) -> list[ClientRecord]:
        """
        Devuelve todos los clientes que se procesaron
        :return:
        """
        return list(self._client_record.values())

class Register:
    def __init__(self, get_time: Callable[[], int]):
        self.get_time: Callable[[], int] = get_time

        self._shops_records: dict[str, ShopRecord] = {}
        """
        Registros de actividad por cada tienda
        """

    def get_store_record_by_store(self, store_name: str):
        if not store_name in self._shops_records:
            new_store_record = ShopRecord(self.get_time)
            self._shops_records[store_name] = new_store_record
            return new_store_record

    def get_all_stock_record(self) -> list[ShopRecord]:
        """
        llamar cuando finalize para tener todos los StockRecord
        :return:
        """
        return list(self._shops_records.values())


class ProcesingOrdersRecord:
    def __init__(self,
                 store_to_supply: str,
                 order_supply_store_id: str,
                 company_make_buss_name: str,
                 company_make_buss_type: TypeCompany,
                 company_destination_process_name: str,
                 company_destination_process_type: TypeCompany,
                 logistic_name:str,
                 product_buy_name: str,
                 product_count_buy: int,
                 time_acept_the_buy_order: int,
                 time_process_the_buy_order: int,
                 price_cost_per_unit: float

                 ):
        self.logistic_name:str=logistic_name
        self.store_to_supply: str = store_to_supply
        self.order_supply_store_id: str = order_supply_store_id
        self.company_make_buss_name: str = company_make_buss_name
        self.company_make_buss_type: TypeCompany = company_make_buss_type
        self.company_destination_process_name: str = company_destination_process_name
        self.company_destination_process_type: TypeCompany = company_destination_process_type
        self.product_buy_name: str = product_buy_name
        self.product_count_buy: int = product_count_buy
        self.time_acept_the_buy_order: int = time_acept_the_buy_order

        """
        Tiempo en que la matrix mando a procesar la orden de compra
        """
        self.time_process_the_buy_order: int = time_process_the_buy_order
        """
        Tiempo en que la otra empresa ejecuto la orden de compra
        """
        self.price_cost_per_unit: float = price_cost_per_unit
class MatrixRecord:

    def start(self):
        for store_name in self.store_names:
            self.dict_store_records[store_name] = ShopRecord(store_name, self.get_time)
    def __init__(self,seed:int,store_names:list[str],get_time:Callable[[],int],corrida:int=1,):
        self.seed: int=seed
        self.corrida: int = corrida
        self.store_names:list[str]=store_names
        self.get_time: Callable[[], int] = get_time

        self.dict_store_records:dict[str,ShopRecord]={}

        self.start()

        self.dict_buy_records: dict[str, list[ProcesingOrdersRecord]] = {}
        """
        Diccionario con los nombres de los records de las compras
        """

    def get_store_record(self,store_name:str):

        if not store_name in self.dict_store_records:
            raise Exception(f'La tienda {store_name} no tiene ShopRecord')

        return self.dict_store_records[store_name]

    def _create_procesing_order_record(self,
                                       store_to_supply: str,
                                       order_supply_store_id: str,
                                       company_make_buss_name: str,
                                       company_make_buss_type: TypeCompany,
                                       company_destination_process_name: str,
                                       company_destination_process_type: TypeCompany,
                                       logistic_name:str,
                                       product_buy_name: str,
                                       product_count_buy: int,
                                       time_acept_the_buy_order: int,
                                       time_process_the_buy_order: int,
                                       price_cost_per_unit: float

                                       ):
        return ProcesingOrdersRecord(

            store_to_supply=store_to_supply,
            order_supply_store_id=order_supply_store_id,
            company_make_buss_name=company_make_buss_name,
            company_make_buss_type=company_make_buss_type,
            company_destination_process_name=company_destination_process_name,
            company_destination_process_type=company_destination_process_type,
            logistic_name=logistic_name,
            product_buy_name=product_buy_name,
            product_count_buy=product_count_buy,
            time_acept_the_buy_order=time_acept_the_buy_order,
            time_process_the_buy_order=time_process_the_buy_order,
            price_cost_per_unit=price_cost_per_unit
        )

    def add_buy_record(self,
                       store_want_product_id,
                       store_to_supply: str,
                       order_supply_store_id: str,
                       company_make_buss_name: str,
                       company_make_buss_type: TypeCompany,
                       company_destination_process_name: str,
                       company_destination_process_type: TypeCompany,

                       product_buy_name: str,
                       product_count_buy: int,

                       time_process_the_buy_order: int,
                       price_cost_per_unit: float,
                       logistic_name:str,

                       ):

        buy_record = self._create_procesing_order_record(store_to_supply=store_to_supply,
                                                         order_supply_store_id=order_supply_store_id,
                                                         company_make_buss_name=company_make_buss_name,
                                                         company_make_buss_type=company_make_buss_type,
                                                         company_destination_process_name=company_destination_process_name,
                                                         company_destination_process_type=company_destination_process_type,
                                                         logistic_name=logistic_name,
                                                         product_buy_name=product_buy_name,
                                                         product_count_buy=product_count_buy,
                                                         time_acept_the_buy_order=self.get_time(),
                                                         time_process_the_buy_order=time_process_the_buy_order,
                                                         price_cost_per_unit=price_cost_per_unit)

        if not store_want_product_id in self.dict_buy_records:
            self.dict_buy_records[store_want_product_id] = [buy_record]
            return

        self.dict_buy_records[store_want_product_id].append(buy_record)
