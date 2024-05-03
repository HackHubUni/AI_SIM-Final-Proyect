from supply_chain.products.ingredient import Ingredient
from ...recipe import Recipe
from ..base_products.pizza_base_products import *


class PizzaRecipe(Recipe):
    def __init__(
        self,
        ingredients: set[Ingredient],
    ) -> None:
        ingredients = {
            Ingredient(Cheese(initial_quality=90).get_name(), 1),
            Ingredient(TomatoSauce(initial_quality=90).get_name(), 1),
            Ingredient(Salt(initial_quality=90).get_name(), 1),
            Ingredient(PizzaDough(initial_quality=90).get_name(), 1),
        }
        super().__init__("Pizza Recipe", ingredients)
