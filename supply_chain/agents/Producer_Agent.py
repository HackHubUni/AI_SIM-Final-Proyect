import copy
from abc import ABC, abstractmethod

from new.logic import *

from enum import Enum

from supply_chain.agent import Agent, AgentException
from supply_chain.agents.Sistema_experto import SistExperto
from supply_chain.agents.utils import *

from supply_chain.sim_environment import SimEnvironment

from supply_chain.Company.companies_types.Producer_Company import *

from supply_chain.Comunicator import MessageWantProductOffer


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

    def start(self):
        # Upgradear los productos
        self.update_products()
        # Upgradear los clientes
        self.update_clients()
        # Upgradear las implicaciones
        self.update_implications()

    def __init__(self, name: str, company: ProducerCompany,
                 dict_valoracion_inicial: dict[TypeCompany, dict[str, float]],
                 logic_implication: list[ImplicationLogicWrapped]):
        super().__init__(name)
        self.company = company
        self.dict_valoracion_inicial: dict[TypeCompany, dict[str, float]] = copy.deepcopy(dict_valoracion_inicial)
        self.sistema_experto: SistExperto = SistExperto()
        self.logic_implication: list[ImplicationLogicWrapped] = copy.deepcopy(logic_implication)

        # Start
        self.start()

    def recive_msg(self, msg: MessageWantProductOffer):

        if isinstance(msg, MessageWantProductOffer):
            # Es pq esta pidiendo precio

            # SI no es una empresa matriz lanzo excepcion

            if not msg.company_from_type == TypeCompany.Matrix:
                raise AgentException(
                    f'El agente {self.name} de tipo {self.company.tag}  no puede recibir ofertas de un no matriz {msg.company_from} de tipo {msg.company_from_type}')

            from_company_name = msg.company_from
            product_want_name: str = msg.product_want_name


