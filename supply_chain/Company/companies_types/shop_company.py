import copy
from random import random
from typing import Callable

from ..registrers.resgister import ShopRecord
from ..stock_manager.store_stock_manager import ShopStockManager
from ...client_consumer import ConsumerAgent, generate_basic_consumer_agent
from ...company import Company, TypeCompany
from ...events.client_arrival import ClientArrival
from ...events.client_depearture_store import ClientDepearture, ClienteDecide
from ...sim_event import SimEvent


class StoreCompany(Company):

    def __init__(
        self,
        name: str,
        get_time: Callable[[], int],
        add_event: Callable[[SimEvent], None],
        next_client_distribution: Callable[[], int],
        # create_client
            store_stock_manager: ShopStockManager,
    ) -> None:
        super().__init__(name, get_time, add_event)
        self.next_client_distribution: Callable[[], int] = next_client_distribution
        """This function computes the amount of time to wait for the next client arrival"""
        self.consumer_queue: list[ConsumerAgent] = []

        self.store_stock_manager: ShopStockManager = store_stock_manager

        self.actual_client: ConsumerAgent = None

        self._shop_record: ShopRecord = None

        self.need_restock: Callable[[dict[str, int]],None]=None
        """
        Lambda para decirle al agente que me hace falta restock
        """

        self._update_from_agent = False
        """
        True si el agente cuando se inicializo actualizo los datos
        """





    @property
    def tag(self) -> TypeCompany:
        return TypeCompany.Store


    def restock(self):
        """
        Pregunta al stock manager si necesita reabastecer si el dicc no es vacio llama al lambda del agenta para reabastecer
        :return:
        """
        dic=self.store_stock_manager.restock()
        if len(dic)>0:
            self.need_restock(dic)
    def add_from_the_agent(self, shop_record: ShopRecord, need_restock: Callable[[dict[str, int]], None]):
        # Añadir el nuevo shop_record
        self._shop_record = shop_record
        # Añadir el lambda para llamar a restock
        self.need_restock=need_restock

        self._update_from_agent = True

    def get_list_product_instance(self):

       return self.store_stock_manager.get_all_products_instance()


    def start(self):

        if not self._update_from_agent:
            raise Exception(f'El agente de la tienda {self.name} no ha actualizado los datos de esta')
        self.create_next_client_arrival()

    def _add_client(self, consumer_client: ConsumerAgent) -> None:
        # TODO: Adds a client to the store queue
        # Registrar que llego un nuevo cliente
        self._shop_record.arrival_new_cliente(consumer_client.identifier)
        # Añadir a la cola
        self.consumer_queue.append(consumer_client)
        # Se procesa el cliente
        self.process_client()

    def _process_the_client(self):
        """
        Logica de cuando realmente se procesa un cliente
        :return:
        """
        if self.actual_client is None:
            raise Exception(f'El cliente atender no puede ser None')

        menu = copy.deepcopy(self.get_list_product_instance())
        product_name, count_want, where_process = self.actual_client.decide(menu)
        if not self.store_stock_manager.is_sale_product(product_name):
            raise Exception(
                f'El cliente {self.actual_client} no puede pedir un producto {product_name} que no se vende')
        count_buy = count_want
        count_can_by = self.store_stock_manager.count_product_in_stock(product_name)
        price_per_product = self.store_stock_manager.get_product_price(product_name)

        if count_can_by < count_want:
            # Cuanto queria comprar
            count_buy = count_can_by
        # El precio total
        total_cost = count_buy * price_per_product

        # Productos vendidos
        products_instance = self.store_stock_manager.get_list_products_instance(product_name, count_buy)

        # Tomar el record del cliente
        client_record = self._shop_record.get_client_record_by_name(self.actual_client.identifier)
        # Actualizar esta venta
        client_record.client_buy_food(product_name, count_want, count_buy, total_cost)

        for product_instance in products_instance:
            # Guardar que tan bueno era este producto para el cliente
            client_record.how_good_is_the_product(
                self.actual_client.consumer_body.how_good_is_product(product_instance))

        # Ida del cliente

        client_departure = random.randint(0, 3) + self.time
        # Añadir al resgistro el tiempo de ida

        client_record.client_departure_time(client_departure)

        # Crear el evento de que se va del mostrador
        event = ClientDepearture(client_departure, self._process_next_client)
        #Añadir evento
        self.add_event(event)

    def _process_next_client(self):
        """
        Cuando el evento llama a este metodo lo que hace es hacer None el cliente y llamar a procesar al otro
        :return:
        """


        self.actual_client = None
        self.process_client()



    def process_client(self):
        """Procesa un cliente si la cola no esta vacia u no hay nadie en atencion"""
        if self.actual_client is None and len(self.consumer_queue) > 0:
            self.actual_client = self.consumer_queue.pop(0)

            # Añadir a las estadísticas que se fue de la tienda
            self._shop_record.process_client(self.actual_client.identifier)
            # Procesar el cliente
            # El cliente pide
            time_execute = self.actual_client.attending_time() + self.time
            event = ClienteDecide(time_execute, self._process_the_client)
            # Se añade el evento
            self.add_event(event)

    def create_next_client_arrival(self):
        current_time = self.get_time()
        delay = self.next_client_distribution()
        arrival_time = current_time + delay
        client_arrival_event = ClientArrival(
            arrival_time,
            lambda: generate_basic_consumer_agent(
                self.get_time,
                self.add_event,
            ),
            self._add_client,
        )
        self.add_event(client_arrival_event)
