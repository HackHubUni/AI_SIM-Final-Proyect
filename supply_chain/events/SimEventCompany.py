from typing import Callable, Self

from supply_chain.sim_environment import SimEnvironment
from supply_chain.sim_event import SimEvent


class CompanyRestockSimEvent(SimEvent):

    def __init__(self, time: int, priority: int, execute: Callable) -> None:
        self._execute: Callable = execute

        super().__init__(time, priority)

    def execute(self, environment: SimEnvironment):
        self._execute()
