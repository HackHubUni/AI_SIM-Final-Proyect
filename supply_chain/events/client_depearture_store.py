from typing import Callable

from supply_chain.sim_event import SimEvent


class ClientDepearture(SimEvent):
    def __init__(self,
                 time_execute:int,

                 execute: Callable[[], None]

                 ):
        super().__init__(time_execute,9)
        self._execute:Callable[[],None]=execute

    def execute(self):

        self._execute()
