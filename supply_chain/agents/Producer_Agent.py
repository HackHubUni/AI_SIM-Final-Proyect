import copy
from abc import ABC, abstractmethod

from new.logic import *

from enum import Enum

from supply_chain.agent import Agent, AgentException
from supply_chain.agents.Sistema_experto import SistExperto
from supply_chain.agents.utils import *

from supply_chain.sim_environment import SimEnvironment

from supply_chain.Company.companies_types.Producer_Company import *

from supply_chain.Comunicator import *


def make_valoracion(calificacion: float):
    """define la valoracion tags de empresas"""
    # INicia siendo mala
    tag = ValoracionTag.Fatal
    if calificacion > 2:
        tag = ValoracionTag.Mal
    elif calificacion > 4:
        tag = ValoracionTag.Regular
    elif calificacion > 6:
        tag = ValoracionTag.Bien
    elif calificacion > 8:
        tag = ValoracionTag.MuyBien
    elif calificacion > 9.4:
        tag = ValoracionTag.Excelente
    return tag


class ProducerAgent(Agent):

    def update_clients(self):
        # Valoracion e las matrices
        matrix_names = self.dict_valoracion_inicial[TypeCompany.Matrix]
        # TODO:ACa estan los valores para discriminar que tan bien me caen
        for name in matrix_names.keys():
            # Añadir los clientes
            client = ClientWrapped(name)
            self.sistema_experto.add(client)

            # Obtengo la calificacion en puntos
            calificacion = matrix_names[name]

            # Ahora la llevo a los tags
            tag = make_valoracion(calificacion)

            # Creo la figura Valoracion
            valoracion = Valoracion(name, tag)

            # Lo añado al sistema experto
            self.sistema_experto.add(valoracion)

    def update_products(self):
        list_products_init_ = self.company.get_name_products_in_stock_now()

        for product_name in list_products_init_:
            product = ProductWrapped(product_name)
            # Añadir al sist experto
            self.sistema_experto.add(product)

    def update_implications(self):

        for implication in self.logic_implication:
            self.sistema_experto.add(implication)

    def update(self):
        # Upgradear los productos
        self.update_products()
        # Upgradear los clientes
        self.update_clients()
        # Upgradear las implicaciones
        self.update_implications()

    def start(self):
        self.update()

    def __init__(self,
                 name: str,
                 company: ProducerCompany,
                 dict_valoracion_inicial: dict[TypeCompany, dict[str, float]],
                 logic_implication: list[ImplicationLogicWrapped],
                 env_visualizer: EnvVisualizer,

                 ):
        super().__init__(name)
        self.company = company
        self.dict_valoracion_inicial: dict[TypeCompany, dict[str, float]] = copy.deepcopy(dict_valoracion_inicial)
        self.sistema_experto: SistExperto = SistExperto()
        self.logic_implication: list[ImplicationLogicWrapped] = copy.deepcopy(logic_implication)
        self.env_visualizer: EnvVisualizer = env_visualizer
        # Start
        self.start()

        # Manager de las ofertas
        self.ofer_manager: ResponseOfertProductMessaageManager = ResponseOfertProductMessaageManager(
            self.env_visualizer.get_time)

        # guid, Respuesta de la peticion de precio

    @property
    def time(self):
        return self.env_visualizer.get_time()


    def send_smg_to_a_agent(self,msg:Message):
        """Envia un mensaje a otro agente"""
        self.env_visualizer.send_msg(msg)

    def sent_msg_response_ofer(self, oferta: MessageWantProductOffer, count_can_supply: int, price_per_unit: float):

        response = ResponseOfertProductMessaage(company_from_type=self.company.tag,
                                                company_from=self.company.name,
                                                company_destination_type=oferta.company_from_type,
                                                company_destination_name=oferta.company_from,
                                                product_name=oferta.product_want_name,
                                                price_per_unit=price_per_unit,
                                                count_can_supply=count_can_supply,
                                                peticion_instance=oferta,
                                                )

        self.ofer_manager.add_ResponseOfertProductMessaage(response)



    def sent_msg_response_ofer_cant_supply(self, oferta: MessageWantProductOffer):
        self.sent_msg_response_ofer(oferta, 0, -1.1)

    def _get_a_factor_to_a_client(self, from_company_name: str, product_want_name: str,
                                  class_type: PedirPrecio | PedirCantidad):
        """Metodo base para que se pueda pedir factor para suplir de pedido y cant de factor de precio"""
        # Ahora pedir el factor del precio
        price_ask = class_type(StringWrapped(from_company_name), StringWrapped(product_want_name), "x")
        # Factor a multiplicar el precio
        factor = self.sistema_experto.ask(price_ask)

        if not isinstance(factor, float):
            AgentException(
                f'En el agente {self.name} recibiendo una orden de {from_company_name} como pidiendo precio lo que devolvio la inferencia no es float para ser el facto es {type(factor)}')
        return factor

    def get_factor_price_to_a_client(self, from_company_name: str, product_want_name: str) -> float:
        """
        Devuelve el factor a ajustar para un cliente dado
        :param from_company_name:
        :param product_want_name:
        :return:
        """
        return self._get_a_factor_to_a_client(from_company_name, product_want_name, PedirPrecio)

    def get_factor_count_to_sell_producto_to_a_client(self, from_company_name: str, product_want_name: str) -> float:
        """
        Devuelve el factor a multiplicar por la cant de unidades disponibles para vender
        :param from_company_name:
        :param product_want_name:
        :return:
        """
        return self._get_a_factor_to_a_client(from_company_name, product_want_name, PedirCantidad)

    def _ask_price_product(self, msg: MessageWantProductOffer):
        # Es pq esta pidiendo precio

        # SI no es una empresa matriz lanzo excepcion

        if not msg.company_from_type == TypeCompany.Matrix:
            raise AgentException(
                f'El agente {self.name} de tipo {self.company.tag}  no puede recibir ofertas de un no matriz {msg.company_from} de tipo {msg.company_from_type}')

        # Comprobar que hay en stock este producto
        if not self.company.is_product_in_stock(msg.product_want_name):
            # Decirle que no  tengo
            self.sent_msg_response_ofer_cant_supply(msg)

        from_company_name = msg.company_from
        product_want_name: str = msg.product_want_name

        factor_price = self.get_factor_price_to_a_client(from_company_name, product_want_name)

        final_price = self.company.get_product_price(product_want_name) * factor_price

        # Cuantas unidades se le puede vender

        factor_to_buy = self.get_factor_count_to_sell_producto_to_a_client(from_company_name, product_want_name)

        temp = self.company.stock_manager.get_count_product_in_stock(product_want_name) * factor_to_buy
        final_count_to_supply = int(temp)

        # Enviar la respuesta

        self.sent_msg_response_ofer(msg, final_count_to_supply, final_price)

    def make_sell_ofert_response(self,msg:BuyOrderMessage,count_to_sell:int):
        """
        Hace los mensaje sque se le envia a la empresa por la compra
        :param msg:
        :return:
        """
        ofer_id = msg.ofer_id
        response = SellResponseMessage(
            company_from=self.company.name,
            company_from_type=self.company.tag,
            company_destination_name=msg.company_from,
            company_destination_type=msg.company_from_type,
            ofer_id=msg.ofer_id,
            count_want=msg.count_want_buy,
            count_sell=count_to_sell

        )
        return response
    def going_to_sell(self,msg:BuyOrderMessage):
        """Cuando te hacen una orden de compra"""
        ofer_id = msg.ofer_id

        if not self.ofer_manager.is_ofer_active(ofer_id) :
            # Responder con cant a vender cero no hay oferta
            response=self.make_sell_ofert_response(msg,0)
            self.send_smg_to_a_agent(response)
        ofer = self.ofer_manager.get_ofer_by_id(ofer_id)


        sell_order = SellOrder(product_name=ofer.product_name,
                               matrix_name=ofer.company_from,
                               price_sold=ofer.price_per_unit,
                               amount_asked=ofer.count_can_supply,
                               amount_sold=msg.count_want_buy,
                               normal_price_per_unit=self.company.get_product_price(ofer.product_name),
                               to_company=msg.to_company,
                               logistic_company=msg.logistic_company

                               )
        product_name=ofer.product_name
        self.company.sell(sell_order)
        count_to_supply=min(min(ofer.count_can_supply,msg.count_want_buy),self.company.get_count_product_in_stock(product_name))

        response=self.make_sell_ofert_response(msg,count_to_supply)
        self.send_smg_to_a_agent(response)

    def recive_msg(self, msg: Message):
        # Upgradear la base de conocimiento
        self.update()

        if isinstance(msg, MessageWantProductOffer):
            return self._ask_price_product(msg)
        elif isinstance(msg, BuyOrderMessage):
            self.going_to_sell(msg)


