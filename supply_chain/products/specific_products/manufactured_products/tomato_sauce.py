from ...product import *


class TomatoSauce(Product):
    def __init__(
        self,
        name: str,
        flavor: Flavor,
        nutritive_properties: NutritiveProperties,
        initial_quality: float,
    ) -> None:
        super().__init__(name, flavor, nutritive_properties, initial_quality)
