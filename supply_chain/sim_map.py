import random
import random as rnd

from supply_chain.utils.utility_functions import *


class MapNode:
    """This class represents the connections of a point and the distance to reach all of them"""

    def __init__(self, point: tuple[float, float]) -> None:
        self.point: tuple[float, float] = point
        """The point that this node represents"""
        self.connections: dict[tuple[float, float], float] = {}
        """This represents all the points reachable from this point and the distance to those points"""

    def add_connection(
        self,
        point: tuple[float, float],
        distance: float,
    ) -> bool:
        """This function adds a connection between points"""
        if point in self.connections:
            return False
        real_distance = distance_between_points(self.point, point)
        if distance < real_distance:
            raise Exception(
                f"The distance between the points {self.point} and {point} is {real_distance} and you are trying to add a distance smaller than this"
            )
        self.connections[point] = distance
        return True

    def get_connections(self):
        """Get the list of connections of this map"""
        res = [item for item in self.connections.items()]
        return res

    def get_distance(self, other_point: tuple[float, float]) -> float:
        """Get the distance from this point to the other point"""
        if not other_point in self.connections:
            raise Exception(
                f"The point '{self.point}' has no connection edge to the point '{other_point}'"
            )
        return self.connections[other_point]

    def update_distance(self, point: tuple[float, float], new_distance: float):
        """This method tries to update the distance between the points but raise an exception if the point is not in the connections and if the distance is less than the real distance (geographical distance) between the points"""
        if point not in self.connections:
            raise Exception(
                f"The point {point} doesn't exists in the list of connections of the point {self.point}, that is why is not possible to update the distance"
            )
        real_distance = distance_between_points(self.point, point)
        if new_distance < real_distance:
            raise Exception(
                f"The distance between the points {self.point} and {point} is {real_distance} and you are trying to add a distance smaller than this"
            )
        self.connections[point] = new_distance

    def remove_connection(
        self,
        point: tuple[float, float],
    ) -> bool:
        """This method removes a connection"""
        if point in self.connections:
            self.connections.pop(point, (0, 0))
            return True
        return False


class SimMap:
    """This class represents the map of the city where the
    Companies live"""

    def __init__(
        self,
    ) -> None:
        self.points: dict[tuple[float, float], MapNode] = {}

        self.selected_points: set[tuple[float, float]] = set()
        """
        Set con los puntos que ya tienen alguna empresa
        """

    @property
    def points_tuple_list(self) -> list[tuple[float, float]]:
        """
        Lista con los valores de las coordenadas
        """
        return list(self.points.keys())

    def point_in_map(self, point: tuple[float, float]) -> bool:
        """Returns True if the point is in the map"""
        return point in self.points

    def add_point(self, point: tuple[float, float]) -> bool:
        if self.point_in_map(point):
            return False
        self.points[point] = MapNode(point)
        return True

    def add_directed_connection(
        self,
        point1: tuple[float, float],
        point2: tuple[float, float],
        distance: float,
        create_point_if_not_exist: bool = False,
    ):
        if not create_point_if_not_exist:
            if not self.point_in_map(point1):
                raise Exception(
                    f"The first point ({point1[0]}, {point1[1]}) is not a point in the map"
                )
            if not self.point_in_map(point2):
                raise Exception(
                    f"The second point ({point2[0]}, {point2[1]}) is not a point in the map"
                )
        else:
            # self.points.setdefault(point1, MapNode)
            self.add_point(point1)
            # self.points.setdefault(point2, MapNode)
            self.add_point(point2)
        # self.points[point1].add_connection(point2, distance)
        node = self.points[point1]
        node.add_connection(point=point2, distance=distance)

    def add_bidirectional_connection(
        self,
        point1: tuple[float, float],
        point2: tuple[float, float],
        distance: float,
        create_point_if_not_exist: bool = False,
    ):
        self.add_directed_connection(
            point1, point2, distance, create_point_if_not_exist
        )
        self.add_directed_connection(
            point2, point1, distance, create_point_if_not_exist
        )

    def remove_point(self, point: tuple[float, float]):
        self.points.pop(point, (0, 0))
        for _, map_node in self.points.items():
            map_node.remove_connection(point, (0, 0))

    def add_directed_connection_with_random_distance(
        self,
        point1: tuple[float, float],
        point2: tuple[float, float],
        max_exceeding_distance: float = 1,
        create_point_if_not_exist: bool = False,
    ):
        max_exceeding_distance: float = max(1, max_exceeding_distance)
        real_distance: float = distance_between_points(point1, point2)
        # distance = rnd.randrange(real_distance, real_distance + max_exceeding_distance)
        distance = rnd.uniform(real_distance, real_distance + max_exceeding_distance)
        self.add_directed_connection(
            point1, point2, distance, create_point_if_not_exist
        )

    def add_bidirectional_connection_with_random_distance(
        self,
        point1: tuple[float, float],
        point2: tuple[float, float],
        max_exceeding_distance: float = 1,
        create_point_if_not_exist: bool = False,
    ):
        self.add_directed_connection_with_random_distance(
            point1, point2, max_exceeding_distance, create_point_if_not_exist
        )
        self.add_directed_connection_with_random_distance(
            point2, point1, max_exceeding_distance, create_point_if_not_exist
        )

    def get_connections(self, point: tuple[float, float]) -> MapNode:
        if not self.point_in_map(point):
            raise Exception(f"The point {point} is not in the map")
        res: MapNode = self.points[point]
        return res

    def get_distance(
        self,
        point1: tuple[float, float],
        point2: tuple[float, float],
    ) -> float:
        if not self.point_in_map(point1):
            raise Exception(f"The point {point1} is not in the map")
        if not self.point_in_map(point2):
            raise Exception(f"The point {point2} is not in the map")
        node = self.get_connections(point1)
        return node.get_distance(point2)

    def get_random_point(self) -> tuple[float, float]:
        """
        Devuelve un punto del mapa que nunca ha sido dado anteriormente
        :return:
        """
        if len(self.points_tuple_list)<1 or self.points_tuple_list is None:
            raise Exception(f'la lista con los puntos no puede estar vacia o se None')
        while True:

            value: tuple[float, float] = random.choice(self.points_tuple_list)

            if not value in self.selected_points:
                break

        self.selected_points.add(value)
        return value
