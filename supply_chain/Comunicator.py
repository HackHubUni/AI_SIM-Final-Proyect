from abc import ABC

from supply_chain.Company.companies_types.distribution_company import LogisticCompany
from supply_chain.Message import Message
from supply_chain.agents.utils import generate_guid, ImplicationLogicWrapped
from supply_chain.company import Company, TypeCompany
from typing import Callable

import uuid
from typing import Callable
import heapq


class MessageWantProductOffer(Message):
    """Clase para mensajes ResponseOfertProductMessaage"""

    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 product_want_name: str,
                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type)
        self.product_want_name: str = product_want_name


class BuyOrderMessage(Message):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 ofer_id: str,
                 count_want: int,
                 logistic_company_name: str,
                 id_contract_logistic: str,
                 id_contract_destination:str, #Si es una tienda poner el id en -1
                 to_company: str,
                 price_logist: float,
                 time_logist: int,

                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type)
        self.id_contract_logistic: str = id_contract_logistic
        self.ofer_id: str = ofer_id
        self.price_logist: float = price_logist
        self.time_logist: int = time_logist
        self.count_want_buy = count_want
        self.logistic_company: str = logistic_company_name
        self.to_company: str = to_company
        self.id_contract_destination: str=id_contract_destination

class SellResponseMessage(BuyOrderMessage):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 ofer_id: str,
                 count_want: int,
                 count_sell: int,
                 total_cost: int,
                 logistic_company: LogisticCompany,
                 to_company: Company

                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type,
                         ofer_id,
                         count_want)

        self.count_sell = count_sell

        self.total_cost = total_cost


class HacerServicioDeDistribucion(Message):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 product_name: str,
                 count_move: int,
                 recibir_producto_desde_name: str,
                 recibir_producto_desde_tag: TypeCompany,
                 destino_producto_compania_nombre: str,
                 destino_producto_compania_tag: TypeCompany,

                 ):
        super().__init__(company_from=company_from,
                         company_from_type=company_from_type,
                         company_destination_name=company_destination_name,
                         company_destination_type=company_destination_type,
                         )
        self.product_name: str = product_name
        self.count_move: int = count_move
        self.recibir_producto_desde_name: str = recibir_producto_desde_name
        self.recibir_producto_desde_tag: TypeCompany = recibir_producto_desde_tag
        self.destino_producto_compania_nombre: str = destino_producto_compania_nombre
        self.destino_producto_compania_tag: TypeCompany = destino_producto_compania_tag


class Comunicator:

    def __init__(self,
                 productor_list: list[Company],
                 ):
        self.productor_list = productor_list

    def sent_want_product_msg(self, msg: MessageWantProductOffer):
        productor_name = msg.company_destination_name
        for productor in self.productor_list:
            if productor.name == productor_name:
        # TODO: Agregar aca  el enviar al agente


class EnvVisualizer:

    def __init__(self,
                 get_time: Callable[[], int], send_msg: Callable[[Message], None],
                 dict_valoracion_inicial: dict[TypeCompany, dict[str, float]],
                 logic_implication: list[ImplicationLogicWrapped],
                 get_distance_in_the_map:Callable[[str,str],float],
                 ):
        self.get_distance_in_the_map:Callable[[str,str],float]=get_distance_in_the_map
        self.get_time: Callable[[], int] = get_time
        self.send_msg: Callable[[Message], None] = send_msg
        self.dict_valoracion_inicial: dict[TypeCompany, dict[str, float]] = dict_valoracion_inicial
        self.logic_implication: list[ImplicationLogicWrapped] = logic_implication
