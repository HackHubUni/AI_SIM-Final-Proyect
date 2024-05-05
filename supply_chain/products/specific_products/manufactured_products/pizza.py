from ...product import *


class Pizza(Product):
    def __init__(
        self,
        initial_quality: float,
    ) -> None:
        flavor = Flavor(10, 30, 20, 0, 40)
        nutritive_properties = NutritiveProperties(30, 50, 20)
        super().__init__(
            "Pizza", flavor, nutritive_properties, initial_quality
        )

    @staticmethod
    def get_the_name()->str:
        return "Pizza"

