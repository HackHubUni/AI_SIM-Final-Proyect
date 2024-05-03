from typing import *
from supply_chain.utils.utility_functions import *
import random as rnd


class Flavor:
    """This class represents the flavor of a product"""

    def __init__(
        self,
        sweet: float,
        salty: float,
        acid: float,
        bitter: float,
        spicy: float,
    ) -> None:
        flavors = percentage_normalization([sweet, salty, acid, bitter, spicy])
        self.sweet: float = flavors[0]
        self.salty: float = flavors[1]
        self.acid: float = flavors[2]
        self.bitter: float = flavors[3]
        self.spicy: float = flavors[4]

    def get_flavor_as_vector(self) -> list[float]:
        return [self.sweet, self.salty, self.acid, self.bitter, self.spicy]

    def how_similar(self, other_flavor: Self) -> float:
        """This method returns a float that represents how similar are the flavors.
        The closer to 1 the result of this function, the more similar the flavors will be
        """
        my_vector: list[float] = self.get_flavor_as_vector()
        other_vector: list[float] = other_flavor.get_flavor_as_vector()
        return vector_similarity(my_vector, other_vector)

    def get_random_similar_flavor(
        self,
    ) -> Self:
        original = self.get_flavor_as_vector()
        mod = lambda x: max(0, rnd.uniform(0, x * 100))
        new = [mod(val) for val in original]
        return Flavor(*new)
