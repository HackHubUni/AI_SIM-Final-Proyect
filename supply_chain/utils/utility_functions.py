import math


def percentage_normalization(values: list[float]) -> list[float]:
    """Returns a normalization in percentage of the values.
    The sum of all elements in the returned list is 1"""
    total_sum = sum(values)
    total_sum = total_sum if total_sum > 0 else 1
    return list(value / total_sum for value in values)


def sum_points(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """This function sums 2 points"""
    return (p1[0] + p2[0], p1[1] + p2[1])


def mul_point_by_escalar(p1: tuple[float, float], scalar: float) -> tuple[float, float]:
    """This function multiplies a point with a scalar"""
    return (p1[0] * scalar, p1[1] * scalar)


def distance_between_points(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Return the distance between points"""
    return norm([p1[0] - p2[0], p1[1] - p2[1]])


def point_inside_circle(
    point: tuple[float, float], center: tuple[float, float], radius: float
) -> bool:
    """Returns True if the point is inside the circle"""
    return distance_between_points(point, center) < radius


def boundary_inside_circle(
    bottom_left_point_boundary: tuple[float, float],
    upper_right_point_boundary: tuple[float, float],
    circle_center: tuple[float, float],
    radius: float,
) -> bool:
    """Returns True if the whole boundary is inside the circle"""
    p1 = bottom_left_point_boundary
    p2 = upper_right_point_boundary
    p3 = p1[0], p2[1]
    p4 = p2[0], p1[1]
    points = [p1, p2, p3, p4]
    return any(point_inside_circle(point, circle_center, radius) for point in points)


def norm(vector: list[float]) -> float:
    """Returns the norm of the vector"""
    product = list(one**2 for one in vector)
    return math.sqrt(sum(product))


def vector_similarity(vector_one: list[float], vector_two: list[float]) -> float:
    """Returns how similar are the vectors. This use the cosine similarity.
    The closer to 1 the result of this function, the more similar the vectors will be
    """
    product = list(one * two for one, two in zip(vector_one, vector_two))
    norm_one = norm(vector_one)
    norm_two = norm(vector_two)
    res = sum(product) / (norm_one * norm_two)
    return res * 0.5 + 0.5  # To have the result between 0 and 1
