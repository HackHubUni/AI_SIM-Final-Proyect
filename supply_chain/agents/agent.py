from collections import abc
from SE.belief import *
from SE.so_sistemaexperto import *
import queue
class Agent(abc.Protocol):
    def brf(self):
        # partir de una entrada perceptual y el cjto de creencias actuales determina un nuevo cjto de creencias
        pass
    
    def options(self):
        while not self.orders.empty():
            order = self.orders.get()
            desire = Desire(order)
            self.Desires.add(desire)

    def options(self):
    
        while not self.orders.empty():
            order = self.orders.get()
            desire = Desire(order)
            self.Desires.add(desire)

    def filter(self):
        pass

    def execute(self):
        pass

class Message:
            """
            Represents a message for communication between agents.
            """

            def __init__(self, sender, receiver, content:Belief):
                self.sender = sender
                self.receiver = receiver
                self.content = content

            def to_belief(self)->Belief:
                """
                Converts the message into a belief.
                """
                return self.content
            
class OrderAgent():
    """
    Represent a order agent in the supply chain.
    """
    
    def __init__(self, product, quantity, origin, request_date, delivery_date):
        self.product = product
        self.quantity = quantity
        self.origin = origin
        self.request_date = request_date
        self.delivery_date = delivery_date



class Desire:
    """
    Represent a desire in the supply chain.
    """

    def __init__(self, order:OrderAgent):
        self.order = order

    


class AgenteProductor:
    """
    Representa un agente productor en la cadena de suministro.
    """

    def __init__(self):
        self.cola_pedidos = []  # Cola de pedidos recibidos
        self.inventario = {}  # Inventario de productos disponibles

    def recibir_pedido(self, pedido):
        """
        Recibe un nuevo pedido y lo agrega a la cola de pedidos.
        """
        self.cola_pedidos.append(Pedido(pedido))

    def transformar_pedido_en_deseo(self):
        """
        Transforma el siguiente pedido de la cola en un deseo.
        """
        if self.cola_pedidos:
            pedido = self.cola_pedidos.pop(0)
            return Deseo(pedido)
        else:
            return None

    def planificar_produccion(self, deseo):
        """
        Crea un plan de producción para cumplir con el deseo especificado.
        """
        # Implementar lógica de planificación de producción
        pass

    def ejecutar_produccion(self, plan_produccion):
        """
        Ejecuta el plan de producción y fabrica el producto deseado.
        """
        # Implementar lógica de ejecución de producción
        pass

    def satisfacer_deseo(self, deseo, producto_fabricado):
        """
        Satisface el deseo entregando el producto fabricado al agente solicitante.
        """
        # Implementar lógica de satisfacción del deseo
        pass

    def gestionar_pedidos(self):
        """
        Gestiona los pedidos recibidos, transformándolos en deseos y ejecutando la producción.
        """
        while True:
            deseo = self.transformar_pedido_en_deseo()
            if deseo:
                plan_produccion = self.planificar_produccion(deseo)
                producto_fabricado = self.ejecutar_produccion(plan_produccion)
                self.satisfacer_deseo(deseo, producto_fabricado)
            else:
                break


# Ejemplo de uso
producto = "Producto A"
cantidad = 100
prioridad = 1
origen = "Agente Cliente 1"
fecha_solicitud = datetime.datetime.now()
fecha_entrega = fecha_solicitud + datetime.timedelta(days=5)

pedido = Pedido(producto, cantidad, prioridad, origen, fecha_solicitud, fecha_entrega)

agente_productor = AgenteProductor()
agente_productor.recibir_pedido(pedido)
agente_productor.gestionar_pedidos()
