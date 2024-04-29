from typing import *
from supply_chain.utils.utility_functions import *


class NutritiveProperties:
    """This class represents the nutritive properties of the products"""

    def __init__(
        self,
        fat: int,
        carbohydrates: int,
        proteins: int,
    ) -> None:
        nutrition = percentage_normalization([fat, carbohydrates, proteins])
        self.fat: float = nutrition[0]
        self.carbohydrates: float = nutrition[1]
        self.proteins: float = nutrition[2]

    def get_nutrition_as_vector(self) -> list[float]:
        return [self.fat, self.carbohydrates, self.proteins]

    def how_similar(self, other_nutritive: Self) -> float:
        """This method returns a float that represents how similar are the nutritive properties.
        The closer to 1 the result of this function, the more similar the nutritive properties will be
        """
        my_vector: list[float] = self.get_nutrition_as_vector()
        other_vector: list[float] = other_nutritive.get_nutrition_as_vector()
        return vector_similarity(my_vector, other_vector)
