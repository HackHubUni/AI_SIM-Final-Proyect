from supply_chain.Building.Builder_base import BuilderBase
from supply_chain.map_search_problem import MapSearchProblem
from supply_chain.sim_map import SimMap
from supply_chain.utils.points_generators import poisson_disc_sampling
import random

class BuilderSimMap(BuilderBase):
    def __init__(self,
                 seed: int,
                 number_of_points: int=40
                 ):
        super().__init__(seed)
        self.number_of_points: int = number_of_points
        self.points = poisson_disc_sampling(self.number_of_points, (0, 0), (5000, 5000), 20, 20)


    def create_instance(self,number_of_connections = 40)->SimMap:

        connections: list[tuple[tuple[float, float], tuple[float, float]]] = []

        simulation_map: SimMap = SimMap()

        for _ in range(number_of_connections):
            p1, p2 = random.sample(self.points, 2)
            connections.append((p1, p2))
            simulation_map.add_bidirectional_connection_with_random_distance(p1, p2, 50, True)

        return simulation_map