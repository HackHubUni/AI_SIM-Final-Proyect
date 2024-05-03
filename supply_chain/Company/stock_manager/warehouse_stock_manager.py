import random

import numpy as np

from stock_manager import *
from supply_chain.events.SimEventCompany import WarehouseRestockSimEvent
from supply_chain.products.product import Product


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

        self._product_price_stock: dict[str, float] = {}

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
        """
        Comprueba que se tenga los mismos nombres

        :param companies_name:
        :return:
        """

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
        """
        Chequea cuando se crea la instancia que las llaves de los dicc son correctos
        :return:
        """
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

    def get_cost_by_product_and_unit_time(self,product_name:str):

        if product_name not in self._product_price_stock:
            return -1

        return self._product_price_stock[product_name]

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

        # Ver el costo
        # TODO:Añadir a las estadísticas
        cost_lambda = company_cost_product_distribution[product_name]
        # Coste en este reabastecimiento
        cost_now = cost_lambda()

        self._product_price_stock[product_name]=cost_now

        # TODO: ACAAAAAAAAAAAAAAAAAAA
        cost_price = cost_now * count_want

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

        matrix_dic = self._stock_by_company[matrix_name]
        if not product_name in matrix_dic:
            raise Exception(f'La compañia matriz {matrix_dic} no tiene unidades del producto {product_name} en stock')

        lis = [product.get_quality(self.time) for product in matrix_dic[product_name]]
        # Retornar el promedio de los productos
        return np.mean(lis)

    def _get_dicc_stock_by_company(self, matrix_name: str) -> dict[str, list[Product]]:
        """
        Devuelve el dicc que tiene una empresa matriz en específico
        :param matrix_name: nombre de la empresa matriz
        :return:
        """

        if matrix_name in self._stock_by_company:

            return self._stock_by_company[matrix_name]

        else:
            new_dicc: dict[str, list[Product]] = {}
            self._stock_by_company[matrix_name] = new_dicc
            return new_dicc

    def _add_product_to_and_check_balance_it_s_ok(self
                                                  , product_instance: Product, dicc: dict[str, list[Product]]) -> dict[
        str, list[Product]]:
        """
        Toma la instancia de un producto y tiene completa la lógica
        de añadir ese producto al stock de esa tienda
        :param product_instance:
        :param dicc:
        :return:
        """

        product_name = product_instance.name
        # Si el producto no esta contemplado dentro de lo que se puede guardar en la tienda
        if not product_name in self.product_max_stock:
            raise Exception(f'El producto {product_name} no está en el dicc de max_stock')

        # Stock maximo que se puede tener de este producto
        max_stock = self.product_max_stock[product_name]

        # Si no hay un producto en específico

        if not product_name in dicc:
            dicc[product_name] = []

        # Darme la lista de productos
        produc_list = dicc[product_name]

        # Cant de productos en el stock de ese tipo ahora

        count_stock_now = len(produc_list)

        assert count_stock_now <= max_stock, f'La cant de productos en la lista {count_stock_now} es mayor que el max_stock{max_stock}'

        if count_stock_now == max_stock:
            produc_list = self.delete_firts_n_worts_products_in_quality(produc_list, 1)

        produc_list.append(product_instance)

        # Reordear la lista random
        random.shuffle(produc_list)

        dicc[product_name] = produc_list

        return dicc

    def add_products(self, matrix_name: str, list_Products: list[Product]):
        # Tomar el stock de esa compañia
        company_stock_dicc = self._get_dicc_stock_by_company(matrix_name)

        # Por cada producto guardarlos en sus stock
        for product in list_Products:
            self._add_product_to_and_check_balance_it_s_ok(product, company_stock_dicc)

    def is_product_in_this_company_subStorage(self, matrix_name: str, product_name: str) -> bool:

        if not matrix_name in self._stock_by_company:
            return False

        dict_company = self._stock_by_company[matrix_name]
        if not product_name in dict_company:
            return False

        lis_product = dict_company[product_name]

        if len(lis_product) < 1:
            return False

        return True

    def get_list_products_by_company(self, matrix_name: str, product_name: str):
        if not matrix_name in self._stock_by_company:
            return []

        dict_company = self._stock_by_company[matrix_name]
        if not product_name in dict_company:
            return []

        lis_product = dict_company[product_name]

        if len(lis_product) < 1:
            return []
        return_list = lis_product[:1]
        new_list = lis_product[1:]
        dict_company = new_list
        return lis_product[0:]
