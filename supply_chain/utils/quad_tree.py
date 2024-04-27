from typing import *
from utility_functions import point_inside_circle, boundary_inside_circle


class QuadTreeNode:
    def __init__(
        self,
        bottom_left_point_boundary: tuple[float, float],
        upper_right_point_boundary: tuple[float, float],
        max_points: int = 10,
    ) -> None:
        self.max_points: int = max_points
        """This represents the maximum number of points to store
        before splitting the QuadTreeNode"""
        self.points: list[tuple[float, float]] = []
        """The points stored in the QuadTreeNode if it is not splitted"""
        if not QuadTreeNode.valid_boundaries(
            bottom_left_point_boundary, upper_right_point_boundary
        ):
            raise Exception("Invalid boundaries")
        self.bottom_left_point_boundary: tuple[float, float] = (
            bottom_left_point_boundary
        )
        """The bottom left boundary point of the QuadTreeNode"""
        self.upper_right_point_boundary: tuple[float, float] = (
            upper_right_point_boundary
        )
        """The upper right boundary point of the QuadTreeNode"""
        self.splitted: bool = False
        """This represents if the QuadTreeNode is splitted"""
        self.up_left: QuadTreeNode = None
        """The upper left QuadTreeNode"""
        self.bottom_left: QuadTreeNode = None
        """The bottom left QuadTreeNode"""
        self.up_right: QuadTreeNode = None
        """The upper right QuadTreeNode"""
        self.bottom_right: QuadTreeNode = None
        """The bottom right QuadTreeNode"""

    @staticmethod
    def valid_boundaries(
        bottom_left_point_boundary: tuple[float, float],
        upper_right_point_boundary: tuple[float, float],
    ) -> bool:
        """Returns True if the boundaries are valid"""
        return (
            bottom_left_point_boundary[0] < upper_right_point_boundary[0]
            and bottom_left_point_boundary[1] < upper_right_point_boundary[1]
        )

    @staticmethod
    def point_in_boundaries(
        point: tuple[float, float],
        bottom_left_point_boundary: tuple[float, float],
        upper_right_point_boundary: tuple[float, float],
    ) -> bool:
        """Returns True if the point is in the given boundaries"""
        return (
            bottom_left_point_boundary[0] <= point[0] < upper_right_point_boundary[0]
            and bottom_left_point_boundary[1]
            <= point[1]
            < upper_right_point_boundary[1]
        )

    def point_in_boundary(self, point: tuple[float, float]) -> bool:
        """Returns True if the point is in the boundary of the QuadTreeNode"""
        return QuadTreeNode.point_in_boundaries(
            point, self.bottom_left_point_boundary, self.upper_right_point_boundary
        )

    def find_child_for_point(self, point: tuple[float, float]) -> Self:
        """Returns the quad tree child in which this point belong"""
        if self.up_left.point_in_boundary(point):
            return self.up_left
        if self.up_right.point_in_boundary(point):
            return self.up_right
        if self.bottom_left.point_in_boundary(point):
            return self.bottom_left
        if self.bottom_right.point_in_boundary(point):
            return self.bottom_right
        raise Exception(f"The point is outside the boundaries of the QuadTree")

    def contains(self, point: tuple[float, float]) -> bool:
        """Returns True if the point is already in the QuadTreeNode"""
        if not self.point_in_boundary(point):
            return False
        if self.splitted:
            child = self.find_child_for_point(point)
            return child.contains(point)
        return point in self.points

    def add_point(self, point: tuple[float, float]) -> bool:
        """Adds a point to the QuadTreeNode"""
        if not self.point_in_boundary(point):
            return False
        if self.contains(point):
            return False
        if not self.splitted:
            if len(self.points) < self.max_points:
                if self.point_in_boundary(point):
                    self.points.append(point)
                    return True
                return False
            else:
                self.split_quad_tree_node()
                return self.add_point(point)  # Recursive call
        else:
            child = self.find_child_for_point(point)
            return child.add_point(point)

    def split_quad_tree_node(self) -> None:
        """Splits the QuadTreeNode into four QuadTreeNodes"""
        if self.splitted:
            raise Exception(f"The quad tree is already splitted")
        self.splitted = True
        bottom_point = self.bottom_left_point_boundary
        upper_point = self.upper_right_point_boundary
        self.up_left = QuadTreeNode(
            (bottom_point[0], (bottom_point[1] + upper_point[1]) / 2),
            ((bottom_point[0] + upper_point[0]) / 2, upper_point[1]),
            self.max_points,
        )
        self.bottom_left = QuadTreeNode(
            bottom_point,
            (
                (bottom_point[0] + upper_point[0]) / 2,
                (bottom_point[1] + upper_point[1]) / 2,
            ),
            self.max_points,
        )
        self.up_right = QuadTreeNode(
            (
                (bottom_point[0] + upper_point[0]) / 2,
                (bottom_point[1] + upper_point[1]) / 2,
            ),
            upper_point,
            self.max_points,
        )
        self.bottom_right = QuadTreeNode(
            (
                (bottom_point[0] + upper_point[0]) / 2,
                bottom_point[1],
            ),
            (upper_point[0], (bottom_point[1] + upper_point[1]) / 2),
            self.max_points,
        )
        for point in self.points:
            child = self.find_child_for_point(point)
            child.add_point(point)
        self.points = []

    def get_all_points(self) -> list[tuple[float, float]]:
        """Returns all the points inside this QuadTree"""
        if self.splitted:
            up_left_points = self.up_left.get_all_points()
            up_right_points = self.up_right.get_all_points()
            bottom_left_points = self.bottom_left.get_all_points()
            bottom_right_points = self.bottom_right.get_all_points()
            return (
                up_left_points
                + up_right_points
                + bottom_left_points
                + bottom_right_points
            )
        return [point for point in self.points]

    def get_points_inside_circle(
        self,
        circle_center: tuple[float, float],
        radius: float,
    ) -> list[tuple[float, float]]:
        """Returns the list of points of the Quad Tree that is inside the circle"""
        if self.splitted:
            up_left_points = self.up_left.get_points_inside_circle(
                circle_center, radius
            )
            up_right_points = self.up_right.get_points_inside_circle(
                circle_center, radius
            )
            bottom_left_points = self.bottom_left.get_points_inside_circle(
                circle_center, radius
            )
            bottom_right_points = self.bottom_right.get_points_inside_circle(
                circle_center, radius
            )
            return (
                up_left_points
                + up_right_points
                + bottom_left_points
                + bottom_right_points
            )
        if boundary_inside_circle(
            self.bottom_left_point_boundary,
            self.upper_right_point_boundary,
            circle_center,
            radius,
        ):
            return self.get_all_points()
        out_points: list[tuple[float, float]] = [
            point
            for point in self.points
            if point_inside_circle(point, circle_center, radius)
        ]
        return out_points


