# %%
from supply_chain.Building.Builder_base import BuilderBase
from supply_chain.Company.stock_manager.manufacturing_stock_manager import *
from supply_chain.Company.stock_manager.store_stock_manager import ShopStockManager
from supply_chain.Company.stock_manager.warehouse_stock_manager import WarehouseStockManager
from supply_chain.products.specific_products.recipes.pizza_recipe import PizzaRecipe

product_name = 'pizza'

import random



class BuildProductorStockManager(BuilderBase):

    def _check(self):
        # Chequear que el min del minimo del del max stock sea mayor= que el minimo
        # del minimo restock
        if not self.min_of_the_max_stock >= self.max_of_the_min_stock:
            msg = (
                f'No se puede crear dado que el minimo valor que puede tener la cant maxima de stock es de {self.min_of_the_max_stock} y la cant maxima que puede tener el minimo restock es de  {self.max_of_the_min_stock}'
            )

            raise Exception(msg)


    def __init__(self,
                 create_product_lambda: dict[str, Callable[[int], list[Product]]],
                 list_products_can_sell_name: list[str],
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],
                 seed:int,
                 min_of_the_max_stock: int = 8,
                 max_of_the_max_stock:int=60,
                 min_of_the_min_stock: int = 1,
                 max_of_the_min_stock: int = 6,

                 min_supply_distribution: int = 1,
                 max_supply_distribution: int = 30,

                 min_price_distribution: float = 0.5,
                 max_price_distribution: float = 2.0,

                 min_time_restock: int = 60 * 60 * 12,
                 max_time_restock: int = 60 * 60 * 24 * 3,


                 ):

        super().__init__(seed=seed)
        # Chequear



        self.create_product_lambda: dict[str, Callable[[int], list[Product]]] = create_product_lambda
        """Lambda para crear el producto"""

        self.list_products_can_sell_name: list[str] = list_products_can_sell_name
        """Lista de productos que puede ofrecer la empresa"""

        self.min_of_the_max_stock: int = min_of_the_max_stock
        """
        Minima cantidad del max stock
        """
        self.max_of_the_max_stock: int = max_of_the_max_stock
        """
        Maxima cant del max stock
        """

        self.min_of_the_min_stock: int = min_of_the_min_stock
        """
        Minima cant del minimo stock
        """

        self.max_of_the_min_stock: int = max_of_the_min_stock
        """
        Maxima cant del minimo stock
        """

        self.min_supply_distribution: int = min_supply_distribution
        """
        Minimo a reabastecer en cada restock
        """

        self.max_supply_distribution: int = max_supply_distribution
        """
        Maximo a reabastecer en cada restock
        """

        self.min_price_distribution: float = min_price_distribution
        """
        Min Price de distribucion
        """
        self.max_price_distribution: float = max_price_distribution
        """
        Max precio de distribucion
        """

        self.min_time_restock: int = min_time_restock
        """
        Minimo tiempo de restock
        """
        self.max_time_restock: int = max_time_restock
        """
        Max tiempo de restock
        """
        self._check()

        self.add_event: Callable[[SimEvent], None] = add_event
        self.get_time: Callable[[], int] = get_time

    def create_products_max_stock(self) -> dict[str, int]:
        dict_return = {}

        for product_name in self.list_products_can_sell_name:
            dict_return[product_name] = self.get_random_int(self.min_of_the_max_stock, self.max_of_the_max_stock)

        return dict_return

    def create_products_min_stock(self) -> dict[str, int]:
        dict_return = {}

        for product_name in self.list_products_can_sell_name:
            dict_return[product_name] = self.get_random_int(self.min_of_the_min_stock, self.max_of_the_min_stock)

        return dict_return

    def create_supply_distribution(self) -> Dict[str, Callable[[], int]]:
        """Devuelve la supply_distribution"""

        def _distribucion():
            return self.get_random_int(self.min_supply_distribution, self.max_supply_distribution)

        dict_return = {}

        for product_name in self.list_products_can_sell_name:
            dict_return[product_name] = _distribucion
        return dict_return

    def create_time_restock_distribution(self) -> Callable[[], int]:

        def _distribution():
            return self.get_random_int(self.min_time_restock, self.max_time_restock)

        return _distribution

    def create_sale_price_distribution(self) -> dict[str, Callable[[], float]]:

        dict_return = {}

        def distribution():
            return self.get_random_float(self.min_price_distribution, self.max_price_distribution)

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




