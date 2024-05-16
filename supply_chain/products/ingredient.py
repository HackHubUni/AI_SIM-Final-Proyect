

class Ingredient:
    """This represents a single ingredient for the creation of a product"""

    def __init__(self, product_name: str, amount: int) -> None:
        self.product_name: str = product_name
        """The name of the product"""
        self.amount: int = amount
        """The amount of units needed"""

    def get_product_name(self) -> str:
        """The name of the product that this ingredient needs"""
        return self.product_name

    def get_amount(self) -> int:
        """The number of units of the product needed for the ingredient"""
        return self.amount
