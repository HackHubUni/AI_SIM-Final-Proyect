from supply_chain.Building.Builder_base import *
from supply_chain.products.specific_products.base_products.pizza_base_products import *
from supply_chain.products.specific_products.manufactured_products.pizza import Pizza


class ExampleBuilderProduct(BuilderBase):
    def __init__(self, seed: int):
        super().__init__(seed)

    def _finals_products_lambda(self):
        def get_pizzas(count: int):
            return [Pizza(self.get_random_float(1, 100)) for _ in range(count)]

        return get_pizzas

    def get_finals_products_names(self)->list[str]:
        return list(self.create_dict_final_products().keys())

    def create_dict_final_products(self):
        """
        Devuelve el diccionario con los productos manufacturados o finales
        :return:
        """
        return {Pizza.get_the_name(): self._finals_products_lambda()}

    def create_dict_base_products(self):
        """
        Devuelve un diccionario con los productos bases como nombnre y sus lambdas para crear
        :return:
        """
        dict_ret = {}

        dict_ret[Cheese.get_the_name()] = lambda x: [Cheese(self.get_random_int(1, 100)) for _ in range(x)]
        dict_ret[TomatoSauce.get_the_name()] = lambda x: [TomatoSauce(self.get_random_int(1, 100)) for _ in range(x)]
        dict_ret[Salt.get_the_name()] = lambda x: [Salt(self.get_random_int(1, 100)) for _ in range(x)]
        dict_ret[PizzaDough.get_the_name()] = lambda x: [Cheese(self.get_random_int(1, 100)) for _ in range(x)]

        return dict_ret

    def get_list_base_products_names(self)->list[str]:
        return list(self.create_dict_base_products().keys())




class BuilderProduct(BuilderBase):
    def __init__(self, seed: int):
        super().__init__(seed)

    def _create_Flavor(self):
        return Flavor(
            sweet=self.get_random_float(1, 10),
            salty=self.get_random_float(1, 10),
            acid=self.get_random_float(1, 10),
            bitter=self.get_random_float(1, 10),
            spicy=self.get_random_float(1, 10)
        )

    def _create_nutritive(self):
        return NutritiveProperties(fat=self.get_random_float(1, 10),
                                   carbohydrates=self.get_random_float(1, 10),
                                   proteins=self.get_random_float(1, 10))

    def create_products(self, amount: int, product_name: str) -> List[Product]:
        return [Product(product_name, self._create_Flavor(), self._create_nutritive(), self.get_random_float(1, 100))
                for i in range(amount)]

    def get_lambda(self, product_name):
        def lam(count: int):
            return self.create_products(count, product_name)

        return lam
    def create_product_lambda_dict(self, product_names: List[str]) -> Dict[str, Callable[[int], List[Product]]]:

        dict_ret = {}

        for product_name in product_names:
            dict_ret[product_name] = self.get_lambda(product_name)

        return dict_ret





if __name__=="__main__":
    pr = BuilderProduct(123).create_product_lambda_dict(['Pizza', 'Cerveza', 'Papas'])
    pizza = pr['Papas']

    pizza_int = pizza(1)

    print(pizza_int)
    my_priza = pizza_int[0]
    print(my_priza.name, my_priza.get_name())

    print()
