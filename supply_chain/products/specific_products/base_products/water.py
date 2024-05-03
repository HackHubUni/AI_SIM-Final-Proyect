from ...product import *


class Water(Product):
    def __init__(
        self,
        initial_quality: float,
    ) -> None:
        flavor = Flavor(0, 0, 0, 0, 0)
        nutritive_properties = NutritiveProperties(0, 0, 0)
        super().__init__("Water", flavor, nutritive_properties, initial_quality)
