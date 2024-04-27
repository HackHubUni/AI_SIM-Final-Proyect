from abc import ABC, abstractmethod
from sim_environment import SimEnvironment


class SimEvent:
    """This is the base class for all the events in the simulation"""

    def __init__(self, time: int, priority: int) -> None:
        self.time: int = time
        """The time in which the event should be processed"""
        self.priority: int = priority
        """The priority that helps the simulator to choose an order of execution
        between events in the same time"""

    @abstractmethod
    def execute(environment: SimEnvironment):
        pass

