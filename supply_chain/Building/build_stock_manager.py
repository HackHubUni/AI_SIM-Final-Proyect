
from supply_chain.Company.stock_manager.manufacturing_stock_manager import *
from supply_chain.Company.stock_manager.warehouse_stock_manager import WarehouseStockManager

product_name = 'pizza'

import random


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

        # products_min_stock: dict[str, int],
        # create_product_lambda: Dict[str, Callable[[int], List[Product]]],
        # supply_distribution: Dict[str, Callable[[], int]],
        # sale_price_distribution: dict[str, Callable[[], float]],
        # time_restock_distribution: Callable[[], int],
        # get_time: Callable[[], int],
        # recipe_dic: dict[str, Recipe],
        # price_produce_product_per_unit: dict[str, float]


class BuildingmanufacterStockManager:

    def __init__(self,
                 list_products: list[Product]
                 ):
        self.list_products: list[Product] = list_products

        self.products_names = map(lambda x: x.name, self.list_products)

    def create_products_max_stock(self) -> dict[str, int]:
        dict_return = {}
        rand_int = random.randint(3001, 8564)


class BuildWareHouseStockManager:

    def __init__(self,
                 products_name: list[str],
                 matrix_names: list[str],
                 create_product_lambda: dict[str, Callable[[int], list[Product]]],
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],

                 min_stock_random: int = 500,
                 max_stock_random: int = 6000,
                 company_magic_stock_min_random: int = 300,
                 company_magic_stock_max_random: int = 3500,
                 company_time_stock_min_time: int = 60 * 60 * 24,
                 company_time_stock_max_time: int = 60 * 60 * 24 * 3,
                 company_price_min_restock: int = 20,
                 company_price_max_restock: int = 650,

                 ):
        self.name = ''
        self.products_name: list[str] = products_name

        self.matrixs_names: list[str] = matrix_names

        self.create_product_lambda: dict[str, Callable[[int], list[Product]]] = create_product_lambda

        self.add_event: Callable[[SimEvent], None] = add_event
        self.get_time: Callable[[], int] = get_time

        self.min_random = min_stock_random
        self.max_random = max_stock_random

        self.company_magic_stock_min_random: int = company_magic_stock_min_random
        self.company_magic_stock_max_random: int = company_magic_stock_max_random

        self.company_time_stock_min_time: int = company_time_stock_min_time
        self.company_time_stock_max_time: int = company_time_stock_max_time

        self.company_price_min_restock = company_price_min_restock
        self.company_price_max_restock: int = company_price_max_restock

    def create_product_max_stock(self) -> dict[str, int]:
        dic = {}

        for product_name in self.products_name:
            dic[product_name] = random.randint(self.min_random, self.max_random)

        return dic

    def _create_random_supply_distribution(self, min: int, max: int) -> Callable[[], int]:

        def _random_supply():
            return random.randint(min, max)

        return _random_supply

    def _create_company_product_magic_distribution(self, min_restock_random: int, max_restock_random: int) -> dict[
        str, dict[str, Callable[[], int]]]:
        dict_: dict[str, dict[str, Callable[[], int]]] = {}
        for matrix_name in self.matrixs_names:
            temp_dict: dict[str, Callable[[], int]] = {}
            for product_name in self.products_name:
                temp_dict[product_name] = self._create_random_supply_distribution(
                    min_restock_random, max_restock_random)

            dict_[matrix_name] =temp_dict

        return dict_

    def create_company_product_count_supply_magic_distribution(self) -> dict[str, dict[str, Callable[[], int]]]:

        return self._create_company_product_magic_distribution(self.company_magic_stock_min_random,
                                                               self.company_magic_stock_max_random)

    def create_company_product_time_count_supply_magic_distribution(self) -> dict[str, dict[str, Callable[[], int]]]:
        return self._create_company_product_magic_distribution(self.company_time_stock_min_time,
                                                               self.company_time_stock_max_time)

    def create_company_product_price_supply_magic_distribution(self) -> dict[str, dict[str, Callable[[], float]]]:
        return self._create_company_product_magic_distribution(self.company_price_min_restock,
                                                               self.company_price_max_restock)




    def get_ware_house_stock_manager(self):

        ret=WarehouseStockManager(
            product_max_stock=self.create_product_max_stock(),
            company_product_count_supply_magic_distribution=self.create_company_product_count_supply_magic_distribution(),
            company_product_price_supply_magic_distribution=self.create_company_product_time_count_supply_magic_distribution(),
            create_product_lambda=self.create_product_lambda,
            add_event=self.add_event,
            get_time=self.get_time,




        )
        return ret