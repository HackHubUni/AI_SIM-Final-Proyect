from supply_chain.Comunicator import BuyOrderMessage
from supply_chain.Mensajes.Mensajes_de_dar_el_precio_y_cant_a_la_matriz import ResponseOfertProduceProductMessage
from supply_chain.products.ingredient import Ingredient
from supply_chain.products.product import Product


class RecipeGestor:

    def start(self):
        for ingredient in self.list_ingredientes:
            product_name = ingredient.get_product_name()
            self.dic_product_ingredient_instance[product_name] = []
            self.dict_ingredient_by_name[product_name] = ingredient

    def __init__(self,
                 list_ingredientes: list[Ingredient],
                 buy_order: BuyOrderMessage,
                 firts_offer: ResponseOfertProduceProductMessage
                 ):

        self.buy_order: BuyOrderMessage = buy_order
        self.firts_offer: ResponseOfertProduceProductMessage = firts_offer

        self.list_ingredientes: list[Ingredient] = list_ingredientes

        self.dict_ingredient_by_name: dict[str, Ingredient] = {}

        self.dic_product_ingredient_instance: dict[str, list[Product]] = {}

        self.start()

    def add_ingredient(self, ingrediente_product: Product) -> bool:
        product_name = ingrediente_product.get_name()
        if not product_name in self.dic_product_ingredient_instance:
            raise Exception(f'El producto {product_name} no esta en el diccionario de ingredientes')

        lis = self.dic_product_ingredient_instance[product_name]
        ingredient = self.dict_ingredient_by_name[product_name]
        if len(lis) >= ingredient.get_amount():
            # Es que se cumplio la resticcion y por tanto no se puede llenar

            return False

        lis.append(ingrediente_product)
        return True

    def get_products(self) -> list[Product]:
        lis = []
        for key in self.dic_product_ingredient_instance.keys():
            lis.extend(self.dic_product_ingredient_instance[key])
        return lis

    def add_list_ingredient(self, ingredient_list_product: list[Product]):
        for i in ingredient_list_product:
            self.add_ingredient(i)

    def is_already_the_recipe(self) -> bool:

        """Dice si ya la receta se puede mandar a transformar en producto"""
        for product_name in self.dic_product_ingredient_instance.keys():
            lis = self.dic_product_ingredient_instance[product_name]
            recipe = self.dict_ingredient_by_name[product_name]

            if len(lis) != recipe.get_amount():
                # Si en algun momento algun producto falta por llenarse
                return False

        return True
