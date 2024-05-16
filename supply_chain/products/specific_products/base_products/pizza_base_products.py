from ...product import *


class Cheese(Product):
    def __init__(
        self,
        initial_quality: float,
    ) -> None:
        flavor = Flavor(10, 50, 0, 3, 0)
        nutritive_properties = NutritiveProperties(10, 10, 10)
        super().__init__("Cheese", flavor, nutritive_properties, initial_quality)

    @staticmethod
    def get_the_name():
        return 'Cheese'


class TomatoSauce(Product):
    def __init__(
        self,
        initial_quality: float,
    ) -> None:
        flavor = Flavor(40, 30, 0, 0, 0)
        nutritive_properties = NutritiveProperties(10, 10, 10)
        super().__init__("Tomato Sauce", flavor, nutritive_properties, initial_quality)

    @staticmethod
    def get_the_name():
        return 'TomatoSauce'


class Salt(Product):
    def __init__(
        self,
        initial_quality: float,
    ) -> None:
        flavor = Flavor(0, 100, 0, 0, 0)
        nutritive_properties = NutritiveProperties(0, 0, 0)
        super().__init__("Salt", flavor, nutritive_properties, initial_quality)

    @staticmethod
    def get_the_name():
        return 'Salt'


class PizzaDough(Product):

    def __init__(
        self,
        initial_quality: float,
    ) -> None:
        flavor = Flavor(20, 20, 0, 10, 0)
        nutritive_properties = NutritiveProperties(10, 10, 2)
        super().__init__("Pizza Dough", flavor, nutritive_properties, initial_quality)

    @staticmethod
    def get_the_name():
        return 'PizzaDough'
