# %%
from supply_chain.Company.stock_manager.productor_stock_manager import *

product_name = 'pizza'



class BuildProductorStockManager:

    def __init__(self,
                 create_product_lambda: dict[str, Callable[[int], list[Product]]],
                 list_products_can_sell_name: list[str],
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int]
                 ):
        self.create_product_lambda: dict[str, Callable[[int], list[Product]]] = create_product_lambda
        """Lambda para crear el producto"""

        self.list_products_can_sell_name: list[str] = list_products_can_sell_name
        """Lista de productos que puede ofrecer la empresa"""

        self.add_event: Callable[[SimEvent], None] = add_event
        self.get_time: Callable[[], int] = get_time

    def create_products_max_stock(self) -> dict[str, int]:
        dict_return = {}

        for product_name in self.list_products_can_sell_name:
            dict_return[product_name] = 300

        return dict_return

    def create_products_min_stock(self) -> dict[str, int]:
        dict_return = {}

        for product_name in self.list_products_can_sell_name:
            dict_return[product_name] = 30

        return dict_return

    def create_supply_distribution(self) -> Dict[str, Callable[[], int]]:
        """Devuelve la supply_distribution"""

        def distribucion():
            return 5000

        dict_return = {}

        for product_name in self.list_products_can_sell_name:
            dict_return[product_name] = distribucion
        return dict_return

    def create_time_restock_distribution(self) -> Callable[[], int]:

        def distribution():
            return 50

        return distribution

    def create_sale_price_distribution(self) -> dict[str, Callable[[], float]]:

        dict_return = {}

        def distribution():
            return 20.1

        for product_name in self.list_products_can_sell_name:
            dict_return[product_name] = distribution

        return dict_return

    def create_ProductorStockManager(self):
        return ProductorCompanyStock(products_max_stock=self.create_products_max_stock(),
                                     products_min_stock=self.create_products_min_stock(),
                                     create_product_lambda=self.create_product_lambda,
                                     supply_distribution=self.create_supply_distribution(),
                                     sale_price_distribution=self.create_sale_price_distribution(),
                                     time_restock_distribution=self.create_time_restock_distribution(),
                                     add_event=self.add_event,
                                     get_time=self.get_time,

                                     )