class BuildingManufacterStockManager:

    def __init__(self,
                list_manufactore_products: list[str],
                list_base_products:list[str],
                list_sale_products:list[str],
                create_product_lambda: Dict[str, Callable[[int], List[Product]]],
                get_time: Callable[[], int],
                min_product_amount:int = 100,
                min_stock_random: int = 3000,
                max_stock_random: int = 9000,
                min_price: int = 50,
                max_price: int = 200,
                 distribution_min_supply: int = 1,
                 distribution_max_supply: int = 60
                 ):
        self.list_manufactor_products:list[str]=list_manufactore_products
        """
        Nombre de los productos manufacturados
        """
        self.list_base_products:list[str]=list_base_products
        """
        Nombre de productos base
        """

        self._distribution_min = distribution_min_supply
        """
        Cant de productos que se reponen min en un restock
        """
        self._distribution_max_supply: int = distribution_max_supply
        """
        Cant maxima de productos que se reponen en un restock
        """

        self.products_sale_names = list_sale_products
        """
        Nombre de los productos que se venden
        """
        self.get_time: Callable[[], int] = get_time
        """
        lambda para dar la hora
        """
        self.min_product_amount: int = min_product_amount
        """
        Cant minima de productos que puede haber cuando se crea
        """
        self.min_stock_random: int = min_stock_random
        """
        Es la cota superior para la cant de productos min que hay para hacer restock
        """

        self.max_stock_random: int = max_stock_random
        """
        Cant maxima de stock
        """

        self.min_price: int = min_price
        """
        Precio minimo
        """

        self.max_price: int = max_price
        """
        Precio maximo
        """
        self.create_product_lambda: dict[str, Callable[[int], list[Product]]] = create_product_lambda
    def create_products_max_stock(self)->dict[str, int]:
        dict_return={}

        for i in self.list_manufactor_products:
            if not i in dict_return :
                dict_return[i] = random.randint(self.min_product_amount, self.min_stock_random)
            else:
                continue

        return dict_return

    def create_products_min_stock(self)->dict[str, int]:
        dic = {}

        for i in self.list_manufactor_products:
            if not i in dic :
                dic[i] = random.randint(self.min_product_amount,self.min_stock_random)
            else:
                continue
        return dic

    def create_price_produce_product_per_unit(self)->dict[str, float]:
        dic = {}

        for i in self.list_manufactor_products:
            if not i in dic:
                dic[i] = random.randint(50, 200)
            else:
                continue
        return dic

    def create_recipe_dic(self)-> dict[str, Recipe]:
        dic ={}
        for product in self.list_products:
            dic[product] = PizzaRecipe

        return dic

    def create_time_restock_distribution(self)->Callable[[], int]:
        def distribution():
            return random.randint(1,60)

        return distribution

    def create_sale_price_distribution(self)->dict[str, Callable[[], float]]:

        dict_return = {}

        def func():
            return random.randint(self.min_price, self.max_price)

        for product_name in self.list_manufactor_products:
            dict_return[product_name] = func

        return dict_return

    def create_supply_distribution(self)-> Dict[str, Callable[[], int]]:
        dict_return = {}

        def func():
            return random.randint(self._distribution)

        for product_name in self.list_manufactor_products:
            dict_return[product_name] = func

        return dict_return

    def create_ManufactureStock(self):
        return ManufacturingStock(self.create_products_max_stock(),
                                  self.create_products_min_stock(),
                                  self.create_product_lambda,
                                  self.create_supply_distribution(),
                                  self.create_sale_price_distribution(),
                                  self.create_time_restock_distribution(),
                                  self.get_time,
                                  self.create_recipe_dic(),
                                  self.create_price_produce_product_per_unit())



class BuildWareHouseStockManager(BuilderBase):

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
            dic[product_name] =self.get_random_int(self.min_random, self.max_random)

        return dic

    def _create_random_supply_distribution(self, min: int, max: int) -> Callable[[], int]:

        def _random_supply():
            return self.get_random_int(min, max)

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



