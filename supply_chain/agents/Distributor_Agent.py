from supply_chain.agents.Producer_Agent import *


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

    def _factor_as_not_in_this_city(self):
        return 5000

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
        if factor < 0:
            factor = self._factor_as_not_in_this_city()

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
