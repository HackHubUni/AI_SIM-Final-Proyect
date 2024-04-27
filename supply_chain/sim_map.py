from typing import *
from utils.utility_functions import *


class MapNode:
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
            self.connections.pop()
            return True
        return False


class SimMap:
    """This class represents the map of the city where the
    Companies live"""

    def __init__(
        self,
    ) -> None:
        pass
