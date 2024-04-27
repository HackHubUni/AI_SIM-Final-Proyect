from supply_chain.products.product import Product
from typing import Callable, Dict, List
from abc import ABC, abstractmethod, abstractproperty

from supply_chain.sim_environment import SimEnvironment


class BaseCompanyReStockException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class CompanyStock(ABC):
    @abstractmethod
    def restock(self):
        """
        Se reabastece magicamente la empresa
        :return: el precio de reabastecerse
        """
        pass


class BaseCompanyStock(CompanyStock):

    def __init__(self,
                 products_max_stock: dict[str, int],
                 products_min_stock: dict[str, int],
                 create_product_lambda: Dict[str, Callable[[int], List[Product]]],
                 supply_distribution: Dict[str, Callable[[], int]],
                 sale_price_distribution: dict[str, Callable[[], float]],
                 time_restock_distribution: Callable[[], int],
                 environment: SimEnvironment
                 ):

        self.env = environment
        """
        El env de la simulación
        """

        self.products_max_stock: dict[str, int] = products_max_stock
        """
        Cant maxima de productos en stock
        """
        self.products_min_stock: dict[str, int] = products_min_stock
        """
        Cant mínima de productos en stock
        """
        self.create_product_lambda: Dict[str, Callable[[int], List[Product]]] = create_product_lambda
        """
        Guarda el producto, su lambda a crear, cada vez se llame devuelve una lista con los productos se le pasa la cant a 
         producir como un entero count
        """
        self.supply_distribution: Dict[str, Callable[[], int]] = supply_distribution
        """
        Cant de productos a crear en cada llamado
        """

        self.sale_price_distribution: dict[str, Callable[[], float]] = sale_price_distribution
        """
        Función que devuelva siempre >=1 pq osea se multiplica el precio de producción por este coeficiente
        """
        self.time_restock_distribution: Callable[[], int] = time_restock_distribution
        """
        Tiempo a pasar entre cada restock
        """

        # Locales

        self._stock: dict[str, list[Product]] = {}
        """
        El stock de la empresa
        """
        self._sale_product_price: dict[str, float] = {}
        """
        Precio por producto del stock
        """

        self._check()
        """
        Chequear que los nombres de los productos son correctos
        """

    @property
    def stock(self):
        """Brinda el stock de la empresa"""
        return self._stock

    @property
    def sale_product_price(self):
        """
        Da el diccionario del precio por producuto
        :return:

        """
        return self._sale_product_price

    def _check(self):
        products_name = self.products_max_stock.keys()
        products_min_stock_name = self.products_min_stock.keys()
        supply_names = self.supply_distribution.keys()
        create_product_lambda = self.create_product_lambda.keys()
        sale_price_name = self.sale_price_distribution.keys()
        if not (set(products_name) == set(supply_names)
                and
                set(supply_names) == set(products_min_stock_name)
                and
                set(
                    supply_names) == set(products_min_stock_name)
                and
                set(create_product_lambda) == set(sale_price_name)
        ):
            raise BaseCompanyReStockException(f'The names in the dicts ar different')

    def _actualizar_costos(self, product_name: str):
        """
        Actualiza los costos de venta del producto del producto
        :param product_name: Nombre del producto
        :return:
        """

        # Actualizar el precio de venta del producto

        actual_sale_distribution = self.sale_price_distribution[product_name]
        # Osea se da el precio de venta del producto
        self._sale_product_price[product_name] = actual_sale_distribution()

    def _get_count_supply(self, product_name: str) -> int:
        """
        Da la cant de productos a se quisiera abastecer por la función de cuanto a abastecer
        :param product_name: nombre del producto
        :return: cuantos se quisieran abastecer
        """
        # Se genera una cant de productos
        supply_distribution = self.supply_distribution[product_name]
        # Llamar para saber cuanto seria reabastecer
        count_supply = supply_distribution()
        return count_supply

    def _restock_without_exists(self, product_name: str) -> bool:
        """
        Si un producto no esta en stock, pq no hay existencias de el
        se reabastece
        :param product_name:
        :return: bool: True si se reabasteció
        """
        # Comprobar el stock actual
        # Si no esta en el stock es pq no hay existencias

        count_supply = self._get_count_supply(product_name)
        # saber cuanto es que se puede reabastecer
        max_supply = self.products_max_stock[product_name]
        if count_supply > max_supply:
            count_supply = max_supply
        # Se añade al stock la lista de los productos creados
        self._stock[product_name] = self.create_product_lambda[product_name](count_supply)
        # Actualizar los costos
        self._actualizar_costos(product_name)

        return True

    def _restock_with_exists(self, product_name: str) -> bool:
        """
        Si hay existencias en el stock de un producto reabastece lo que se desea reabastecer, siempre respetando la cota máxima
        de producto en stock
        :param product_name:
        :return: True:Si se reabasteció, False: Si no se reabasteció
        """
        count_in_stock = len(self._stock[product_name])

        # Si todavía no hay que reabastecer
        if count_in_stock >= self.products_min_stock[product_name]:
            return False
        # Cuanto se quiere satisfacer
        count_want_supply: int = self._get_count_supply(product_name)

        # Cuanto queda por llenar
        count_to_supply: int = self.products_max_stock[product_name] - count_in_stock

        if count_want_supply < count_to_supply:
            # Si la cant que se quiere suministrar es menor que la cant que queda para llegar al máximo
            count_to_supply = count_want_supply

            # Se toma la lista de productos en stock

            lis_temp = self._stock[product_name]
            # Se toma añade  a la lista del stock actual los recién creados y se actualiza el stock
            self._stock[product_name] = lis_temp + self.create_product_lambda[product_name](count_to_supply)
            # Actualizar los costos
            self._actualizar_costos(product_name)

            return False

    def _next_restock(self):
        # TODO: llamar lanzar el evento
        time_next_restock = self.time_restock_distribution()

    def restock(self):
        """
        Se reabastece magicamente la empresa
        :return: el precio de reabastecerse
        """

        product_names = self.products_max_stock.keys()

        for product_name in product_names:
            # Si esta en el stock

            if product_name not in self._stock:
                self._restock_without_exists(product_name)
            else:
                # Si no esta en el stock
                self._restock_with_exists(product_name)

        # Lanzar el evento de reabastecer en el próximo tiempo

        self._next_restock()
