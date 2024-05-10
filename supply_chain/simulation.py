import heapq

from supply_chain import CompanyConfidence
from supply_chain.agents.matrix_agent import MatrixAgent
from supply_chain.sim_environment import SimEnvironment
from supply_chain.sim_event import *


class SupplyChainSimulator:
    def __init__(self, environment: SimEnvironment, simulation_time: int) -> None:
        self.environment: SimEnvironment = environment
        """The environment of the simulation"""
        self.event_queue: list[SimEvent] = []
        """The queue of events to process in the simulation"""
        self.simulation_time: int = simulation_time
        """This define in which moment the simulation most end"""
        self.company_confidence_: dict[str, CompanyConfidence] = {}
        """
            This dict has for company en the map the CompanyConfidence for the matrix
        """

    def reset(self):
        """Reset the simulation to it's initial parameters"""
        # TODO: We need to implement a class only for storing the simulation parameters.
        # This will make the reset more easy
        self.environment.time = 0
        self.event_queue = []
        self.simulation_over = False

    def add_event(self, event: SimEvent) -> bool:
        """Add an event to the event queue"""
        if event.time > self.simulation_time:
            return False
        heapq.heappush(self.event_queue, event)
        return True

    def get_next_event(self) -> SimEvent:
        """Get the next event from the event queue"""

        return heapq.heappop(self.event_queue)

    def step(self) -> bool:
        """Advance the simulation by one time unit"""
        if len(self.event_queue) == 0:
            print("There is no event left for processing")
            return False
        next_event = self.get_next_event()
        if next_event.time < self.environment.time:
            raise Exception(
                f"The event {next_event} time is less than the current time"
            )
        self.environment.time = next_event.time
        next_event.execute()
        return True



    def run(self):
        print("Starting the simulation")
        self.reset()
         #Create the company confidence dict


        companies = (
            self.environment.companies_in_map + self.environment.matrix_companies
        )

        for company in companies:
            company.start()
        #    if company.tag==TypeCompany.Store:
        #        company.create_next_client_arrival(self.simulation_time)

        #matrix_agent=self.environment.get_matrix_agent()
        #Inicializar el agente matrix
        #matrix_agent.start()
        while self.step():
            continue

        matrix_agent: MatrixAgent = self.environment.get_matrix_agent()
        print("Simulation Over")
        return matrix_agent.matrix_record






