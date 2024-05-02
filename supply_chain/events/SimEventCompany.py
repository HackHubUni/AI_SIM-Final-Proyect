from typing import Callable, Self

from supply_chain.sim_environment import SimEnvironment
from supply_chain.sim_event import SimEvent


class CompanyRestockSimEvent(SimEvent):

    def __init__(self, time: int, priority: int, execute: Callable) -> None:
        self._execute: Callable = execute

        super().__init__(time, priority)

    def execute(self, environment: SimEnvironment):
        self._execute()


class WarehouseRestockSimEvent(CompanyRestockSimEvent):
    def __init__(self, time: int, priority: int, execute: Callable[[str, str], []], company_name: str,
                 product_name: str) -> None:
        super().__init__(time, priority, execute)
        self._execute = execute
        self._company_name = company_name
        self._product_name = product_name

    def execute(self, environment: SimEnvironment):
        self._execute(self._company_name, self._product_name)
