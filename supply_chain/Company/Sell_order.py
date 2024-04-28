from supply_chain import Company
from supply_chain.products.product import Product


class SellOrder:
    def __init__(self,
                 product_name: str,
                 price_sold: float,
                 amount_asked: int,
                 amount_sold: int,
                 normal_price_per_unit: float,
                 matrix_name: str,
                 to_company: Company,
                 logistic_company: Company
                 ):
        self.product_name: str = product_name
        self.price_sold: float = price_sold
        self.amount_asked: int = amount_asked
        self.amount_sold: int = amount_sold
        self.normal_price_per_unit: float = normal_price_per_unit
        self.matrix_name: str = matrix_name
        self.to_company: Company = to_company
        self.logistic_company: Company = logistic_company


class ProduceOrder(SellOrder):
    """
    Clase para procesar las ventas de
     productos que se tienen que procesar
    """

    def __init__(self,
                 product_name: str,
                 price_sold: float,
                 amount_asked: int,
                 amount_sold: int,
                 normal_price_per_unit: float,
                 matrix_name: str,
                 to_company: Company,
                 logistic_company: Company,
                 ingredients: list[Product]
                 ):
        self.ingredients: list[Product] = ingredients
        super().__init__(product_name,
                         price_sold,
                         amount_asked,
                         amount_sold,
                         normal_price_per_unit,
                         matrix_name,
                         to_company,
                         logistic_company,
                         )
