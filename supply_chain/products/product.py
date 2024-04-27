from supply_chain.products.flavor import *
from supply_chain.products.nutritive_properties import *
from abc import ABC, abstractmethod


class Product(ABC):
    """This is the base class for all the products in the simulation. Tha BaseProduct and CreatedProduct inherits from this class"""

    def __init__(
        self,
        name: str,
        flavor: Flavor,
        nutritive_properties: NutritiveProperties,
        initial_quality: float,
    ) -> None:
        super().__init__()
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
        """Returns the name of the product"""
        return self.name

    def get_flavor(self) -> Flavor:
        """Obtain the flavor of the product"""
        return self.flavor

    def get_nutritive_properties(self) -> NutritiveProperties:
        """Obtain the nutritive properties of the product"""
        return self.nutritive_properties

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Product):
            return self.name == value.name
        return False
