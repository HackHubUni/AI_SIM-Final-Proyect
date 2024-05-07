import copy
from typing import Callable

from ..stock_manager.store_stock_manager import ShopStockManager
from ...client_consumer import ConsumerAgent, generate_basic_consumer_agent
from ...company import Company, TypeCompany
from ...events.client_arrival import ClientArrival
from ...events.client_depearture_store import ClientDepearture
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

    @property
    def tag(self) -> TypeCompany:
        return TypeCompany.Store

    def get_list_product_instance(self):

       return self.store_stock_manager.get_all_products_instance()

    def start(self):


        self.create_next_client_arrival()

    def _add_client(self, consumer_client: ConsumerAgent) -> None:
        # TODO: Adds a client to the store queue
        self.consumer_queue.append(consumer_client)
        # Se procesa el cliente
        self.process_client()

    def _process_the_client(self):
        menu = copy.deepcopy(self.get_list_product_instance())
        product_name, count_want, where_process = self.actual_client.decide(menu)
        if not self.store_stock_manager.is_sale_product(product_name):
            raise Exception(
                f'El cliente {self.actual_client} no puede pedir un producto {product_name} que no se vende')
        count_buy = count_want
        count_can_by = self.store_stock_manager.count_product_in_stock(product_name)
        price_per_product = self.store_stock_manager.get_product_price(product_name)

        if count_can_by < count_want:
            # TODO:Añadir aca cuanto queria comprar
            count_buy = count_can_by
        # TODO:AÑAdir el coste
        total_cost = count_buy * price_per_product

        products_instance = self.store_stock_manager.get_list_products_instance(product_name, count_buy)
        lis_how_good = []
        for product_instance in products_instance:
            lis_how_good.append(self.actual_client.consumer_body.how_good_is_product(product_instance))

        # El cliente se va de la tienda
        time_execute = self.actual_client.attending_time()
        event = ClientDepearture(time_execute, self.process_client)
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
            # Procesar el cliente
            self._process_the_client()

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
