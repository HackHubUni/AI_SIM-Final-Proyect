import math


def percentage_normalization(values: list[float]) -> list[float]:
    """Returns a normalization in percentage of the values.
    The sum of all elements in the returned list is 1"""
    total_sum = sum(values)
    return list(value / total_sum for value in values)


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
    return sum(product) / (norm_one * norm_two)
