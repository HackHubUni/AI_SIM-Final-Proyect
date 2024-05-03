import copy
from abc import ABC, abstractmethod

from enum import Enum

from supply_chain.Company.companies_types.manufacturer_company import ManufacturerCompany
from supply_chain.Mensajes.Mensajes_de_dar_el_precio_y_cant_a_la_matriz import *
from supply_chain.agent import Agent, AgentException
from supply_chain.agents.Sistema_experto import SistExperto

from supply_chain.agents.utils import *

from supply_chain.Company.companies_types.Producer_Company import *

from supply_chain.Comunicator import *


def make_valoracion(calificacion: float):
    """define la valoracion tags de empresas"""
    # INicia siendo mala
    tag = ValoracionTag.Fatal
    if calificacion > 2:
        tag = ValoracionTag.Mal
    if calificacion > 4:
        tag = ValoracionTag.Regular
    if calificacion > 6:
        tag = ValoracionTag.Bien
    if calificacion > 8:
        tag = ValoracionTag.MuyBien
    if calificacion > 9.4:
        tag = ValoracionTag.Excelente
    return tag


class AgentWrapped(Agent):

    @property
    def logic_implication(self) -> list[ImplicationLogicWrapped]:
        return self.env_visualizer.get_logic_implication()

    @property
    def dict_valoracion_inicial(self) -> dict[TypeCompany, dict[str, float]]:
        return self.env_visualizer.get_dict_valoracion()

    @property
    def time(self):
        return self.env_visualizer.get_time()

    def __init__(self,
                 name: str,
                 company: Company,
                 env_visualizer: EnvVisualizer,

                 ):
        super().__init__(name)
        self.company: Company = company
        self.sistema_experto: SistExperto = SistExperto()
        self.env_visualizer: EnvVisualizer = env_visualizer
        # Manager de las ofertas
        self.ofer_manager: GestorOfertas = GestorOfertas(
            self.env_visualizer.get_time)
        self.start()

    def lanzar_excepcion_por_no_saber_mensaje(self, msg: Message):
        raise AgentException(
            f'El mensaje {msg} de typo {type(msg)} no puede ser recibido en esta compañia en {self.name}, {self.company.tag}')

    def start(self):
        self.company.agent_name = self.name
        self.update()

    def send_smg_to_a_agent(self, msg: Message):
        """Envia un mensaje a otro agente"""
        print(msg)

        self.env_visualizer.send_msg(msg)

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
            print(valoracion.show())
            # Lo añado al sistema experto
            self.sistema_experto.add(valoracion)

    def update(self):
        # Upgradear los clientes
        self.update_clients()
        # Upgradear las implicaciones
        self.update_implications()

    def _get_a_factor_to_a_client(self, from_company_name: str, product_want_name: str,
                                  class_type: PedirPrecio | PedirCantidad):
        """Metodo base para que se pueda pedir factor para suplir de pedido y cant de factor de precio"""
        # Ahora pedir el factor del precio
        price_ask = class_type(from_company_name,product_want_name, "z")
        # Factor a multiplicar el precio

        print(price_ask.show())

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

    def tell(info):
        pass

    @abstractmethod
    def recive_msg(self, msg: Message):
        pass

    def update_implications(self):

        for implication in self.logic_implication:
            print(implication.show())
            self.sistema_experto.add(implication)


class ProducerAgent(AgentWrapped):

    def update_products(self):
        list_products_init_ = self.company.get_name_products_in_stock_now()

        for product_name in list_products_init_:
            product = ProductWrapped(product_name)
            # Añadir al sist experto
            print(product.show())
            self.sistema_experto.add(product)

    def update(self):

        # Upgradear los productos
        self.update_products()

        super().update()

    def __init__(self,
                 name: str,
                 company: ProducerCompany,
                 env_visualizer: EnvVisualizer,

                 ):
        super().__init__(name, company, env_visualizer)
        self.company: ProducerCompany = company

        # Start
        self.start()

        # guid, Respuesta de la peticion de precio

    def get_time_demora(self):
        return 300000

    def sent_msg_response_ofer(self, oferta: MessageWantProductOffer, count_can_supply: int, price_per_unit: float):

        response = ResponseOfertProductMessaage(company_from_type=self.company.tag,
                                                company_from=self.company.name,
                                                company_destination_type=oferta.company_from_type,
                                                company_destination_name=oferta.company_from,
                                                product_name=oferta.product_want_name,
                                                price_per_unit=price_per_unit,
                                                count_can_supply=count_can_supply,
                                                peticion_instance=oferta,
                                                end_time=self.get_time_demora()

                                                )

        self.ofer_manager.add_response_despues_de_negociar_oferta(response)

    def sent_msg_response_ofer_cant_supply(self, oferta: MessageWantProductOffer):
        self.sent_msg_response_ofer(oferta, 0, -1.1)

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
            return

        from_company_name = msg.company_from
        product_want_name: str = msg.product_want_name

        factor_price = self.get_factor_price_to_a_client(from_company_name, product_want_name)

        final_price = self.company.get_product_price(product_want_name) * factor_price

        # Cuantas unidades se le puede vender

        factor_to_buy = self.get_factor_count_to_sell_producto_to_a_client(from_company_name, product_want_name)
        print(f'Factor de venta {factor_to_buy}')

        temp = self.company.stock_manager.get_count_product_in_stock(product_want_name) * factor_to_buy



        final_count_to_supply = int(temp)

        # Enviar la respuesta

        self.sent_msg_response_ofer(msg, final_count_to_supply, final_price)

    def make_sell_ofert_response(self, msg: BuyOrderMessage, count_to_sell: int):
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

    def deliver(self, sell_order: SellOrder, time_transport: int):

        a = HacerServicioDeDistribucion(
            matrix_name=sell_order.matrix_name,
            company_from=self.company.name,
            company_from_type=self.company.tag,
            company_destination_name=sell_order.to_company,
            company_destination_type=sell_order.to_company_tag,
            product_name=sell_order.product_name,
            count_move=sell_order.amount_sold,
            time_demora_logistico=time_transport,

        )

        self.company.deliver(self.send_smg_to_a_agent, a)

    # TODO:Implementar la logica de esperar cierto tiempo para enviar

    def going_to_sell(self, msg: BuyOrderMessage):
        """Cuando te hacen una orden de compra"
          se la pasa el id que tiene el logistico para dar el tiempo
        """
        ofer_id = msg.ofer_id

        if not self.ofer_manager.is_ofer_active(ofer_id):
            # Responder con cant a vender cero no hay oferta
            response = self.make_sell_ofert_response(msg, 0)
            self.send_smg_to_a_agent(response)
        ofer: ResponseOfertProductMessaage = self.ofer_manager.get_ofer_by_id(ofer_id)

        sell_order = SellOrder(product_name=ofer.product_name,
                               matrix_name=ofer.company_from,
                               price_sold=ofer.price_per_unit,
                               amount_asked=ofer.count_can_supply,
                               amount_sold=msg.count_want_buy,
                               normal_price_per_unit=self.company.get_product_price(ofer.product_name),
                               to_company=msg.to_company,
                               logistic_company=msg.logistic_company,
                               to_company_tag=msg.company_from_type

                               )
        product_name = ofer.product_name
        self.company.sell(sell_order)
        count_to_supply = min(min(ofer.count_can_supply, msg.count_want_buy),
                              self.company.get_count_product_in_stock(product_name))

        response = self.make_sell_ofert_response(msg, count_to_supply)
        self.send_smg_to_a_agent(response)

        # Retornar el sell order
        return sell_order

    def recive_msg(self, msg: Message):
        # Upgradear la base de conocimiento
        self.update()

        if isinstance(msg, MessageWantProductOffer):
            return self._ask_price_product(msg)
        elif isinstance(msg, BuyOrderMessage):
            sell_order = self.going_to_sell(msg)
            # Enviar el producto
            self.deliver(sell_order)

        else:
            self.lanzar_excepcion_por_no_saber_mensaje(msg)


