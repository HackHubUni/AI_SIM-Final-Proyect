from dto_InfoCompany import Dto_InfoCompany
from genai_api import gen_report,create_prompt
# Utilizando los métodos add para rellenar la información del informe en la instancia info


info:Dto_InfoCompany = Dto_InfoCompany()


# Agregar balance general
info.add_balance_general(10000, 5000)

# Agregar costo del producto
info.add_product_cost(2000)

# Agregar costo de transporte
info.add_transportation_cost(500)

# Agregar pérdidas por sobreprecio
info.add_overcost_losses(100)

# Agregar proveedores
info.add_supplier("Producto A", "Proveedor 1", 8, 9, 100)
info.add_supplier("Producto A", "Proveedor 2", 7, 8, 120)
info.add_supplier("Producto B", "Proveedor 1", 9, 9, 150)
info.add_supplier("Producto B", "Proveedor 2", 6, 7, 130)

# Agregar clientes perdidos
info.add_store_lost_customers("Tienda 1", 10)
info.add_store_lost_customers("Tienda 2", 5)
info.add_store_lost_customers("Tienda 3", 8)

# Agregar calidad de comida en la tienda
info.add_store_food_quality("Tienda 1", 4)
info.add_store_food_quality("Tienda 2", 6)
info.add_store_food_quality("Tienda 3", 9)

report = gen_report(create_prompt(info))
print(report)