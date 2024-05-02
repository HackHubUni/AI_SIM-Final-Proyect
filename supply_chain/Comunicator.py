from supply_chain.company import Company, TypeCompany


class Message:
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
    """Clase para mensajes oferta"""

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
                 id_:str,
                 end_time:int
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
        self._id=id_
        self.end_time:int=

    def __lt__(self, other):
        return self.end_time < other.end_time

    def __eq__(self, other):
        if isinstance(other, Oferta):
            return self.id == other.id
        return False


class SellOrderMessage(Message):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,

                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type)

import uuid
from typing import Callable
import heapq


class Oferta:
    def __init__(self,
                 product_name: str,
                 count_to_sell: int,
                 end_time: int,
                 matrix_name: str):
        self.id: str = str(uuid.uuid4())
        self.product_name: str = product_name
        self.count_to_sell: int = count_to_sell
        self.end_time: int = end_time
        self.matrix_name = matrix_name

    def __lt__(self, other):
        return self.end_time < other.end_time

    def __eq__(self, other):
        if isinstance(other, Oferta):
            return self.id == other.id
        return False


class OfertaManager:
    def __init__(self, get_time: Callable[[], int]):
        self._get_time: Callable[[], int] = get_time
        self._list_actual: list[Oferta] = []
        self._actual_set: set[Oferta] = set()

    @property
    def time(self):
        return self._get_time()

    def add_oferta(self, oferta: Oferta):
        if self.time >= oferta.end_time:
            raise Exception(f'La oferta: {oferta} ya esta vencida')

        if oferta in self._actual_set:
            raise Exception(f'La oferta: {oferta} ya esta creada')

        # Añadir al set
        self._actual_set.add(oferta)
        # añadir a la lista
        self._list_actual.append(oferta)

        assert len(self._list_actual) == len(
            self._actual_set), f'El len de la lista es:{len(self._list_actual)} es distinto al del set {len(self._actual_set)}'

        heapq.heappush(self._list_actual, oferta)

    def get_ofertas(self) -> list[Oferta]:
        self.update()
        return self._list_actual

    def update(self):
        while len(self._list_actual) > 0 and self._list_actual[0].end_time <= self.time:
            to_remove = heapq.heappop(self._list_actual)
            self._actual_set.discard(to_remove)


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
