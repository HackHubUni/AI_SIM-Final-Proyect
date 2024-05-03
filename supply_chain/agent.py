from abc import ABC, abstractmethod

from supply_chain.Message import Message


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
    def recive_msg(self, msg: Message):
        pass
    @abstractmethod
    def tell(info):
        # TODO: Carla must type the info variable because every body in the repo
        # should know how to pass info to the agent
        pass
    
    