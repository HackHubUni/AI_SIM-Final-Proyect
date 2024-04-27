from sim_event import *
import heapq


class SupplyChainSimulator:
    def __init__(self, environment: SimEnvironment, simulation_time: int) -> None:
        self.environment: SimEnvironment = environment
        """The environment of the simulation"""
        self.event_queue: list[SimEvent] = []
        """The queue of events to process in the simulation"""
        self.simulation_time: int = simulation_time
        """This define in which moment the simulation most end"""

    def reset(self):
        """Reset the simulation to it's initial parameters"""
        # TODO: We need to implement a class only for storing the simulation parameters.
        # This will make the reset more easy
        self.environment.time = 0
        self.event_queue = []

    def add_event(self, event: SimEvent) -> bool:
        """Add an event to the event queue"""
        if event.time > self.simulation_time:
            return False
        heapq.heappush(self.event_queue, event)
        return True

    def get_next_event(self) -> SimEvent:
        """Get the next event from the event queue"""
        return heapq.heappop(self.event_queue)

    def step(self) -> None:
        """Advance the simulation by one time unit"""
        next_event = self.get_next_event()
        if next_event.time < self.environment.time:
            raise Exception(
                f"The event {next_event} time is less than the current time"
            )
        self.environment.time = next_event.time
        new_events = next_event.execute(self.environment)
        for e in new_events:
            self.add_event(e)
