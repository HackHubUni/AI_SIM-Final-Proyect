from abc import ABC, abstractmethod, abstractproperty
from supply_chain.sim_environment import SimEnvironment
from enum import Enum
from supply_chain.agents.agent import Agent


class TypeCompany(Enum):
    Matrix = 1
    BaseProducer = 2
    SecondaryProvider = 3
    Logistic = 4
    Warehouse = 5
    Store = 6


class Company(ABC):
    """Base class for all the companies in the supply chain"""

    def __init__(self, name: str, environment: SimEnvironment) -> None:
        super().__init__()
        self.name: str = name
        """The name of the company"""
        self.environment: SimEnvironment = environment
        """The reference to the environment of the simulation"""
        # TODO: Paco, remember that companies offer services. Think in how to model this

    @property
    @abstractmethod
    def tag(self) -> TypeCompany:
        """
        Devuelve el tag del tipo de compañia que es
        :return:
        """
        pass


class CompanyWrapped(Company):

    def __init__(self, name: str, environment: SimEnvironment, agent: Agent):
        super().__init__(name, environment)
        self.agent: Agent = agent


class BaseProducer(CompanyWrapped):
    """Productor de productos base"""

    def __init__(self, name: str, environment: SimEnvironment, agent: Agent):
        if not isinstance(agent, ProducerAgent):
            raise Exception(
                f"The base company need a ProducerAgent not a {type(agent)}"
            )
        super().__init__(name, environment, agent)

        self.plans = self.agent.get_plans()

    @property
    def tag(self):
        return TypeCompany.BaseProducer


class LogisticCompany(CompanyWrapped):
    """
    Class for the logistic Company
    """

    pass
