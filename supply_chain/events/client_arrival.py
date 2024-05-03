from ..sim_event import *
from ..client_consumer import *
from ..Company.companies_types.shop_company import StoreCompany



class ClientArrival(SimEvent):
    def __init__(
        self,
        time: int,
        create_client: Callable[[], ConsumerAgent],
        add_client_to_store: Callable[[ConsumerAgent], None],
    ) -> None:
        super().__init__(time, 10)
        self.create_client: Callable[[], ConsumerAgent] = create_client
        """This function creates a new consumer"""
        self.add_client_to_store: Callable[[ConsumerAgent], None] = add_client_to_store
        """This function adds a client in the store"""

    def execute(self):
        consumer = self.create_client()
        self.add_client_to_store(consumer)
