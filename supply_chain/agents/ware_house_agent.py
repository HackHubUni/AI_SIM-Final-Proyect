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

        can_storage_in_stock = self.company.get_how_can_storage_a_company(company_from_name, product_want_name)

        self.sent_msg_response_ofer(msg, can_storage_in_stock, total_cost, self.get_delay_time(),

                                    ResponseStorageProductOffer)

    def _process_count_product_in_stock(self, msg: AskCountProductInStock):
        if msg.company_from_type != TypeCompany.Matrix:
            raise Exception(f'El mensaje no viene de una Matrix viene de una {msg.company_from_type}')

        matrix_name = msg.company_from
        product_want = msg.product_want_name

        count_in_stock = self.company.get_how_can_storage_a_company(matrix_name, product_want)

        self.sent_msg_response_ofer(msg, count_in_stock, 0, self.get_delay_time(), ResponseStoreProductInStockNow)

    def recive_products(self, msg: HacerServicioDeDistribucion):

        matrix_name = msg.matrix_name
        product_name = msg.product_name
        lis_product = msg.products_instance

        self.company.add_list_product_in_storage(lis_product, matrix_name)

    def _out_product_from(self, msg: BuyOrderMessage):

        matrix_name = msg.company_from
        offer_id = msg.ofer_id
        offer_instance: ResponseStoreProductInStockNow = self.ofer_manager.get_ofer_by_id(offer_id)
        count_want = msg.count_want_buy
        product_name = offer_instance.product_name
        destiny_name = msg.to_company

        if count_want > offer_instance.count_can_supply:
            raise Exception(
                f'La empresa matrix {matrix_name} quiere {count_want} producto pero solo se le puede dar {offer_instance.count_can_supply}')

        lis_order = self.company.get_list_products_by_company(matrix_name, product_name)

        count_to_supply = len(lis_order)

        response = HacerServicioDeDistribucion(matrix_name=matrix_name,
                                               company_from=self.company.name,
                                               company_from_type=self.company.tag,
                                               company_destination_name=destiny_name,
                                               company_destination_type=None,
                                               product_name=product_name,
                                               count_move=count_to_supply,
                                               id_to_recive_company=msg.id_contract_destination,
                                               time_demora_logistico=msg.time_logist,

                                               )

        response.set_list_product(lis_order)

        self.send_smg_to_a_agent(response)

    def recive_msg(self, msg: Message):
        if isinstance(msg, AskPriceWareHouseCompany):
            self._process_ask_price(msg)
        elif isinstance(msg, HacerServicioDeDistribucion):
            self.recive_products(msg)

        elif isinstance(msg, AskCountProductInStock):
            self._process_count_product_in_stock(msg)

        elif isinstance(msg, BuyOrderMessage):

            self._out_product_from(msg)
        else:
            self.lanzar_excepcion_por_no_saber_mensaje(msg)
