from abc import ABC, abstractmethod
from typing import *
from sim_environment import SimEnvironment


class SimEvent:
    """This is the base class for all the events in the simulation"""

    def __init__(self, time: int, priority: int) -> None:
        self.time: int = time
        """The time in which the event should be processed"""
        self.priority: int = priority
        """The priority that helps the simulator to choose an order of execution
        between events in the same time"""

    def __lt__(self, other):
        if not isinstance(other, SimEvent):
            return False
        if self.time < other.time:
            return True
        if self.time == other.time:
            return self.priority < other.priority
        return False

    @abstractmethod
    def execute(self, environment: SimEnvironment) -> list[Self]:
        pass



