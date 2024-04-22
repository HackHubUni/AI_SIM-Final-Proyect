from supply_chain.products.flavor import *
from supply_chain.products.nutritive_properties import *
from abc import ABC, abstractmethod


class Product(ABC):
    """This class represents the products of the simulation"""

    def __init__(
        self,
        name: str,
        flavor: Flavor,
        nutritive_properties: NutritiveProperties,
        initial_quality: float,
    ) -> None:
        self.name: str = name
        """The name of the product"""
        self.flavor: Flavor = flavor
        self.nutritive_properties: NutritiveProperties = nutritive_properties
        # TODO: Check if the quality is greater than 0 and less equal than 100
        self.initial_quality: float = initial_quality
        """The initial quality of the product"""

    @abstractmethod
    def get_quality(self, time: int) -> float:
        """This function returns the quality of the product at a specific point in time"""
        pass

    def get_name(self) -> str:
        return self.name

    def get_flavor(self) -> Flavor:
        return self.flavor

    def get_nutritive_properties(self) -> NutritiveProperties:
        return self.nutritive_properties
