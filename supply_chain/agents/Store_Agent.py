from typing import Callable

from supply_chain.Company.companies_types.shop_company import StoreCompany
from supply_chain.agent import *
from supply_chain.agents.expert_system.Sistema_experto import SistExperto


class StoreAgent(Agent):

    def __init__(
            self,
            name: str,
            company: StoreCompany,
            get_time: Callable[[], int],
            send_msg: Callable[[Message], None],

    ) -> None:
        super().__init__(name)
        self.company: StoreCompany = company
        self.get_time: Callable[[], int] = get_time
        self.send_msg: Callable[[Message], None] = send_msg
        self.sistema_experto: SistExperto = SistExperto()

    def recive_msg(self, msg: Message):
        pass
