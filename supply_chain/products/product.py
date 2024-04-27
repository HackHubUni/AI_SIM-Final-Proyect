from supply_chain.products.flavor import *
from supply_chain.products.nutritive_properties import *
from abc import ABC, abstractmethod


class Product(ABC):
    """This is the base class for all the products in the simulation. Tha BaseProduct and CreatedProduct inherits from this class"""

    def __init__(
        self,
        name: str,
    ) -> None:
        super().__init__()

    @abstractmethod
    def get_quality(self, time: int) -> float:
        """This function returns the quality of the product at a specific point in time"""
        pass

    def get_name(self) -> str:
        """Returns the name of the product"""
        return self.name

    @abstractmethod
    def get_flavor(self) -> Flavor:
        """Obtain the flavor of the product"""
        pass

    @abstractmethod
    def get_nutritive_properties(self) -> NutritiveProperties:
        """Obtain the nutritive properties of the product"""
        pass
