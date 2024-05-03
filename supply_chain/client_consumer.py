from uuid import uuid4
import random as rnd
from typing import *
from .products.flavor import Flavor
from .products.nutritive_properties import NutritiveProperties
from .products.product import Product
from .sim_event import SimEvent


class ConsumerBody:
    """This class represents a client of a shop that decides for products to buy"""

    def __init__(
        self,
        ideal_flavor: Flavor,
        ideal_nutrition_properties: NutritiveProperties,
    ) -> None:
        self.ideal_flavor: Flavor = ideal_flavor
        self.ideal_nutrition_properties: NutritiveProperties = (
            ideal_nutrition_properties
        )

    def how_good_is_product(self, product: Product) -> float:
        """This method says how good is a product"""
        flavor_score: float = self.ideal_flavor.how_similar(product.get_flavor())
        nutritive_score: float = self.ideal_nutrition_properties.how_similar(
            product.get_nutritive_properties()
        )
        return flavor_score * nutritive_score  # TODO: Improve this implementation


class ConsumerAgent:
    def __init__(
        self,
        get_time: Callable[[], int],
        add_event: Callable[[SimEvent], None],
        attending_time: Callable[[], int],
        amount_selection: Callable[[], int],
    ) -> None:
        self.identifier: str = str(uuid4())
        """The unique identifier of the client"""
        self.consumer_body: ConsumerBody = generate_consumer_body()
        """The body of this consumer"""
        self.get_simulation_time: Callable[[], int] = get_time
        """Function to get the current time of the simulation"""
        self.add_event: Callable[[SimEvent], None] = add_event
        """Function to add an event"""
        self.attending_time: Callable[[], int] = attending_time
        """Function that represents the time that this client takes to select a product"""
        self.amount_selection: Callable[[], int] = amount_selection
        """This method represents the amount of units of a product this client will select"""

    def decide(self, product_list: list[tuple[Product, int]]) -> tuple[Product, int]:
        # TODO: This method should add a ShopSellEvent
        if len(product_list) == 0:
            raise Exception(f"The product list is empty. This should not happen")
        weights = [
            self.consumer_body.how_good_is_product(product)
            for product, _ in product_list
        ]
        selected_product = rnd.choices(product_list, weights)[0]
        # TODO: Select the number of units to ask


def generate_consumer_body() -> ConsumerBody:
    """Generate a random Consumer Body with tendency to the sweet flavor and high carbohydrates"""
    base_ideal_flavor = Flavor(50, 30, 5, 5, 5)
    base_ideal_nutrition = NutritiveProperties(10, 40, 30)
    return ConsumerBody(
        base_ideal_flavor.get_random_similar_flavor(),
        base_ideal_nutrition.get_random_similar_flavor(),
    )