class BuilderStoreStockManager(BuilderBase):

    def __init__(self,
                 list_products: list[str],
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],
                 create_product_lambda: dict[str, Callable[[int], list[Product]]],
                 seed: int,
                 # Minimo del minimo stock que se puede tener
                 min_min_stock_random: int = 30,
                 # Maximo del minimo stock que se puede tener
                 max_min_stock_random: int = 90,
                 # Minimo del stock maximo que se puede tener
                 min_max_stock_random: int = 93,
                 # Maximo del stock maximo que se puede tener
                 max_max_stock_random: int = 300,

                 min_price: int = 50,
                 max_price: int = 200,
                 ):
        """
        Creador de tiendas
        :param list_products: list[str] nombre de los productos que venden estas tiendas
        :param add_event:
        :param get_time:
        :param create_product_lambda:dict[str,Callable[[int],list[Product]] llave nombre del producto : Lambda para crear un producto ,
        :param seed: la semilla
        :param min_min_stock_random: minimo del minimo stock para la aleatoriedad
        :param max_min_stock_random: maximo del minimo stock para la aleatoriedad
        :param min_max_stock_random: minimo del maximo stock para la aleatoriedad
        :param max_max_stock_random: maximo del maximo stock para la aleatoriedad
        :param min_price: precio minimo para la aleatoriedad
        :param max_price: precio maximo para la aleatoriedad
        """
        super().__init__(seed)

        self.list_products_names: list[str] = list_products
        """
        Nombre de los productos
        """

        self.min_min_stock_random: int = min_min_stock_random
        """
         Minimo del minimo stock que se puede tener
        """

        self.max_min_stock_random: int = max_min_stock_random
        """
        Maximo del minimo stock que se puede tener
        """

        self.min_max_stock_random: int = min_max_stock_random
        """
         Minimo del stock maximo que se puede tener
        """

        self.max_max_stock_random: int = max_max_stock_random
        """
         Maximo del stock maximo que se puede tener
        """



        """
        Nombre de los productos 
        """
        self.add_event: Callable[[SimEvent], None] = add_event
        self.get_time: Callable[[], int] = get_time

        self.create_product_lambda: dict[str, Callable[[int], list[Product]]] = create_product_lambda
        """
        Dicc que tienen el lamda para crear cada producto
        """

        self.min_price: int = min_price
        """
        Precio minimo
        """
        self.max_price: int = max_price
        """
        Precio maximo
        """

    def _create_dict_from_product_name_to_int_assing_random(self, min_value: int, max_value: int) -> dict[str, int]:
        """
        Crea un diccionario desde el nombre de las llaves hasta un entero que es seleccionado aleatioramente
        :param min_value:
        :param max_value:
        :return:
        """
        dic = {}
        for product_name in self.list_products_names:
            dic[product_name] = self.get_random_int(min_value, max_value)
        return dic

    def _create_price_product(self) -> dict[str, int]:
        return self._create_dict_from_product_name_to_int_assing_random(self.min_price, self.max_price)

    def _create_min_stock_product(self) -> dict[str, int]:
        return self._create_dict_from_product_name_to_int_assing_random(self.min_min_stock_random,
                                                                        self.max_min_stock_random)

    def _create_max_stock_product(self) -> dict[str, int]:
        return self._create_dict_from_product_name_to_int_assing_random(self.min_max_stock_random,
                                                                        self.max_max_stock_random)

    def create_init_product(self) -> dict[str, list[Product]]:
        """
        Fabricar productos iniciales
        :return:
        """
        dic_ret: [str, list[Product]] = {}
        for product_name in self.list_products_names:

            if not product_name in self.create_product_lambda:
                raise Exception(f'El producto {product_name} no está en el diccionario con su lamba para instanciarse')
            fun = self.create_product_lambda[product_name]

            dic_ret[product_name] = fun(self.get_random_int(self.min_min_stock_random, self.min_max_stock_random))
                                                            #Desde el minimo del minimo stock hasta el minimo del maximo stock

        return dic_ret



    def create_ShopStockManager(self):
        return ShopStockManager(
            add_event=self.add_event,
            get_time=self.get_time,
            init_products=self.create_init_product(),
            max_product_stock=self._create_max_stock_product(),
            min_product_stock=self._create_min_stock_product(),
            price_product=self._create_price_product()
        )