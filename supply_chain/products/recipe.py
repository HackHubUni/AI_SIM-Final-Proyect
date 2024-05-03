from abc import ABC, abstractmethod
from supply_chain.products.ingredient import Ingredient
from supply_chain.products.product import *



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
        return list(self.ingredients)

    @abstractmethod
    def _create_output_product(self, initial_quality: float) -> Product:
        """This method is for internat usage.
        It should create an instance of the output product with an initial quality"""
        pass

    def create(self, ingredients: list[Product]) -> Product:
        """This method creates the product given the ingredients.
        The list of the ingredients is a list of products (Note that the if an ingredient is 5 units of apples then in this list you need to add 5 instances of the apple product)
        This method raise an exception if the ingredients are not sufficient with respect to the demand of this recipe
        """
        products: dict[str, int] = {}
        for product in ingredients:
            products.setdefault(product.name, 0)
            products[product.name] += 1
        new_ingredients = [
            Ingredient(name, amount) for name, amount in products.items()
        ]
        to_compare = set(new_ingredients)
        if self.ingredients != to_compare:
            raise Exception(
                f"The list of products are not sufficient for create the recipe"
            )
        return self._create_output_product()
