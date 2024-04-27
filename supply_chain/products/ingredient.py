from product import Product


class Ingredient:
    """This represents a single ingredient for the creation of a product"""

    def __init__(self, product: Product, amount: int) -> None:
        self.product: Product = product
        """The product of the ingredient"""
        self.amount: int = amount
        """The amount of units needed"""

    def get_product(self) -> Product:
        return self.product

    def get_amount(self) -> int:
        return self.amount
