from supply_chain.Company.companies_types.Warehouse_Company import WarehouseCompany
from supply_chain.agents.AgentWrapped import *


class WareHouseAgente(AgentWrapped):
    def __init__(self,
                 name: str,
                 company: WarehouseCompany,
                 env_visualizer: EnvVisualizer,

                 ):
        super().__init__(name, company, env_visualizer)
        self.company: WarehouseCompany = company

        # Start
        self.start()

    def _process_ask_price(self, msg: AskPriceWareHouseCompany):
        company_from_name = msg.company_from
        product_want_name = msg.product_want_name

        if msg.company_from_type != TypeCompany.Matrix:
            raise Exception(
                f'Se le paso un msg de tipo {type(msg)} al agente {self.name} de la compañia tipo {self.company.tag} con nombre {self.company.name}')
        # Factor por el que multiplicar el precio general del servicio
        factor = self.get_factor_price_to_a_client(company_from_name, product_want_name)
        # Coste total del servicio
        total_cost = self.company.get_cost_by_product_and_unit_time(product_want_name)
    def recive_msg(self, msg: Message):
        if isinstance(msg, AskPriceWareHouseCompany):
            self._process_ask_price(msg)
        else:
            self.lanzar_excepcion_por_no_saber_mensaje(msg)
