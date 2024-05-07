import queue

from supply_chain.Message import Message


class StoreOrderGestor:

    def __init__(self,
                 store_name: str,
                 store_restock_msg_matrix_id: str,
                 product_name: str,
                 ):
        self.store_name: str = store_name
        self.store_restock_msg_matrix_id: str = store_restock_msg_matrix_id
        self.product_name: str = product_name
        self._set_ask_from_matrix_to_another_company: set[Message] = set()

        self._set_response_from_another_company_to_matrix: set[Message] = set()

    def add_ask_from_matrix_to_another_company(self, msg: Message):
        """
        Añadir mensajes que envia a otra compañia
        :param msg:
        :return:
        """
        if msg in self._set_ask_from_matrix_to_another_company:
            raise Exception(
                f'El gestor para las peticiones de la tienda {self.store_name} por el producto {self.product_name} ya ha sido enviado el msg {msg}')
        self._set_ask_from_matrix_to_another_company.add(msg)

    def add_response_from_company(self, msg: Message):
        if msg in self._set_response_from_another_company_to_matrix:
            raise Exception(f'No se puede añadir dos veces la respuesta del mensaje {msg}')

    def __eq__(self, other):
        if isinstance(other, StoreOrderGestor):
            return self.store_name == other.store_name and self.product_name == other.store_name
        return False

    def __hash__(self):
        return hash(f'{self.store_name}_{self.product_name}')


class MatrixOrderGestor:

    def __init__(self):
        self._dict_store_order_gestor: dict[tuple[str, str], StoreOrderGestor] = {}
        # Nombre de la tienda nombre producto el store gestor
        self._queue: queue.Queue = queue.Queue(-1)

        self.store_now: StoreOrderGestor = None

    def _make_the_key(self, order: StoreOrderGestor):
        return (order.store_name, order.product_name)

    def push_store_order(self, order: StoreOrderGestor):
        key = self._make_the_key(order)

        if key in self._dict_store_order_gestor:
            raise Exception('La orden para buscar de una tienda ya esta en la gestor de estas ordenes')
        self.store_now = order
        self._dict_store_order_gestor[key] = order
        self._queue.put(order)

    def is_the_order_in_the_gestor(self, order: StoreOrderGestor) -> bool:
        """
        devuelve True or False en dependencia si la orden para una tienda y un producto esta aca osea no ha sido suplida

        :param order:
        :return:
        """
        return self._make_the_key(order) in self._dict_store_order_gestor

    def is_empty(self):
        return self._queue.empty()

    # def pop_store_order(self, order: StoreOrderGestor):
    #    if self.is_empty():
    #        raise Exception(f'La cola de ordenes esta vacia')
    #    value = self._queue.get()
    #    if not value in self._set_store_order_gestor:
    #        raise Exception(f' Hay una orden para comprar para una tienda en la cola que no esta en el set {order}')

    #    self._set_store_order_gestor.discard(value)

    #    return value
    #

    def get_store_manager_now(self):
        """
        Retorna la orden de compra de la tienda que se procesa ahora
        :return:
        """
        if self.store_now is None:
            raise Exception(f'No se puede estar abasteciendo a ninguna tienda ')

        return self.store_now

    def get_store_order(self, store_name: str, product_name: str):
        key = (store_name, product_name)

        if not key in self._dict_store_order_gestor:
            raise Exception(f'La llave {key} no esta en el diccionario')

        return self._dict_store_order_gestor[key]
