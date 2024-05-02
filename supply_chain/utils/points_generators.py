from collections import deque
import random as rnd
import math
from quad_tree import QuadTree
from utility_functions import sum_points, mul_point_by_escalar


def poisson_disc_sampling(
    number_of_points: int,
    bottom_left_point_boundary: tuple[float, float],
    upper_right_point_boundary: tuple[float, float],
    minimum_distance: float = 1,
    max_rejection: int = 30,
) -> list[tuple[float, float]]:
    # TODO: Handle the case where the boundaries are invalid
    space = QuadTree(bottom_left_point_boundary, upper_right_point_boundary)
    mid_point = (
        (bottom_left_point_boundary[0] + upper_right_point_boundary[0]) / 2,
        (bottom_left_point_boundary[1] + upper_right_point_boundary[1]) / 2,
    )
    spawn_points: list[tuple[float, float]] = []
    spawn_points.append(mid_point)
    while len(spawn_points) > 0:
        random_index = rnd.randint(0, len(spawn_points) - 1)
        spawn_point = spawn_points[random_index]
        valid_spawn_point: bool = False
        for _ in range(max_rejection):
            new_point = _generate_point(spawn_point, minimum_distance)
            points = space.get_points_in_circle(new_point, minimum_distance)
            if len(points) > 0:
                continue
            valid_spawn_point = space.add_point(new_point)
            spawn_points.append(new_point)
            if space.get_count() >= number_of_points:
                return space.get_all_points()
        if not valid_spawn_point:
            spawn_points.remove(spawn_point)
    if space.get_count() < number_of_points:
        raise Exception("For some reason it was imposible to generate all the points")


def naive_generator_of_points(
    number_of_points: int,
    bottom_left_point_boundary: tuple[float, float],
    upper_right_point_boundary: tuple[float, float],
    minimum_distance: float = 1,
) -> list[tuple[float, float]]:
    space = QuadTree(bottom_left_point_boundary, upper_right_point_boundary)
    while space.get_count() < number_of_points:
        new_point = _generate_point2(
            bottom_left_point_boundary, upper_right_point_boundary
        )
        points = space.get_points_in_circle(new_point, minimum_distance)
        if len(points) > 0:
            continue
        space.add_point(new_point)
    return space.get_all_points()


def _generate_point(center: tuple[float, float], radius: float) -> tuple[float, float]:
    """Asistan function for generating a single point for the poisson disc sampling"""
    angle = rnd.random() * 2 * math.pi
    direction: tuple[float, float] = (math.sin(angle), math.cos(angle))
    length = rnd.uniform(radius, 2 * radius)
    point = sum_points(center, mul_point_by_escalar(direction, length))
    return point


def _generate_point2(
    bottom_left: tuple[float, float], up_right: tuple[float, float]
) -> tuple[float, float]:
    return (
        rnd.randint(bottom_left[0], up_right[0]),
        rnd.randint(bottom_left[1], up_right[1]),
    )
