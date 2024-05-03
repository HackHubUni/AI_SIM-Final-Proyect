from typing import *
from typing import Callable
from ...sim_event import SimEvent
from ...company import Company, TypeCompany
from ...client_consumer import ConsumerAgent
from ...events.client_arrival import ClientArrival


class StoreCompany(Company):

    def __init__(
        self,
        name: str,
        get_time: Callable[[], int],
        add_event: Callable[[SimEvent], None],
        next_client_distribution: Callable[[], int],
        create_client
    ) -> None:
        super().__init__(name, get_time, add_event)
        self.next_client_distribution: Callable[[], int] = next_client_distribution
        """This function computes the amount of time to wait for the next client arrival"""

    @property
    def tag(self) -> TypeCompany:
        return TypeCompany.Store

    def start(self):
        # TODO: Implement this
        raise NotImplementedError()

    def add_client(consumer_client: ConsumerAgent) -> None:
        # TODO: Adds a client to the store queue
        pass

    def create_next_client_arrival(self):
        current_time = self.get_time()
        delay = self.next_client_distribution()
        arrival_time = current_time + delay
        client_arrival_event = ClientArrival(arrival_time, )

