from typing import *
from supply_chain.sim_map import SimMap
from supply_chain.company import Company
from supply_chain.agent import Agent
from supply_chain.Message import Message
from .utils.utility_functions import *
from .map_search_problem import *
from .sim_ai.search_problem.search_algorithms import *


class SimEnvironment:
    """This class represents the environment of the simulation.
    The map is an element in the environment"""

    def __init__(
        self,
        sim_map: SimMap,
    ) -> None:
        self.time: int = 0
        """The current time of the simulation"""
        self.sim_map: SimMap = sim_map
        """The map in which the companies live"""
        # TODO: Check that the list of companies in map have a valid position in the simulation map
        # this is, checking that the location point of the company is a location in the map
        """The map where the companies in the simulation lives"""
        self.companies_in_map: list[Company] = []
        """The list of companies in the simulation"""
        self.matrix_companies: list[Company] = []
        """The list of matrix companies. This are the companies that take the big decisions
        in the supply chain"""
        self.agents: list[Agent] = []
        """The list of agents in the simulation"""

    def add_companies_in_map(self, companies_in_map: list[Company]):
        #self.companies_in_map.extend(companies_in_map)
        for company in companies_in_map:
            #Añade la compañia a la lista de compañias
            self.companies_in_map.append(company)
            #Le da a la compañia una posicion en el mapa
            company.set_new_position_in_map(self.sim_map.get_random_point())


    def add_matrix_companies(self, matrix_companies: list[Company]):
        self.matrix_companies.extend(matrix_companies)

    def add_agents(self, agents: list[Agent]):
        self.agents.extend(agents)

    def get_map(self) -> SimMap:
        """Returns the map of the simulation"""
        return self.sim_map

    def send_message(self, message: Message):
        company_name = message.company_destination_name
        companies = self.companies_in_map + self.matrix_companies
        agent_name = ""
        for company in companies:
            if company.name == company_name:
                agent_name = company.name
                break
        if agent_name == "":
            raise Exception(f"There is no company in map with name")
        agent = self.get_agent(lambda ag: ag.name == agent_name)
        agent.recive_msg(message)

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

    def get_minimum_distance(self, company1: str, company2: str) -> float:
        """Get the minimum distance between 2 companies in the map"""
        cp1 = self.get_companies_in_map(lambda comp: comp.name == company1)[0]
        cp2 = self.get_companies_in_map(lambda comp: comp.name == company2)[0]

        def map_heuristic(
            actual_position: tuple[float, float], final_position: tuple[float, float]
        ) -> float:
            return distance_between_points(actual_position, final_position)

        initial_position, final_position = (
            cp1.get_position_in_map(),
            cp2.get_position_in_map(),
        )
        map_problem = MapSearchProblem(
            initial_position=initial_position,
            final_position=final_position,
            city_map=self.sim_map,
        )
        found, final_node = a_star_search(
            map_problem, lambda node: map_heuristic(node.state, final_position)
        )
        if not found:
            return -1
        return final_node.path_cost

    def get_agent(self, condition: Callable[[Agent], bool]) -> Agent:
        """Returns the first agent that match the condition. If no agent match the condition then None is returned"""
        for agent in self.agents:
            if condition(agent):
                return agent
        return None

    def get_time(self) -> int:
        """Get the current time of the simulation"""
        return self.time
