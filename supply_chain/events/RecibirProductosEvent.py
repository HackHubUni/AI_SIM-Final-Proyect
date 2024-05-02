from typing import Callable, Self

from supply_chain.sim_environment import SimEnvironment
from supply_chain.sim_event import SimEvent

from supply_chain.Comunicator import *


class SendProductEvent(SimEvent):

    def __init__(self, time: int, priority: int, execute: Callable,
                 delivery_Order: HacerServicioDeDistribucion) -> None:
        self._execute: Callable = execute
        self._delivery_order = delivery_Order
        super().__init__(time, priority)

    def execute(self, environment: SimEnvironment):
        self._execute(self._delivery_order)
