from ...product import *


class Yeast(Product):
    def __init__(
        self,
        initial_quality: float,
    ) -> None:
        flavor = Flavor(0, 0, 0, 0, 0)
        nutritive_properties = NutritiveProperties(0, 0, 0)
        super().__init__("Yeast", flavor, nutritive_properties, initial_quality)
