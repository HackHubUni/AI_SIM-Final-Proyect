from typing import Dict, List, Tuple
class Dto_InfoCompany:
    def __init__(self,total_earnings = None,total_expenses = None,
                product_cost = None,transportation_costs = None,overcost_losses = None,
                suppliers =  None,store_lost_customers = None , store_food_quality = None ):

        self.total_earnings: int = total_earnings if total_earnings is not None else 0 
        self.total_expenses: int = total_earnings if total_earnings is not None else 0 

        self.products_costs: int =  product_cost if product_cost is not None else 0
        self.transportation_costs: int = transportation_costs if transportation_costs is not None else 0
        self.overcost_losses: int = overcost_losses if overcost_losses is not None else 0

        self.suppliers: Dict[str, Dict[str,Tuple[int, int, int]]] = suppliers if suppliers is not None else {}
    
        self.store_lost_customers: Dict[str, int] = store_lost_customers if store_lost_customers is not None else {}
        self.store_food_quality: Dict[str, int] = store_food_quality if store_food_quality is not None else {}


    def add_balance_general(self, total_earnings: int, total_expenses: int):
        self.total_earnings = total_earnings
        self.total_expenses = total_expenses

    def add_product_cost(self,product_cost: int):
        self.products_costs = product_cost
    
    def add_transportation_cost(self, transportation_cost: int):
        self.transportation_cost = transportation_cost

    def add_overcost_losses(self, overcost_losses: int):
        self.overcost_losses = overcost_losses

    def add_supplier(self, product_name: str, supplier_name:str,product_quality:int,trust_level:int,product_cost:int):
        if product_name not in self.suppliers:
            self.suppliers[product_name] = {supplier_name:(product_quality,trust_level,product_cost)}
        else:
            self.suppliers[product_name][supplier_name] = (product_quality,trust_level,product_cost)
        
        
    def add_store_lost_customers(self, store_name: str, lost_customers: int):
        self.store_lost_customers[store_name] = lost_customers

    def add_store_food_quality(self, store_name: str, food_quality: int):
        self.store_food_quality[store_name] = food_quality
        

    def get_top_suppliers(self, product_name: str, num_entries: int) -> List[Tuple[str, int, int, int]]:
        if product_name in self.suppliers:
            suppliers = self.suppliers[product_name]

            sorted_suppliers = sorted(suppliers.items(), key=lambda x: x[1][0] + x[1][1] - x[1][2] , reverse=True)
            return [(k, *v) for k, v in sorted_suppliers[:num_entries]]
        return []

    def get_top_lost_customers(self, num_entries: int) -> List[Tuple[str, int]]:
        sorted_customers = sorted(self.store_lost_customers.items(), key=lambda x: x[1], reverse=True)
        return sorted_customers[:num_entries]
    
    def get_top_food_quality(self, num_entries: int) -> List[Tuple[str, int]]:
        sorted_quality = sorted(self.store_food_quality.items(), key=lambda x: x[1], reverse=True)
        return sorted_quality[:num_entries]