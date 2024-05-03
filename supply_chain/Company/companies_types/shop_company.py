from typing import *
from typing import Callable
from ...sim_event import SimEvent
from ...company import Company, TypeCompany
from ...client_consumer import ConsumerAgent, generate_basic_consumer_agent
from ...events.client_arrival import ClientArrival


class StoreCompany(Company):

    def __init__(
        self,
        name: str,
        get_time: Callable[[], int],
        add_event: Callable[[SimEvent], None],
        next_client_distribution: Callable[[], int],
        # create_client
    ) -> None:
        super().__init__(name, get_time, add_event)
        self.next_client_distribution: Callable[[], int] = next_client_distribution
        """This function computes the amount of time to wait for the next client arrival"""
        self.consumer_queue: list[ConsumerAgent] = []
        self.actual_client: ConsumerAgent = None

    @property
    def tag(self) -> TypeCompany:
        return TypeCompany.Store

    def start(self):
        self.create_next_client_arrival()

    def add_client(self, consumer_client: ConsumerAgent) -> None:
        # TODO: Adds a client to the store queue
        self.consumer_queue.append(consumer_client)

    def process_client(self):
        if self.actual_client is None and len(self.consumer_queue) > 0:
            self.actual_client = self.consumer_queue.pop(0)

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
            self.add_client,
        )
        self.add_event(client_arrival_event)
