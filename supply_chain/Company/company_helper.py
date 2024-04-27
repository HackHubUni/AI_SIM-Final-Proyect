from supply_chain.products.product import Product
from typing import Callable, Dict, List

class BaseCompanyReStockException(Exception):
    def

        def __init__(self, message: str):
            super().__init__(message)


class BaseCompanyStock:

    def __init__(self,
                 products_max_stock: dict[str, int],
                 products_min_stock: dict[str, int],
                 create_product_lambda:Dict[str, Callable[[int], List[Product]]],
                 supply_distribution: Dict[str, Callable[[],float]],
                 create_price_distribution: dict[str, Callable[[],float]],
                 sale_price_distribution: dict[str, Callable[[],float]],
                 time_restock_distribution: callable
                 ):
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
        self.supply_distribution: Dict[str, Callable[[],float]] = supply_distribution
        """
        Cant de productos a crear en cada llamado
        """
        self.create_price_distribution: dict[str, Callable[[],float]] = create_price_distribution
        """
        Determina el precio de esta producción
        """
        self.sale_price_distribution: dict[str, Callable[[],float]] = sale_price_distribution
        """
        Función que devuelva siempre >=1 pq osea se multiplica el precio de producción por este coeficiente
        """
        self.time_restock_distribution: callable = time_restock_distribution
        """
        Tiempo a pasar entre cada restock
        """
        self._stock: dict[str,list[Product]] = {}
        """
        El stock de la empresa
        """
        self._sale_product_price: dict[str, float] = {}
        """
        Precio por producto del stock
        """
        self._cost_product_price: dict[str, float] = {}
        """
        El coste de producir ese producto
        """

        self.check()
        """
        Chequear que los nombres de los productos son correctos
        """

    def check(self):
        products_name = self.products_max_stock.keys()
        products_min_stock_name = self.products_min_stock.keys()
        supply_names = self.supply_distribution.keys()
        create_product_lambda = self.create_product_lambda.keys()
        price_distribution = self.create_price_distribution.keys()
        sale_price_name = self.sale_price_distribution.keys()
        if not (set(products_name) == set(supply_names)
                and
                set(supply_names) == set(products_min_stock_name)
                and
                set(
                    supply_names) == set(price_distribution)
                and
                set(
                    price_distribution) == set(sale_price_name)
                and
                set(create_product_lambda) == set(sale_price_name)
        ):
            raise BaseCompanyReStockException(f'The names in the dicts ar different')

    def _actualizar_costos(self, product_name: str, count_supply: int) -> float:
        """
        Actualiza los costos del producto y devuelve el precio de haberlo producido
        :param product_name: nombre del producto
        :param count_supply_int:
        :return:
        """

        # Distribución del costo
        price_to_supply = self.create_price_distribution[product_name]()
        # Actualizar el precio de venta del producto

        #Actualizar el precio de producción del producto
        self._cost_product_price[product_name]=price_to_supply

        actual_sale_distribution = self.sale_price_distribution[product_name]
        # Osea se da el precio de producción por el coeficiente de venta
        self._sale_product_price[product_name] = actual_sale_distribution() * price_to_supply

        # Cuanto Costo en total
        return count_supply * price_to_supply
    def _get_count_supply(self,product_name:str):
        # Se genera una cant de productos
        supply_distribution = self.supply_distribution[product_name]
        # Llamar para saber cuanto seria reabastecer
        count_supply = supply_distribution()
        return count_supply
    def _restock_without_exists(self, product_name: str) -> float:
        # Comprobar el stock actual
        # Si no esta en el stock es pq no hay existencias

        count_supply=self._get_count_supply()
        # saber cuanto es que se puede reabastecer
        max_supply = self.products_max_stock[product_name]
        if count_supply > max_supply:
            count_supply = max_supply
        # Se añade al stock la lista de los productos creados
        self._stock[product_name] = self.create_product_lambda[product_name](count_supply)
        # Actualizar los costos
        return self._actualizar_costos(product_name, count_supply)

    def _restock_with_exists(self, product_name: str):
        count_in_stock = self._stock

    def restock(self) -> float:
        """
        Se reabastece magicamente la empresa
        :return: el precio de reabastecerse
        """
        cost = 0
        product_names = self.products_max_stock.keys()
        # Comprobar si cada producto esta por debajo de una linea
        for product_name in product_names:
            if product_name not in self._stock:
                cost += self._restock_without_exists(product_name)
        else:
