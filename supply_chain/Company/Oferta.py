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
