from abc import ABC

from supply_chain.Company.companies_types.distribution_company import LogisticCompany
from supply_chain.agents.utils import generate_guid, ImplicationLogicWrapped
from supply_chain.company import Company, TypeCompany
from typing import Callable

import uuid
from typing import Callable
import heapq


class Message(ABC):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,

                 ):
        self.company_from: str = company_from
        self.company_from_type: TypeCompany = company_from_type
        self.company_destination_name: str = company_destination_name
        self.company_destination_type: TypeCompany = company_destination_type


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


class ResponseOfertProductMessaage(Message):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 product_name: str,
                 price_per_unit: float,
                 count_can_supply: int,
                 peticion_instance: MessageWantProductOffer,
                 end_time: int
                 ):
        super().__init__(company_from=company_from,
                         company_from_type=company_from_type,
                         company_destination_name=company_destination_name,
                         company_destination_type=company_destination_type,
                         )
        self.product_name: str = product_name
        self.price_per_unit: float = price_per_unit
        self.count_can_supply: int = count_can_supply
        self.peticion_instance: MessageWantProductOffer = peticion_instance
        self.id_ = generate_guid()
        self.end_time: int = end_time

    def __lt__(self, other):
        return self.end_time < other.end_time

    def __eq__(self, other):
        if isinstance(other, ResponseOfertProductMessaage):
            return self.id_ == other.id_
        return False


class ResponseOfertProductMessaageManager:
    """
    En el heap puede ver ofertas que ya hallan sido consumidas lo que como no se habian vencido
    no se han borrado
    """

    def __init__(self, get_time: Callable[[], int]):
        self._get_time: Callable[[], int] = get_time
        self._list_actual: list[ResponseOfertProductMessaage] = []
        self._actual_dict: dict[str, ResponseOfertProductMessaage] = {}

    @property
    def time(self):
        return self._get_time()

    def add_ResponseOfertProductMessaage(self, response_ofert_msg: ResponseOfertProductMessaage):
        id_ = response_ofert_msg.id_

        if self.time >= response_ofert_msg.end_time:
            raise Exception(
                f'La oferta_osea la respuesta a la peticion de precio-cant a vender: {response_ofert_msg} ya esta vencida')

        if id_ in self._actual_dict:
            raise Exception(
                f'La oferta_osea la respuesta a la peticion de precio-cant a vender: {response_ofert_msg} ya esta creada')

        # Añadir al dicc
        self._actual_dict[id_] = response_ofert_msg
        # añadir a la lista
        self._list_actual.append(response_ofert_msg)

        assert len(self._list_actual) == len(
            self._actual_dict), f'El len de la lista es:{len(self._list_actual)} es distinto al del dict {len(self._actual_dict)}'

        heapq.heappush(self._list_actual, response_ofert_msg)

    def get_ResponseOfertProductMessaages(self) -> list[ResponseOfertProductMessaage]:
        """
        Devuelve una lista con los elementos que se tiene
        :return:
        """
        self.update()
        return list(self._actual_dict.values())

    def is_ofer_active(self, id_) -> bool:
        """Devuelve si la oferta sigue activa o se ha quitado"""

    def get_ofer_by_id(self, id_: str) -> ResponseOfertProductMessaage:
        return self._actual_dict.pop(id_, None)

    def update(self):
        while len(self._list_actual) > 0 and self._list_actual[0].end_time <= self.time:
            to_remove: ResponseOfertProductMessaage = heapq.heappop(self._list_actual)
            del self._actual_dict[to_remove.id_]


class BuyOrderMessage(Message):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 ofer_id: str,
                 count_want: int,
                 logistic_company: LogisticCompany,
                 to_company: Company

                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type)
        self.ofer_id: str = ofer_id
        self.count_want_buy = count_want
        self.logistic_company: LogisticCompany = logistic_company
        self.to_company: Company = to_company


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


class AskPriceLogistic(Message):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 product_name:str,
                 count_move:int,
                 recibir_producto_desde_name:str,
                 recibir_producto_desde_tag:TypeCompany,
                 destino_producto_compania_nombre:str,
                 destino_producto_compania_tag:TypeCompany,

                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type)
        self.product_name: str=product_name
        self.count_move: int=count_move
        self.recibir_producto_desde_name: str=recibir_producto_desde_name
        self.recibir_producto_desde_tag: TypeCompany=recibir_producto_desde_tag
        self.destino_producto_compania_nombre: str=destino_producto_compania_nombre
        self.destino_producto_compania_tag: TypeCompany=destino_producto_compania_tag

class ResponseLogistic(AskPriceLogistic):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 product_name: str,
                 count_ask_move: int,
                 recibir_producto_desde_name: str,
                 recibir_producto_desde_tag: TypeCompany,
                 destino_producto_compania_nombre: str,
                 destino_producto_compania_tag: TypeCompany,
                 price:float,
                 count_can_move:int,
                 time_duration:int,

                 ):
        super().__init__(
                     company_from,
                     company_from_type,
                     company_destination_name,
                     company_destination_type,
                     product_name,
                     count_ask_move,
                     recibir_producto_desde_name,
                     recibir_producto_desde_tag,
                     destino_producto_compania_nombre,
                     destino_producto_compania_tag,

        )
        self.time_duration=time_duration
        self.price=price
        self.count_move=count_can_move
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
                 ):
        self.get_time: Callable[[], int] = get_time
        self.send_msg: Callable[[Message], None] = send_msg
        self.dict_valoracion_inicial: dict[TypeCompany, dict[str, float]] = dict_valoracion_inicial
        self.logic_implication: list[ImplicationLogicWrapped] = logic_implication
