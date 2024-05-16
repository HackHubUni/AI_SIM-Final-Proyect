from supply_chain.sim_ai.search_problem.problem import SearchProblem
from supply_chain.sim_map import SimMap, MapNode


class MapSearchProblem(SearchProblem):
    """Declaration of the search problem for the map of the companies"""

    def __init__(
        self,
        initial_position: tuple[float, float],
        final_position: tuple[float, float],
        city_map: SimMap,
    ) -> None:
        super().__init__(initial_position)
        self.city_map = city_map
        """The map where the companies live"""
        self.final_position: tuple[float, float] = final_position
        """This represents the goal"""

    def get_actions(self, state) -> list[tuple[float, float]]:
        position: tuple[float, float] = state
        map_node: MapNode = self.city_map.get_connections(position)
        neighbors: list[tuple[float, float]] = []
        for connection in map_node.get_connections():
            other_point: tuple[float, float] = connection[0]
            neighbors.append(other_point)
        return neighbors

    def action_cost(self, state, action) -> float:
        actual_position: tuple[float, float] = state
        new_position: tuple[float, float] = action
        distance: float = self.city_map.get_distance(actual_position, new_position)
        return distance

    def apply_action(self, state, action):
        return action

    def is_final(self, state) -> bool:
        return self.final_position == state
