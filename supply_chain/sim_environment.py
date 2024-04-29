from typing import *
from sim_map import SimMap
from company import Company
from agent import Agent


class SimEnvironment:
    """This class represents the environment of the simulation.
    The map is an element in the environment"""

    def __init__(
        self,
        sim_map: SimMap,
        companies_in_map: list[Company],
        matrix_companies: list[Company],
        agents: list[Agent],
    ) -> None:
        self.time: int = 0
        """The current time of the simulation"""
        self.sim_map: SimMap = sim_map
        """The map in which the companies live"""
        # TODO: Check that the list of companies in map have a valid position in the simulation map
        # this is, checking that the location point of the company is a location in the map
        """The map where the companies in the simulation lives"""
        self.companies_in_map: list[Company] = companies_in_map
        """The list of companies in the simulation"""
        self.matrix_companies: list[Company] = matrix_companies
        """The list of matrix companies. This are the companies that take the big decisions
        in the supply chain"""
        self.agents: list[Agent] = agents
        """The list of agents in the simulation"""

    def get_map(self) -> SimMap:
        """Returns the map of the simulation"""
        return self.sim_map

    def get_companies_in_map(
        self,
        condition: Callable[[Company], bool],
    ) -> list[Company]:
        """Returns the list of companies in the map that fulfill the condition"""
        result: list[Company] = [
            company for company in self.companies_in_map if condition(company)
        ]
        return result

    def get_matrix_companies(
        self,
        condition: Callable[[Company], bool],
    ) -> list[Company]:
        """Returns the list of matrix companies that fulfill the condition"""
        result: list[Company] = [
            company for company in self.matrix_companies if condition(company)
        ]
        return result

    def get_agent(self, condition: Callable[[Agent], bool]) -> Agent:
        """Returns the first agent that match the condition. If no agent match the condition then None is returned"""
        for agent in self.agents:
            if condition(agent):
                return agent
        return None

    def get_time(self) -> int:
        """Get the current time of the simulation"""
        return self.time
