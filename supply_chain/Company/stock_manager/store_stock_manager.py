import copy
import random
from typing import Callable

from supply_chain.Company.stock_manager.stock_manager import CompanyStockBase
from supply_chain.products.product import Product
from supply_chain.sim_event import SimEvent


class ShopStockManager(CompanyStockBase):

    def _check(self):

        max_products_keys = set(self.max_product_stock.keys())

        min_products_keys = set(self.min_product_stock.keys())

        product_price_keys = set(self.price_product.keys())

        for product_name in self.products_names:
            if not product_name in self._stock:
                self._stock[product_name] = []

        if max_products_keys != min_products_keys or max_products_keys != product_price_keys:
            raise Exception(
                f"No son iguales las llaves de los dicc de max cant de productos {max_products_keys} y la minima cant de productos {min_products_keys} o del precio del producto {product_price_keys}")

    def __init__(self,
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],
                 init_products: dict[str, list[Product]],
                 min_product_stock: dict[str, int],
                 max_product_stock: dict[str, int],
                 price_product: dict[str, float]

                 ):
        """

        :param add_event:
        :param get_time:
        :param init_products:
        :param min_product_stock: Las cotas son inclusivas
        :param max_product_stock: Las cotas son inclusivas
        """
        self.add_event: Callable[[SimEvent], None] = add_event
        """
        función que brinda poder añadir un evento al simulador
        """
        self.get_time: Callable[[], int] = get_time
        """
        función que brinda el tiempo actual
        """

        self._stock: dict[str, list[Product]] = copy.deepcopy(init_products)
        """
        El stock de la tienda
        """
        self.max_product_stock: dict[str, int] = max_product_stock
        """
        Cant máxima de productos de la tienda
        """
        self.min_product_stock: dict[str, int] = min_product_stock
        """
        Cant mínima de productos de la tienda
        """
        self.products_names: list[str] = list(self.max_product_stock.keys())
        """
        Lista con los productos que se venden 
        """
        self.price_product: dict[str, float] = price_product
        """
        Por producto que se vende en la tienda su precio
        """

        super().__init__(add_event, get_time)

        self._check()

    @property
    def time(self) -> int:
        """
        Da el tiempo actual
        :return:
        """
        return self.get_time()


    def get_all_products_instance(self)->list[Product]:
        """
        Devuelve todos los tipos de producto
        :return:
        """
        lis=[]
        for product_name in self._stock.keys():
            lis.extend(self._stock[product_name])

        return lis


    def add_product(self, product_instance: Product) -> bool:
        """
        Añadir productos al stock
        :param product_instance:
        :return:
        """

        product_name = product_instance.name

        if not product_name in self.products_names:
            raise Exception(f"El producto {product_name} no esta en los productos que vende la tienda")

        if not product_name in self._stock:
            self._stock[product_name] = [product_instance]
            return True

        count_max = self.max_product_stock[product_name]

        product_stock = self._stock[product_name]

        count_in_stock = len(product_stock)

        #TODO: Esto descomentar es lo que no permite qua halla mas stock del que se queria
        if count_max < count_in_stock + 1:
            return False
        #    raise Exception(
        #        f'No se puede añadir más producto {product_name} al stock dado que su límite es {count_max} y hay {count_in_stock}')

        product_stock.append(product_instance)
        # Reorganizar aleatoriamente
        random.shuffle(product_stock)
        return True

    def add_list_products(self, products_list: list[Product]) -> bool:
        """
        Añade una lista de productos
        :param products_list:
        :return:
        """

        for item in products_list:
            if not self.add_product(item):
                return False

        return True

    def count_product_in_stock(self, product_name: str) -> int:

        if not product_name in self.products_names:
            raise Exception(f'El producto {product_name} no se vende en esta tienda')

        if not product_name in self._stock:
            return 0

        stock_lis = self._stock[product_name]

        return len(stock_lis)

    def is_product_in_stock(self, product_name) -> bool:
        """
        Retorna True o False si hay existencia del producto en el stock

        :param product_name:
        :return:
        """
        return self.count_product_in_stock(product_name) > 0

    def is_sale_product(self, product_name: str) -> bool:
        """
        Retorna True si este producto se vende en la tienda
        False en caso contrario
        :param product_name:
        :return:
        """
        return product_name in self.products_names

    def get_list_products_instance(self,product_name:str,count:int):
        count_in_stock=self.count_product_in_stock(product_name)
        if count_in_stock<count:
            raise Exception(f'No se puede pedir {count} productos:{product_name} cuando hay {count_in_stock}')

        lis=[]
        for _ in range(count):
            lis.append(self.get_product_instance(product_name))

        return lis
    def get_product_instance(self,product_name:str):
        if not self.is_product_in_stock(product_name):
            raise Exception(f"No se puede dar el producto {product_name} pq no hay existencias en el stock")

        lis=self._stock[product_name]
        if len(lis)<1:
            raise Exception(f"No se puede dar el producto {product_name} pq no hay existencias en el stock")

        return  lis.pop()


    def get_product_price(self, product_name: str) -> float:
        if not self.is_sale_product(product_name):
            raise Exception(f'El producto :{product_name} no se vende en esta tienda')

        return self.price_product[product_name]

    def restock(self) -> dict[str, int]:
        """
        Chequear que hace falta más productos
        :return: Retorna un diccionario que dice por producto la cant que quiere abastecerse
        Si no hay nada que reabastecer no se pasa nada
        """
        dict_ret: dict[str, int] = {}
        # Chequear por productos

        for product_name in self.products_names:

            count_max = self.max_product_stock[product_name]

            # Ver la cant en stock
            if not product_name in self._stock:
                dict_ret[product_name] = self.max_product_stock[product_name]

            else:
                count_in_stock_now = len(self._stock[product_name])

                count_min = self.min_product_stock[product_name]

                if count_in_stock_now <= count_min:
                    dict_ret[product_name] = count_max - count_in_stock_now

        return dict_ret
