from typing import Callable

import heapq
from supply_chain.Mensajes.ask_msg import Message, MessageWantProductOffer, HacerServicioDeDistribucion, \
    MessageWantProductProduceOffer
from supply_chain.agents.utils import generate_guid
from supply_chain.company import TypeCompany
from supply_chain.products.ingredient import Ingredient


class Oferta(Message):
    """Clase abstractra  no inicializar"""

    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 peticion_instance: Message,
                 end_time: int
                 ):
        super().__init__(company_from=company_from,
                         company_from_type=company_from_type,
                         company_destination_name=company_destination_name,
                         company_destination_type=company_destination_type,
                         )

        self.peticion_instance: Message = peticion_instance
        self.id_ = generate_guid()
        self.end_time: int = end_time

    def __lt__(self, other):
        return self.end_time < other.end_time

    def __eq__(self, other):
        if isinstance(other, Oferta):
            return self.id_ == other.id_
        return False


class ResponseOfertMessage(Oferta):
    """ABstracta"""

    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 product_name: str,
                 price_per_unit: float,

                 peticion_instance: MessageWantProductOffer,
                 end_time: int
                 ):
        super().__init__(company_from=company_from,
                         company_from_type=company_from_type,
                         company_destination_name=company_destination_name,
                         company_destination_type=company_destination_type,
                         end_time=end_time,
                         peticion_instance=peticion_instance
                         )
        self.product_name: str = product_name
        self.price_per_unit: float = price_per_unit
        self.peticion_instance: MessageWantProductOffer = peticion_instance
        self.id_ = generate_guid()
        self.end_time: int = end_time


class ResponseOfertProduceProductMessage(ResponseOfertMessage):
    """Para enviar mensajes desde el productor a la matrix"""
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 product_name: str,
                 price_per_unit: float,
                 peticion_instance: MessageWantProductProduceOffer,
                 end_time: int,
                 list_ingredients_recipe: list[Ingredient]
                 ):
        super().__init__(company_from=company_from,
                         company_from_type=company_from_type,
                         company_destination_name=company_destination_name,
                         company_destination_type=company_destination_type,
                         end_time=end_time,
                         peticion_instance=peticion_instance,
                         price_per_unit=price_per_unit,
                         product_name=product_name,
                         )
        self.list_ingredients_recipe: list[Ingredient]=list_ingredients_recipe


class ResponseOfertProductMessaage(ResponseOfertMessage):
    """Clase que te brinda la respuesta de una empresa a la matrix"""
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
                         end_time=end_time,
                         peticion_instance=peticion_instance,
                         price_per_unit=price_per_unit,
                         product_name=product_name,

                         )
        self.count_can_supply: int = count_can_supply

    def _show(self):
        return f'Producto: {self.product_name} precio por unidad {self.price_per_unit} cuanto puede suplir {self.count_can_supply} el id {self.id_} y finaliza en el {self.end_time}'

    def __str__(self):
        return self._show()

    def __repr__(self):
        return self._show()

class ResponseStorageProductOffer(ResponseOfertProductMessaage):
    """Clase para responder cuanto espacio se puede asignar"""
    pass

class ResponseStoreProductInStockNow(ResponseOfertProductMessaage):
    """Clase para responder cuanto tenemos en stock de un producto"""


class ResponseLogistic(Oferta):
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
                 peticion_instancie: HacerServicioDeDistribucion,
                 price: float,
                 count_can_move: int,
                 end_time: int,

                 ):
        super().__init__(
            company_from=company_from,
            end_time=end_time,
            company_from_type=company_from_type,
            company_destination_type=company_destination_type,
            peticion_instance=peticion_instancie,
            company_destination_name=company_destination_name,

        )

        self.product_name: str = product_name
        self.count_ask_move: int = count_ask_move
        self.recibir_producto_desde_name: str = recibir_producto_desde_name
        self.recibir_producto_desde_tag: TypeCompany = recibir_producto_desde_tag
        self.destino_producto_compania_nombre: str = destino_producto_compania_nombre
        self.destino_producto_compania_tag: TypeCompany = destino_producto_compania_tag
        self.price: float = price
        self.count_can_move: int = count_can_move


class GestorOfertas:
    """
    En el heap puede ver ofertas que ya hallan sido consumidas lo que como no se habian vencido
    no se han borrado
    """

    def __init__(self, get_time: Callable[[], int]):
        self._get_time: Callable[[], int] = get_time
        self._list_actual: list[Oferta] = []
        self._actual_dict: dict[str, Oferta] = {}

    @property
    def time(self):
        return self._get_time()

    def add_response_despues_de_negociar_oferta(self, response_ofert_msg: Oferta):
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
        # self._list_actual.append(response_ofert_msg)

        heapq.heappush(self._list_actual, response_ofert_msg)

        assert len(self._list_actual) == len(
            self._actual_dict), f'El len de la lista es:{len(self._list_actual)} es distinto al del dict {len(self._actual_dict)}'

    def get_ResponseOfertProductMessaages(self) -> list[Oferta]:
        """
        Devuelve una lista con los elementos que se tiene
        :return:
        """
        self.update()
        return list(self._actual_dict.values())

    def is_ofer_active(self, id_) -> bool:
        """Devuelve si la oferta sigue activa o se ha quitado"""

    def get_ofer_by_id(self, id_: str) -> Oferta:
        return self._actual_dict.pop(id_, None)

    def update(self):
        while len(self._list_actual) > 0 and self._list_actual[0].end_time <= self.time:
            to_remove: Oferta = heapq.heappop(self._list_actual)
            del self._actual_dict[to_remove.id_]
