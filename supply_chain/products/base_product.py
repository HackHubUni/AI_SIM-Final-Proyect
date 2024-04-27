# from product import Product
# from flavor import Flavor
# from nutritive_properties import NutritiveProperties


# class BaseProduct(Product):
#     """This class represents the products of the simulation"""

#     def __init__(
#         self,
#         name: str,
#         flavor: Flavor,
#         nutritive_properties: NutritiveProperties,
#         initial_quality: float,
#     ) -> None:
#         super().__init__(name)
#         self.flavor: Flavor = flavor
#         self.nutritive_properties: NutritiveProperties = nutritive_properties
#         # TODO: Check if the quality is greater than 0 and less equal than 100
#         self.initial_quality: float = initial_quality
#         """The initial quality of the product"""

#     def get_flavor(self) -> Flavor:
#         return self.flavor

#     def get_nutritive_properties(self) -> NutritiveProperties:
#         return self.nutritive_properties
