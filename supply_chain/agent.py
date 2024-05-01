from abc import ABC, abstractmethod


class AgentException(Exception):
    pass

class Agent(ABC):
    """Base class for all agents"""

    def __init__(
        self,
        name: str,

    ) -> None:
        super().__init__()
        self.name: str = name
        """The name of the agent"""


    @abstractmethod
    def tell(info):
        # TODO: Carla must type the info variable because every body in the repo
        # should know how to pass info to the agent
        pass
    