class ManufacturerAgent(ProducerAgent):

    def __init__(self,
                 name: str,
                 company: ManufacturerCompany,
                 env_visualizer: EnvVisualizer,

                 ):
        super().__init__(name, company, env_visualizer)
        self.company: ManufacturerAgent = company

        # Start
        self.start()

    def recive_msg(self, msg: Message):

        if isinstance(msg, HacerServicioDeDistribucion):

            pass


        else:
            self.lanzar_excepcion_por_no_saber_mensaje(msg)


class DistributorAgent(AgentWrapped):

    def __init__(self,
                 name: str,
                 company: LogisticCompany,
                 env_visualizer: EnvVisualizer,
                 ):
        super().__init__(name, company, env_visualizer)
        self.company: LogisticCompany = company

        # Start
        self.start()

        # Manager de las ofertas
        self.ofer_manager: GestorOfertas = GestorOfertas(
            self.env_visualizer.get_time)

        # guid, Respuesta de la peticion de precio

    def get_distance(self, company_from_name: str, company_destination_name: str) -> int:

        return int(self.env_visualizer.get_distance_in_the_map(company_from_name, company_destination_name))

    def create_response_msg(self, msg: HacerServicioDeDistribucion, price: float, count_to_move: int, duration: int):

        a = ResponseLogistic(
            company_from=self.company.name,
            company_from_type=self.company.tag,
            company_destination_name=msg.company_from,
            company_destination_type=msg.company_from_type,
            product_name=msg.product_name,
            count_ask_move=count_to_move,
            recibir_producto_desde_name=msg.recibir_producto_desde_name,
            recibir_producto_desde_tag=msg.recibir_producto_desde_tag,
            destino_producto_compania_nombre=msg.destino_producto_compania_nombre,
            destino_producto_compania_tag=msg.recibir_producto_desde_tag,
            price=price,
            count_can_move=count_to_move,
            end_time=duration,
            peticion_instancie=msg

        )
        self.ofer_manager.add_response_despues_de_negociar_oferta(a)
        return a

    def hacer_orden_de_servicio(self, msg: HacerServicioDeDistribucion):
        """
        Le da la oferta a la matrix y la orden de venta del servicio
         y se la envia al agente que le pidio y guarda ese contrato para
         cuando el agente de otra empresa almacen productor o manufacotr
         le pida le de el tiempo y el precio
        :param msg:
        :return:
        """
        # Factor por el que multiplicar el precio general del sericio
        factor = self.get_factor_price_to_a_client(msg.company_from, msg.product_name)
        # Distancia a recorrer
        distance = self.get_distance(msg.recibir_producto_desde_name, msg.destino_producto_compania_nombre)
        # Coste total del servicio
        total_cost = self.company.get_estimated_cost_by_distance_unit(distance) * factor
        # Duracion  del servicio
        duration_time = self.company.get_estimated_time_by_distance_unit(distance)
        # Mensje de respuesta
        response_msg = self.create_response_msg(msg, total_cost, msg.count_move, duration_time)
        # Enviar el mensaje
        self.send_smg_to_a_agent(response_msg)

    def recive_msg(self, msg: Message):

        if isinstance(msg, HacerServicioDeDistribucion):
            # Si quiere que haga
            self.hacer_orden_de_servicio(msg)


        else:
            self.lanzar_excepcion_por_no_saber_mensaje(msg)
