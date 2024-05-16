from supply_chain.Company.stock_manager.productor_stock_manager import *
from supply_chain.products.ingredient import Ingredient
from supply_chain.products.recipe import Recipe


class ManufacturingStock(ProductorCompanyStock):
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
