import queue

from supply_chain.Mensajes.offer_msg import ResponseStoreProductInStockNow, ResponseOfertProductMessaage, Oferta
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
        self._offer_cosas_a_cumplir_si_la_acepto: dict[[Message], list[[Message]]] = {}
        """
        Por cada oferta guarda que tengo que mandar a cumplir en orden 
        """
        self.id__offer_cosas: dict[str, Oferta] = {}
        """
        Aca se guarda la llame del mensaje que esta en el diccionario de arriba
        """

    def get_to_acept_offer_pipe_line(self, id_: str):
        if not id_ in self.id__offer_cosas:
            raise Exception(f' El id {id_} no esta')

        msg = self.id__offer_cosas[id_]
        if not msg in self._offer_cosas_a_cumplir_si_la_acepto:
            raise Exception(f' El mensaje {msg} se tiene guardado por su id_ pero no tiene condiciones')
        pip_line = [msg] + self._offer_cosas_a_cumplir_si_la_acepto[msg]

        return pip_line
    def add_ask_from_matrix_to_another_company(self, msg: Message, list_conditions: list[Message]):
        """
        Añadir mensajes que envia a otra compañia con las condiciones osea el distribuidor o la red de flujo seleccionada
        :param msg:
        :return:La id_ que debe ponerse en el flujo
        """
        if msg in self._offer_cosas_a_cumplir_si_la_acepto:
            raise Exception(
                f'El gestor para las peticiones de la tienda {self.store_name} por el producto {self.product_name} ya ha sido enviado el msg {msg}')

        if len(list_conditions) < 1:
            raise Exception('f La lista de condiciones tiene que tener elementos ')

        self._offer_cosas_a_cumplir_si_la_acepto[msg] = list_conditions

        if isinstance(msg, ResponseStoreProductInStockNow):
            # Cant en el almacen
            self.id__offer_cosas[msg.id_] = msg

        elif isinstance(msg, ResponseOfertProductMessaage):
            # Cantidad que puede vender de materia ya elaborada

            self.id__offer_cosas[msg.id_] = msg


        else:
            raise Exception(f'El mensaje {msg} no esta contemplado')










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
        #self._queue: queue.Queue = queue.Queue(-1)

        #self.store_now: StoreOrderGestor = None

    def _make_the_key(self, order: StoreOrderGestor):
        return (order.store_name, order.product_name)

    def create_store_order_gestor(self, store_name: str, product_want_name: str, id_pedido: str):
        """
        Crea un gestor de peticiones de tiendas el id_pedido es el que tiene el msg que hace la tienda a esta matrix y lo guarda en el gestor de la matrix
        :param store_name:
        :param product_want_name:
        :param id_pedido:
        :return:
        """
        store_order = StoreOrderGestor(store_name=store_name, product_name=product_want_name,
                                       store_restock_msg_matrix_id=id_pedido)
        if self.is_the_order_in_the_gestor(store_order):
            return store_order

        self._push_store_order(store_order)

        return store_order

    def _push_store_order(self, order: StoreOrderGestor):
        key = self._make_the_key(order)

        if key in self._dict_store_order_gestor:
            raise Exception('La orden para buscar de una tienda ya esta en la gestor de estas ordenes')
        #self.store_now = order
        self._dict_store_order_gestor[key] = order
        #

    def can_process_this_store_order(self, store_name: str, product_name: str):
        """
        Devuelve booleano si se puede procesar o no la orden ahora
        :param store_name:
        :param product_name:
        :return:
        """
        return not (store_name, product_name) in self._dict_store_order_gestor

    def is_the_order_in_the_gestor(self, order: StoreOrderGestor) -> bool:
        """
        devuelve True or False en dependencia si la orden para una tienda y un producto esta aca osea no ha sido suplida

        :param order:
        :return:
        """
        return self._make_the_key(order) in self._dict_store_order_gestor

    def is_empty(self):
        return self._queue.empty()


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

    def get_key_from_store_name_and_product_name(self, store_name: str, product_name: str):
        return (store_name, product_name)


    def delete_store_order(self, store_name: str, product_name: str):
        """
        Elimina el store gestor de una tienda para que pueda seguir sacándose resultado
        :param store_name:
        :param product_name:
        :return:
        """
        key = self.get_key_from_store_name_and_product_name(store_name, product_name)
        if not key in self._dict_store_order_gestor:
            raise Exception(f'El store_gestor con key {(store_name, product_name)} no esta disponible')

        del self._dict_store_order_gestor[key]


class OfferGestor:
    def __init__(self, id_offer_objetive: str):
        self.id_offer_objetive: str = id_offer_objetive
        self.id_necesitar_cumplir: set[str] = set()

    def set_necesitar_cumplir_tb_contrato(self, id_contrato: str):
            self.id_necesitar_cumplir.add(id_contrato)


class Gestor:
    def __init__(self, store_name: str):
        self.store_name: str = store_name
        self.dict_offer_need_to_cumplir: dict[Message, list[Message]]
