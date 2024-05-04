from supply_chain.Mensajes.offer_msg import *
from supply_chain.Mensajes.ask_msg import *
from supply_chain.agent import Agent, AgentException
from supply_chain.agents.Sistema_experto import SistExperto
from supply_chain.agents.enviroment_visulizer import EnvVisualizer
from supply_chain.agents.utils import *
from supply_chain.Company.companies_types.Producer_Company import *



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

    def get_time_demora(self):
        return 300000

    def _get_a_factor_to_a_client(self, from_company_name: str, product_want_name: str,
                                  class_type: PedirPrecio | PedirCantidad | PedirBase):
        """Metodo base para que se pueda pedir factor para suplir de pedido y cant de factor de precio"""
        # Ahora pedir el factor del precio
        price_ask = class_type(from_company_name, product_want_name, "z")
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

    def sent_msg_response_ofer(self, oferta: MessageWantProductOffer | AskPriceWareHouseCompany, count_can_supply: int,
                               price_per_unit: float, time_demora,
                               instance=ResponseOfertProductMessaage):

        response = instance(company_from_type=self.company.tag,
                            company_from=self.company.name,
                            company_destination_type=oferta.company_from_type,
                            company_destination_name=oferta.company_from,
                            product_name=oferta.product_want_name,
                            price_per_unit=price_per_unit,
                            count_can_supply=count_can_supply,
                            peticion_instance=oferta,
                            end_time=time_demora

                            )

        self.ofer_manager.add_response_despues_de_negociar_oferta(response)

        # Enviar
        self.send_smg_to_a_agent(response)

    @abstractmethod
    def recive_msg(self, msg: Message):
        pass

    def update_implications(self):

        for implication in self.logic_implication:
            print(implication.show())
            self.sistema_experto.add(implication)
