from abc import ABC, abstractmethod
from ingredient import Ingredient, Product
from product import *
import numpy as np

class Recipe:
    """This represents a recipe"""

    def __init__(self, name: str, ingredients: set[Ingredient]) -> None:
        super().__init__()
        self.name: str = name
        """The name of the product this recipe creates"""
        self.ingredients: set[Ingredient] = ingredients
        """The set of ingredients of the product"""

    def get_ingredients(self) -> list[Ingredient]:
        """Returns the list of ingredients of the product"""
        return list(self.ingredients)

    def create(self, ingredients: list[Product]) -> Product:
        """This method creates the product given the ingredients.
        The list of the ingredients is a list of products (Note that the if an ingredient is 5 units of apples then in this list you need to add 5 instances of the apple product)
        This method raise an exception if the ingredients are not sufficient with respect to the demand of this recipe
        """
        # TODO: Implement this
        pass

    

class PizzaRecipe(Recipe):
    def __init__(self, name: str, ingredients: set[Ingredient]) -> None:
        super().__init__("pizza", set([Ingredient("dough", 1), Ingredient("tomato_sauce", 1), Ingredient("cheese", 1)]))

    def create(self, ingredients: list[Product]) -> Product:
        if len(ingredients) != 3:
            raise ValueError("The ingredients are not enough to create the pizza")
        for ingredient in ingredients:
            if type(ingredient.get_name()) == Dough:
                dough = ingredient
            elif type(ingredient.get_name()) == TomatoSauce:
                tomato_sauce = ingredient
            elif type(ingredient.get_name()) == Cheese:
                cheese = ingredient
            else:
                raise ValueError("The ingredients are not enough to create the pizza")
        
        return Pizza("pizza", np.median([dough.get_flavor(), tomato_sauce.get_flavor(), cheese.get_flavor()]),np.median([dough.get_nutritive_properties(), tomato_sauce.get_nutritive_properties(), cheese.get_nutritive_properties()]), 100)

class DoughRecipe(Recipe):
    def __init__(self, name: str, ingredients: set[Ingredient]) -> None:
        super().__init__("dough", set([Ingredient("flour", 2), Ingredient("water", 1), Ingredient("salt", 1),Ingredient("yeast", 1), Ingredient("olive_oil", 2)]))  

    def create(self, ingredients: list[Product]) -> Product:
        if len(ingredients) != 7:
            raise ValueError("The ingredients are not enough to create the dough")
        for ingredient in ingredients:
            if type(ingredient.get_name()) == Flour:
                flour = ingredient
            elif type(ingredient.get_name()) == Water:
                water = ingredient
            elif type(ingredient.get_name()) == Salt:
                salt = ingredient
            elif type(ingredient.get_name()) == Yeast:
                yeast = ingredient
            elif type(ingredient.get_name()) == OliveOil:
                olive_oil = ingredient
            else:
                raise ValueError("The ingredients are not enough to create the dough")
        
        return Dough("dough", np.median([flour.get_flavor(), water.get_flavor(), salt.get_flavor(),yeast.get_flavor(),olive_oil.get_flavor()]),np.median([flour.get_nutritive_properties(), water.get_nutritive_properties(), salt.get_nutritive_properties(),yeast.get_nutritive_properties(),olive_oil.get_nutritive_properties()]), 100)
    
class TomatoSauceRecipe(Recipe):
    def __init__(self, name: str, ingredients: set[Ingredient]) -> None:
        super().__init__("tomato_sauce", set([Ingredient("tomato", 2), Ingredient("olive_oil", 1), Ingredient("salt", 1),Ingredient("pepper", 1), Ingredient("onion", 1)]))

    def create(self, ingredients: list[Product]) -> Product:
        if len(ingredients) != 5:
            raise ValueError("The ingredients are not enough to create the tomato sauce")
        for ingredient in ingredients:
            if type(ingredient.get_name()) == Tomato:
                tomato = ingredient
            elif type(ingredient.get_name()) == OliveOil:
                olive_oil = ingredient
            elif type(ingredient.get_name()) == Salt:
                salt = ingredient
            elif type(ingredient.get_name()) == Pepper:
                pepper = ingredient
            elif type(ingredient.get_name()) == Onion:
                onion = ingredient
            else:
                raise ValueError("The ingredients are not enough to create the tomato sauce")
        
        return TomatoSauce("tomato_sauce", np.median([tomato.get_flavor(), olive_oil.get_flavor(), salt.get_flavor(),pepper.get_flavor(),onion.get_flavor()]),np.median([tomato.get_nutritive_properties(), olive_oil.get_nutritive_properties(), salt.get_nutritive_properties(),pepper.get_nutritive_properties(),onion.get_nutritive_properties()]), 100)
    
class CheeseRecipe(Recipe):
    def __init__(self, name: str, ingredients: set[Ingredient]) -> None:
        super().__init__("cheese", set([Ingredient("milk", 2), Ingredient("salt", 1), Ingredient("rennet", 1)]))

    def create(self, ingredients: list[Product]) -> Product:
        if len(ingredients) != 3:
            raise ValueError("The ingredients are not enough to create the cheese")
        for ingredient in ingredients:
            if type(ingredient.get_name()) == Milk:
                milk = ingredient
            elif type(ingredient.get_name()) == Salt:
                salt = ingredient
            elif type(ingredient.get_name()) == Rennet:
                rennet = ingredient
            else:
                raise ValueError("The ingredients are not enough to create the cheese")
        
        return Cheese("cheese", np.median([milk.get_flavor(), salt.get_flavor(), rennet.get_flavor()]),np.median([milk.get_nutritive_properties(), salt.get_nutritive_properties(), rennet.get_nutritive_properties()]), 100)