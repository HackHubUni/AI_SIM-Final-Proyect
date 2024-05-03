from supply_chain.products.ingredient import Ingredient, Product
from supply_chain.products.product import Product
from ...recipe import Recipe
from ..base_products.pizza_base_products import *
from ..manufactured_products.pizza import Pizza


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
        super().__init__(Pizza().get_name(), ingredients)

    def _create_output_product(self, initial_quality: float) -> Product:
        return Pizza(initial_quality)
