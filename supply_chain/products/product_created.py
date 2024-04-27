from abc import ABC, abstractmethod
from ingredient import Ingredient, Product
from flavor import Flavor
from nutritive_properties import NutritiveProperties


class ProductCreated(Product):
    def __init__(self, name: str, ingredients: list[Ingredient]) -> None:
        super().__init__()
        self.name: str = name
        """The name of the created product"""
        self.ingredients: list[Ingredient] = ingredients
        """The list of ingredients of the product"""

    def get_ingredients(self) -> list[Ingredient]:
        """Returns the list of ingredients of the product"""
        return self.ingredients

    def get_quality(self, time: int) -> float:
        # TODO: Implement this method
        pass

    def get_flavor(self) -> Flavor:
        # TODO: Implement this method
        pass

    def get_nutritive_properties(self) -> NutritiveProperties:
        # TODO: Implement this method
        pass
