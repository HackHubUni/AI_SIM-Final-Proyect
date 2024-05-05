from typing import List, Dict, Callable

from supply_chain.products.product import Product



class Product_Generator:
    def __init__(self):
        pass

    def create_products(self, amount: int, product: str) -> List[Product]:
        return [Product(product) for i in range(amount)]

    def create_product_lambda_dict(self, product_names: List[str]) -> Dict[str, Callable[[int], List[Product]]]:
        return {name: self.create_products for name in product_names}




if __name__=="__main__":
    print(Product_Generator().create_product_lambda_dict(['Pizza', 'Cerveza', 'Papas']))
