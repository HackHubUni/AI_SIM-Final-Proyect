import json
import google.generativeai as genai
from dto_InfoCompany import Dto_InfoCompany

# Configure API Key
GOOGLE_API_KEY = "AIzaSyDKZl8gFeDs6X0draN3nd3kV5Se0l1FCLg"
model = genai.GenerativeModel('gemini-pro')
genai.configure(api_key=GOOGLE_API_KEY)


def str_supplier(product_name,supplier_name,product_quality,trust_level,product_cost):
    str_supp = f'''- Producto: {product_name}
    * {supplier_name}: 
        * Calidad del producto:{product_quality}/10,
        * Nivel de confianza: {trust_level}/10,
        * Precio: ${product_cost}'''
    return str_supp

def str_lost_customers(shop_name,n_product):
    str_lost = f'''- {shop_name}:
                        * Clientes perdidos:{n_product}'''


def str_botton_food_quality(shop_name,quality):
    str_lost = f'''- {shop_name}:
                        * Calidad de la comida:{quality}/10'''



def create_prompt(info:Dto_InfoCompany):

    
    str_top_suppliers = ""
    str_bottom_suppliers = ""
    str_customers = ""
    str_bottom_food = ""

    for product_name in info.suppliers.keys():
        dict_top_suppliers = info.get_top_suppliers(product_name, 3)
        for (supplier_name, product_quality, trust_level, product_cost) in dict_top_suppliers:
            str_top_suppliers += f"\n{str_supplier(product_name,supplier_name, product_quality, trust_level, product_cost)}"

    for product_name in info.suppliers.keys():
        dict_bottom_suppliers = info.get_top_suppliers(product_name, 3, False)
        for (supplier_name, product_quality, trust_level, product_cost) in dict_bottom_suppliers:
            str_bottom_suppliers += f"\n{str_supplier(product_name,supplier_name, product_quality, trust_level, product_cost)}"

        for (shop_name,n_product) in info.get_top_lost_customers(3):
            str_customers += f'''\n {str_lost_customers(shop_name,n_product)}'''


    for (shop_name,n_product) in info.get_botton_food_quality(3):
        str_bottom_food += f'''\n {str_lost_customers(shop_name,quality)}'''
    
    prompt:str = f'''
Dado el siguiente reporte:
# Balance General
- Empresa: FastFood
- Ganancias Totales: ${info.total_earnings}
- Gastos Totales: ${info.total_expenses}
# Distribución de Gastos:
- Costo de Productos: ${info.products_costs}
- Costo de Transporte y Logístico: ${info.transportation_costs}
- Pérdidas por Sobrecostos: ${info.overcost_losses}

# Estrategias para optimizar resultados:

### Mejores Proveedores para cada tipo de Producto:
\n {str_top_suppliers}
### Peores Proveedores para cada tipo de Producto:
\n {str_bottom_suppliers}
### Tiendas con Mayor Pérdida de Clientes:
\n {str_customers}
### Peores Tiendas en Calidad de Comida:
\n {str_bottom_food}

---
---
---

Dado el informe anterior, genera un nuevo informe basado en los datos proporcionados, con el objetivo de brindar conclusiones, análisis y recomendaciones para mejorar la situación actual de la empresa y facilitar la toma de decisiones del CEO.

---
---
---'''
    return prompt


def load_knowledge_base(json_file):
    with open(json_file, "r") as file:
        knowledge_base = json.load(file)
    return knowledge_base

# Function to ask questions to the language model
def gen_report(prompt):
    response = model.generate_content(prompt)
    return response.text


