from abc import ABC, abstractmethod
from ingredient import Ingredient, Product


class Recipe:
    """This represents a recipe"""

    def __init__(self, name: str, ingredients: set[Ingredient]) -> None:
        super().__init__()
        self.name: str = name
        """The name of the product this recipe creates"""
        self.ingredients: set[Ingredient] = ingredients
        """The set of ingredients of the product"""

    def get_ingredients(self) -> list[Ingredient]:
        """Returns the list of ingredients of the product"""
        return self.ingredients

    def create(self, ingredients: list[Product]) -> Product:
        """This method creates the product given the ingredients.
        The list of the ingredients is a list of products (Note that the if an ingredient is 5 units of apples then in this list you need to add 5 instances of the apple product)
        This method raise an exception if the ingredients are not sufficient with respect to the demand of this recipe
        """
        # TODO: Implement this
        pass
