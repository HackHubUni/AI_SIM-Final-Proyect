from abc import ABC, abstractmethod
from supply_chain.sim_environment import SimEnvironment


class Company(ABC):
    """Base class for all the companies in the supply chain"""

    def __init__(self, name: str, environment: SimEnvironment) -> None:
        super().__init__()
        self.name: str = name
        """The name of the company"""
        self.environment: SimEnvironment = environment
        """The reference to the environment of the simulation"""
        # TODO: Paco, remember that companies offer services. Think in how to model this
