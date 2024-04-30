import copy

from supply_chain.events.SimEventCompany import CompanyRestockSimEvent
from supply_chain.products.ingredient import Ingredient
from supply_chain.products.product import Product
from typing import Callable, Dict, List, Any, Tuple
from abc import ABC, abstractmethod, abstractproperty

from supply_chain.products.recipe import Recipe
from supply_chain.sim_environment import SimEnvironment
from supply_chain.sim_event import SimEvent


class BaseCompanyReStockException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class CompanyStockBase(ABC):
    @abstractmethod
    def restock(self):
        """
        Se reabastece mágicamente la empresa
        :return: el precio de reabastecerse
        """
        pass


class BaseCompanyStock(CompanyStockBase):

    def __init__(self,
                 products_max_stock: dict[str, int],
                 products_min_stock: dict[str, int],
                 create_product_lambda: Dict[str, Callable[[int], List[Product]]],
                 supply_distribution: Dict[str, Callable[[], int]],
                 sale_price_distribution: dict[str, Callable[[], float]],
                 time_restock_distribution: Callable[[], int],
                 quality_distribution: dict[str, Callable[[], float]],
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int]
                 ):

        self.add_event: Callable[[SimEvent], None] = add_event
        """
        función que brinda poder añadir un evento al simulador
        """
        self.get_time: Callable[[], int] = get_time
        """
        función que brinda el tiempo actual
        """
        self.quality_distribution: dict[str, Callable[[], float]] = quality_distribution
        """
        
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
        Da el diccionario del precio por producto
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
        # Nuevo tiempo
        next_restock = self.time_restock_distribution()
        time_next_restock = self.get_time() + next_restock
        event = CompanyRestockSimEvent(time_next_restock, 0, self.restock)
        # Añadir evento al simulador
        self.add_event(event)

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

    def get_count_product_in_stock(self, product_name: str):
        """
        Retorna la cant de unidades de un producto en stock
        -1 si no está en stock
        :param product_name:
        :return: La cant de unidades que hay en stock de un producto dado, - si no hay
        """
        if product_name not in self._stock:
            return -1
        return len(self._stock[product_name])

    def get_products_by_name(self, product_name: str, count: int) -> list[Product]:
        """
              Es para tener la logica de como se quita producto del stock en una cant dada
              Lanza exception si se pide mas que la cant de productos que hay en stock
              :param product_name:
              :param count:
              :return: lista de productos a devolver para la venta
              """

        if product_name not in self._stock:
            raise Exception(f"The product {product_name} don´t exists")

        # Chequear que la cant de producto que se tiene en stock es suficiente
        count_in_stock: int = len(self._stock[product_name])
        if count_in_stock < count:
            raise Exception(
                f"Don t have {count} of the product {product_name} only have {count_in_stock}")
        lis = self._stock[product_name]
        lis_old_len = len(lis)
        temp = copy.deepcopy(lis)
        # elimina los n primeros elementos de la lista
        lis = lis[count:]
        lis_new_len = len(lis)

        will_be = (lis_old_len - count)

        # asegurarse que la cant de productos que tiene la lista nueva del stock es el viejo stock- lo que se quiere pedir
        assert lis_new_len == will_be, f'The product {product_name} want to get {count} units and the new stock will be {lis_new_len} not {will_be}'

        # Si se piden todos los productos
        if len(lis) < 1:
            del self._stock[product_name]
            del self._sale_product_price[product_name]
        else:

            self._stock[product_name] = lis

        return temp[0:count]

    def get_product_price_per_unit(self, product_name: str) -> float:
        """
        Devuelve la el precio de venta de una unidad del producto

        :param product_name: nombre del producto
        :return: el precio de venta del producto, -1 si no hay existencias
        """
        if product_name not in self.sale_product_price:
            return -1
        return self._sale_product_price[product_name]


class ManufacturingStock(BaseCompanyStock):
    def __init__(self,
                 products_max_stock: dict[str, int],
                 products_min_stock: dict[str, int],
                 create_product_lambda: Dict[str, Callable[[int], List[Product]]],
                 supply_distribution: Dict[str, Callable[[], int]],
                 sale_price_distribution: dict[str, Callable[[], float]],
                 time_restock_distribution: Callable[[], int],
                 get_time: Callable[[], int],
                 recipe_dic: dict[str, Recipe],
                 price_produce_product_per_unit: dict[str, float]
                 ):
        super().__init__(
            products_max_stock,
            products_min_stock,
            create_product_lambda,
            supply_distribution,
            sale_price_distribution,
            time_restock_distribution,
            get_time
        )

        self.recipe_dic: dict[str, Recipe] = recipe_dic
        """
        Dict de nombre del producto y su receta
        """

        self.price_produce_product_per_unit: dict[str, float] = price_produce_product_per_unit
        """
        Dict de nombre del producto más precio por elaborarlo
        """

    @property
    def get_produce_products(self) -> list[str]:
        """
        Da el nombre de los productos los cuales puede elaborar dándole sus ingredientes

        :return:list[str]
        """
        return list(self.price_produce_product_per_unit.keys())

    def get_price_produce_product_per_unit(self, product_name: str):
        """
        Devuelve el precio de producir un producto dándole
        los ingredientes devuelve -1 si no está el producto
        :param product_name: nombre del producto
        :return:float precio de producir el producto
        """
        if product_name not in self.price_produce_product_per_unit:
            return -1
        return self.price_produce_product_per_unit[product_name]

    def get_product_ingredients(self, product_name: str) -> list[Ingredient]:
        """
        Dado el nombre de un producto el cual dado sus ingredientes se brinda
        el servicio de procesar hasta este producto, devuelve los ingredientes
        :param product_name:
        :return:
        """

        if product_name not in self.recipe_dic:
            raise Exception(f'No se brinda el servicio de procesar el producto:{product_name} en esta empresa ')
        recipe = self.recipe_dic[product_name]
        return recipe.get_ingredients()

    def _check_ingredientes_recipe_are_fine(self, item: Ingredient, product_name, ingredients: List[Product]):
        """
        Chequea que la lista de productos ingredientes es la misma en cantidad que la que tiene la receta
        :param item: el ingrediente a ver
        :param product_name: nombre del producto a elaborar
        :param ingredients: lista de productos ingredientes
        :return:
        """
        ingredient_name = item.get_product_name()
        ingredient_amount = item.get_amount()
        # Busca la lista de ingredientes que tiene ese nombre
        products_ingredients: List[Product] = list(filter(lambda x: x.name == ingredient_name, ingredients))
        if len(products_ingredients) != ingredient_amount:
            raise Exception(
                f'La cantidad de ingredientes que se necesitan para elaborar el producto {product_name} del ingrediente {ingredient_name} es de {ingredient_amount} unidades')

    def _filter_and_remove(self, input_list: list[Product], product_want_name: str, count_of_the_condition: int) -> \
            Tuple[List[Product], List[Product]]:
        """
        Aca dado una lista de productos y la cant y el nombre de estr que se quiere
        devuelve una lista donde ya se quitaron esos elementos de la lista original y
        una lista donde esta esos elementos con esa cant
        :param input_list:lista con todos los ingredientes
        :param product_want_name: nombre del producto a buscar
        :param count_of_the_condition:int cant de producto a querer
        :return:Tupple(lista con los elementos quitados,lista con la cant de productos que queria)
        """

        filtered_list = input_list.copy()
        return_to_continue_list = []
        """Lista para devolver con los ingredientes que no son los del condition"""
        list_filter = []
        """Lista de los productos que se quiere"""

        for item in filtered_list:
            # Si es el nombre del producto que estamos buscando
            # se añade al list_filter siempre que el i<count
            if product_want_name == item.name and len(list_filter) < count_of_the_condition:
                list_filter.append(item)
            else:
                return_to_continue_list.append(item)

        if len(list_filter) != count_of_the_condition:
            raise Exception(
                f'Se queria {count_of_the_condition} del producto {product_want_name} pero se tiene {len(filtered_list)}')
        return return_to_continue_list, list_filter

    def process_new_product_from_his_ingredients(self, product_name: str, ingredients: List[Product]) -> Product:
        """
        Dada los productos ingredientes de un producto, se crea una unidad del producto procesado
        Nota:Cuando se devuelve la unidad de dicho producto la lista se ingredients se deja vacia
        :param product_name:
        :param ingredients:
        :return:
        """
        if product_name not in self.recipe_dic:
            raise Exception(f'No se brinda el servicio de procesar el producto:{product_name} en esta empresa ')

        # Chequear que los ingredientes son los necesarios
        ingredients_recipe = self.get_product_ingredients(product_name)
        for item in ingredients_recipe:
            # Chequea que la cant de productos ingredientes coincida con los de la receta
            self._check_ingredientes_recipe_are_fine(item, product_name, ingredients)

        # Crear el nuevo producto
        recipe = self.recipe_dic[product_name]

        new_product = recipe.create(ingredients)
        # Limpiar la lista de ingredientes
        ingredients.clear()
        return new_product

    def process_a_list_of_new_products_from_his_ingredients(self, product_name: str, ingredients: List[Product],
                                                            count_to_produce: int) -> list[Product]:
        # Lista para retornar con los productos procesados
        temp_return_product_list: list[Product] = []
        lis_ingredients = ingredients
        # Por cada elemento
        if not product_name in self.recipe_dic:
            raise Exception(f'El producto {product_name} no se produce')
        recipe = self.recipe_dic[product_name]
        for _ in range(0, count_to_produce):
            # INgredientres para cada unidad del producto
            temp_ing = []

            for ingredient in recipe.get_ingredients():
                new_lis, ing = self._filter_and_remove(lis_ingredients, ingredient.get_product_name(),
                                                       ingredient.get_amount())

                # Actualizar los ingredientes actuales
                lis_ingredients = new_lis
                # añadir al de producir
                temp_ing += ing

            # Ahora crear el producto
            new_product = self.process_new_product_from_his_ingredients(product_name, temp_ing)
            temp_return_product_list.append(new_product)

        # Dejar la lista de entrada vacia
        ingredients.clear()
        # retornar la lista de productos
        return temp_return_product_list


class WarehouseStockManager(CompanyStockBase):

    @abstractmethod
    def restock(self):
        """
        Se reabastece mágicamente la empresa
        :return: el precio de reabastecerse
        """
        pass
