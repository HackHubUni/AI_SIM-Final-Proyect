import unittest
from recipe import *
from ingredient import *
from product import *

class TestRecipe(unittest.TestCase):
    def test_pizza_recipe(self):
        # Create ingredients
        dough = Dough("dough", 5, 10, 100)
        tomato_sauce = TomatoSauce("tomato_sauce", 3, 8, 100)
        cheese = Cheese("cheese", 4, 9, 100)
        
        # Create pizza recipe
        pizza_recipe = PizzaRecipe("pizza", set([Ingredient("dough", 1), Ingredient("tomato_sauce", 1), Ingredient("cheese", 1)]))
        
        # Create pizza using the recipe
        pizza = pizza_recipe.create([dough, tomato_sauce, cheese])
        
        # Check if the pizza is created correctly
        self.assertEqual(pizza.get_name(), "pizza")
        self.assertEqual(pizza.get_flavor(), 4)
        self.assertEqual(pizza.get_nutritive_properties(), 9)
        self.assertEqual(pizza.get_quantity(), 100)
    
    def test_dough_recipe(self):
        # Create ingredients
        flour = Flour("flour", 2, 5, 100)
        water = Water("water", 1, 3, 100)
        salt = Salt("salt", 1, 2, 100)
        yeast = Yeast("yeast", 1, 4, 100)
        olive_oil = OliveOil("olive_oil", 2, 6, 100)
        
        # Create dough recipe
        dough_recipe = DoughRecipe("dough", set([Ingredient("flour", 2), Ingredient("water", 1), Ingredient("salt", 1),Ingredient("yeast", 1), Ingredient("olive_oil", 2)]))
        
        # Create dough using the recipe
        dough = dough_recipe.create([flour, water, salt, yeast, olive_oil])
        
        # Check if the dough is created correctly
        self.assertEqual(dough.get_name(), "dough")
        self.assertEqual(dough.get_flavor(), 2)
        self.assertEqual(dough.get_nutritive_properties(), 4)
        self.assertEqual(dough.get_quantity(), 100)
    
    def test_tomato_sauce_recipe(self):
        # Create ingredients
        tomato = Tomato("tomato", 2, 6, 100)
        olive_oil = OliveOil("olive_oil", 1, 3, 100)
        salt = Salt("salt", 1, 2, 100)
        pepper = Pepper("pepper", 1, 4, 100)
        onion = Onion("onion", 1, 5, 100)
        
        # Create tomato sauce recipe
        tomato_sauce_recipe = TomatoSauceRecipe("tomato_sauce", set([Ingredient("tomato", 2), Ingredient("olive_oil", 1), Ingredient("salt", 1),Ingredient("pepper", 1), Ingredient("onion", 1)]))
        
        # Create tomato sauce using the recipe
        tomato_sauce = tomato_sauce_recipe.create([tomato, olive_oil, salt, pepper, onion])
        
        # Check if the tomato sauce is created correctly
        self.assertEqual(tomato_sauce.get_name(), "tomato_sauce")
        self.assertEqual(tomato_sauce.get_flavor(), 2)
        self.assertEqual(tomato_sauce.get_nutritive_properties(), 4)
        self.assertEqual(tomato_sauce.get_quantity(), 100)
    
    def test_cheese_recipe(self):
        # Create ingredients
        milk = Milk("milk", 2, 6, 100)
        salt = Salt("salt", 1, 2, 100)
        rennet = Rennet("rennet", 1, 4, 100)
        
        # Create cheese recipe
        cheese_recipe = CheeseRecipe("cheese", set([Ingredient("milk", 2), Ingredient("salt", 1), Ingredient("rennet", 1)]))
        
        # Create cheese using the recipe
        cheese = cheese_recipe.create([milk, salt, rennet])
        
        # Check if the cheese is created correctly
        self.assertEqual(cheese.get_name(), "cheese")
        self.assertEqual(cheese.get_flavor(), 2)
        self.assertEqual(cheese.get_nutritive_properties(), 4)
        self.assertEqual(cheese.get_quantity(), 100)

if __name__ == '__main__':
    unittest.main()