class QuadTree:
    """This class represents a QuadTree data structure.
    You have the following basic methods.
    AddPoint: Add a point to the QuadTree
    QueryNeighborPoints: Query the neighbor points of a given point with a given radius
    RemovePoint: Remove a point from the QuadTree
    """

    def __init__(
        self,
        bottom_left_point_boundary: tuple[float, float],
        upper_right_point_boundary: tuple[float, float],
    ) -> None:
        self.count: int = 0
        """The number of points in the QuadTree"""
        self.bottom_left_point_boundary: tuple[float, float] = (
            bottom_left_point_boundary
        )
        """The bottom left point of the QuadTree"""
        self.upper_right_point_boundary: tuple[float, float] = (
            upper_right_point_boundary
        )
        """The upper right point of the QuadTree"""
        self.root: QuadTreeNode = QuadTreeNode(
            self.bottom_left_point_boundary, self.upper_right_point_boundary
        )
        """The root node of this quad tree"""

    def get_count(self) -> int:
        """Returns the number of points in the QuadTree"""
        return self.count

    def add_point(self, point: tuple[float, float]) -> bool:
        if self.root.add_point(point):
            self.count += 1
            return True
        return False

    def get_all_points(self) -> list[tuple[float, float]]:
        """Returns all the points in the QuadTree"""
        return self.root.get_all_points()

    def get_points_in_circle(
        self, center: tuple[float, float], radius: float
    ) -> list[tuple[float, float]]:
        """Returns the list of points that lay inside the circle"""
        return self.root.get_points_inside_circle(center, radius)
