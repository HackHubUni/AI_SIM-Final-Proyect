import copy
import random
from supply_chain.events.SimEventCompany import CompanyRestockSimEvent, WarehouseRestockSimEvent
from supply_chain.products.ingredient import Ingredient
from supply_chain.products.product import Product
from typing import Callable, Dict, List, Any, Tuple
from abc import ABC, abstractmethod, abstractproperty
import numpy as np
from supply_chain.products.recipe import Recipe
from supply_chain.sim_event import SimEvent


class BaseCompanyReStockException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class CompanyStockBase(ABC):

    def __init__(self,
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

    @property
    def time(self) -> int:
        """
        Da el tiempo actual
        :return:
        """
        return self.get_time()

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

        super().__init__(add_event=add_event, get_time=get_time)
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

    def get_average_quality_products(self, product_name: str):

        if not product_name in self._stock:
            raise Exception(f"El producto {product_name} no esta en stock")
        # Se rellena una lista con todos las calidades de las instancias del producto
        # En este momento
        temp = [product.get_quality(self.time) for product in self._stock[product_name]]
        # Retornar el promedio
        return np.mean(temp) if temp else 0


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

    def __init__(self,
                 product_max_stock: dict[str, int],
                 company_product_count_supply_magic_distribution: dict[str, dict[str, Callable[[], int]]],
                 company_product_time_count_supply_magic_distribution: dict[str, dict[str, Callable[[], int]]],
                 company_product_price_supply_magic_distribution: dict[str, dict[str, Callable[[], float]]],
                 create_product_lambda: Dict[str, Callable[[int], List[Product]]],
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int]):
        super().__init__(add_event=add_event,
                         get_time=get_time)

        self.product_max_stock: dict[str, int] = product_max_stock
        """Por producto la capacidad máxima de este en el almacén"""

        self.company_product_price_supply_magic_distribution: dict[
            str, dict[str, Callable[[], float]]] = company_product_price_supply_magic_distribution
        """Por cada matriz:(producto : lambda con el precio del producto en ese restock))"""

        self.company_product_count_supply_magic_distribution: dict[
            str, dict[str, Callable[[], int]]] = company_product_count_supply_magic_distribution
        """Por compañía :( producto : la función que devuelve cuando producto se debe reabastecer
            mágicamente en ese momento)
        """
        self.company_product_time_count_supply_magic_distribution: dict[
            str, dict[str, Callable[[], int]]] = company_product_time_count_supply_magic_distribution
        """
        Por compañía :( producto : la funcion dice cuando debe reabastecerse la proxima vez:
        time actual + lo que de ese lambda)
        
        """

        self.create_product_lambda: Dict[str, Callable[[int], List[Product]]] = create_product_lambda
        """
        Guarda el producto, su lambda a crear, cada vez se llame devuelve una lista con los productos se le pasa la cant a 
         producir como un entero count
        """

        # Chqueaer
        self._check()

        # Locales
        self._stock_by_company: dict[str, dict[str, list[Product]]] = {}
        """Diccionario que por cada matrix que tenga algo guardado algo aca"""

    def _check_names(self):
        set_company_product_time_count_supply_magic_distribution = set(
            self.company_product_time_count_supply_magic_distribution.keys())
        set_company_product_count_supply_magic_distribution = set(
            self.company_product_count_supply_magic_distribution.keys())
        if not set_company_product_count_supply_magic_distribution == set_company_product_time_count_supply_magic_distribution:
            raise BaseCompanyReStockException(f'Existen nombres de compañias que no coinciden')

    def _check_companies_name(self, company_name: str):
        """
        Comprueba que todos los dicc donde esten involucados los nombres de las
        compañias tengan esta compañia
        :param company_name:
        :return:
        """

        if not company_name in self.company_product_time_count_supply_magic_distribution:
            raise Exception(
                f'La compania {company_name} no esta en el diccionario company_time_count_supply_magic_distribution')

        if not company_name in self.company_product_count_supply_magic_distribution:
            raise Exception(
                f'La compania {company_name} no esta en el diccionario company_product_count_supply_magic_distribution ')

    def _check_start_products_in_companies(self, companies_name):

        products_names = list(self.company_product_count_supply_magic_distribution[companies_name].keys())
        # TOmar la cant que se quiere suministrar magicamente en cada restock y ver si tiene todos los productos
        product_count_supply_magical_distribution = self.company_product_count_supply_magic_distribution[companies_name]
        # TOmar si en esta empresa todos los productos tiene  tiempo de restock en esta empresa
        product_time_count_supply_magic_distribution = self.company_product_time_count_supply_magic_distribution[
            companies_name]
        for product in products_names:
            # comprobar que producto se puede crear
            if not product in self.create_product_lambda:
                raise Exception(f'El producto {product} no esta en create_product_lambda')

            # Comprobar que por producto hay un stock maximo

            if not product in self.product_max_stock:
                raise Exception(f'El producto {product} no esta en product_max_stock')

            # Comprobar que por producto hay una cant deseada a reabastecer por restock
            if not product in product_count_supply_magical_distribution:
                raise Exception(f'El producto {product} no esta en company_product_count_supply_magic_distribution')

            # Comprotbar que este el producto en la distribucion magica
            if not product in product_time_count_supply_magic_distribution:
                raise Exception(
                    f'El producto {product} no esta en company_product_time_count_supply_magic_distribution')

        # Testing the sets:

        set_create_product_lambda = set(self.create_product_lambda.keys())
        set_product_max_stock = set(self.product_max_stock.keys())
        set_product_count_supply_magical_distribution = set(product_count_supply_magical_distribution.keys())
        set_product_time_count_supply_magic_distribution = set(product_time_count_supply_magic_distribution.keys())
        # Si alguno no es igual lanzar exception
        if not (
                set_create_product_lambda == set_product_max_stock
                and
                set_create_product_lambda == set_product_count_supply_magical_distribution
                and
                set_create_product_lambda == set_product_time_count_supply_magic_distribution
        ):
            raise BaseCompanyReStockException(f'No coincide el nombre de algun producto en los dict')

    def _check(self):
        # Chequear los  nombres
        self._check_names()
        # TOmar las empresas
        companies_name: list[str] = list(self.company_product_count_supply_magic_distribution.keys())
        for company_name in companies_name:
            # Chequear que coinciden los nombres de las compañías
            self._check_companies_name(company_name)
            # Chequer que coinciden los productos para cada compañía osea que no haya uno que no tenga
            # distribucion o cant máxima
            self._check_start_products_in_companies(companies_name)

    def get_quality_of_a_product_instance_now(self, product: Product) -> float:
        """Devuelve la calidad de un producto en este mismo momento"""
        return product.get_quality(self.time)

    def delete_firts_n_worts_products_in_quality(self, list_product: list[Product], count: int) -> list[Product]:
        """
        Toma la lista de productos y quita los count peores en calidad
        :param list_product: toma la lista original de instancia de producto
        :param count: La cant de productos a eliminar
        :return: Una nueva lista con los sin los count peores productos que además ha sido reordenada random
        """
        # lanzar exepcion si el count es menor que la cant que hay en la lista
        if count > len(list_product):
            raise BaseCompanyReStockException(
                f'No se puede quitar los {count} primeros peores si solo se tiene {len(list_product)}')
        # Ordenar la lista de menor a mayor de acuerdo a su calidad actual
        temp_list = sorted(list_product, key=self.get_quality_of_a_product_instance_now)

        # Quitar del inicio los count peores productos
        new_list = temp_list[count:]
        # Reorganizar random los productos restantes
        random.shuffle(new_list)

        return new_list

    def _add_new_restock_product_in_a_company_event(self, company_name: str, product_name: str):
        # Añadir evento
        # Ver cuando toca el proximo reinventario
        company_time = self.company_product_time_count_supply_magic_distribution[company_name]
        product_time_lambda = company_time[product_name]
        next_time = self.time + product_time_lambda()
        event = WarehouseRestockSimEvent(time=next_time,
                                         priority=0,
                                         execute=self._restock_product_in_a_company,
                                         product_name=product_name,
                                         company_name=company_name)
        self.add_event(event)

    def _restock_product_in_a_company(self, company_name: str, product_name: str):
        """
        Dado una compañia y un producto reabastece de este
        si cuando se hace restock magico hay mas productos que los que se pueden reabastecer
        pues se toma la cant faltantes y en el stock de esa empresa y el producto
        se eliminan los peores y se añaden los nuevos
        Esta función se encarga tb de llamar al sgt evento de reabastecer ese producto de
        esa empresa matriz
        :param company_name:
        :param product_name:
        :return:
        """

        # El stock de la compañia
        company_stock = self._stock_by_company[company_name]
        # Distribucion de cant de alimentos en la compañia
        count_supply_distrubution = self.company_product_count_supply_magic_distribution[company_name]

        company_cost_product_distribution = self.company_product_price_supply_magic_distribution[company_name]

        # Lista de productos inicialmente vacia por si no hay producto en el stock
        lis_product_stock = []

        # Si no esta el producto en el dicc añadirlo
        count_in_stock: int = 0
        max_in_stock = self.product_max_stock[product_name]
        if not product_name in company_stock:
            company_stock[product_name] = []
        else:
            # Lista de las instancias del producto en stock
            lis_product_stock = company_stock[product_name]
            # Si no esta en el stock
            count_in_stock = len(lis_product_stock)

            # Si lo que hay en stock es lo máximo que debe ver se termina aca el analysis
            if count_in_stock == max_in_stock:
                return

        # Que me de la cant de producto a querer
        # Pero como se quitan los n peores entonces siempre se compra en realidad el count_want

        count_want: int = count_supply_distrubution[product_name]()

        if count_want + count_in_stock > max_in_stock:
            # Esto es cuanto realmente se deberia comprar

            # Si no cabe tods lo que se va a rellenar en el stock
            need_buy = max_in_stock - count_in_stock
            # TODO:Añadir estadísticas la cant que no se acepta
            quantity_not_accepted = count_want - need_buy

            # Comprobar que no se eliminen mas de los que hay en stock
            assert count_in_stock < quantity_not_accepted, f'En la empresa {company_name} producto {product_name} se quiere quitar los {quantity_not_accepted} peores productos pero en stock hay {count_in_stock}'
            # ELiminar la cant de desechar peores
            # Actualizar los productos en stock
            lis_product_stock = self.delete_firts_n_worts_products_in_quality(lis_product_stock, quantity_not_accepted)

        # Generar los productos y añadirlos
        create_product = self.create_product_lambda[product_name]
        # Crear esta cant nuevos productos osea los count_want
        # pq en caso de a ver desechado productos ya caben el count_want
        new_products = create_product(count_want)
        lis_product_stock = lis_product_stock + new_products
        # Reordenar la lista
        random.shuffle(lis_product_stock)

        # Ver el cosot
        # TODO:Añadir a las estadísticas
        cost_lambda = company_cost_product_distribution[product_name]
        # Coste en este reabastecimiento
        cost_price = cost_lambda() * count_want

        # Añadir la nueva lista
        company_stock[product_name] = lis_product_stock
        self._stock_by_company[company_name] = company_stock

        # Crear el nuevo evento
        self._add_new_restock_product_in_a_company_event(company_name=company_name,
                                                         product_name=product_name)

    def restock(self):
        """
        Se reabastece mágicamente la empresa
        OJO:Esto es solo para llamar el inicio en el start
        :return: el precio de reabastecerse
        """
        companies_name = list(self.company_product_count_supply_magic_distribution.keys())
        products_name = list(self.product_max_stock.keys())
        # Ir por cada compañía
        for company_name in companies_name:
            if not company_name in self._stock_by_company:
                # Si no esta la empresa se añade al diccionario
                self._stock_by_company[company_name] = {}
            # Ir por cada producto
            for product_name in products_name:
                # HAcer el reabastecimineto de ese producto
                self._restock_product_in_a_company(company_name, product_name)

    def get_average_quality_products_by_matrix_company(self, matrix_name: str, product_name: str):

         if not matrix_name in self._stock_by_company:
             raise Exception(f'La compañia matriz {matrix_name} no tiene ningun stock en este almacen')

         matrix_dic=self._stock_by_company[matrix_name]
         if not product_name in matrix_dic:
             raise Exception(f'La compañia matriz {matrix_dic} no tiene unidades del producto {product_name} en stock')

         lis=[product.get_quality(self.time) for product in matrix_dic[product_name]]
         #Retornar el promedio de los productos
         return np.mean(lis)



