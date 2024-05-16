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


