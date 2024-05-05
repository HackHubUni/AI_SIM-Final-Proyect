
from supply_chain.Company.companies_types.Matrix_Company import MatrixCompany
from supply_chain.agents.AgentWrapped import *
from supply_chain.agents.enviroment_visulizer import MatrixEnvVisualizer


class MatrixAgent(AgentWrapped):
    def __init__(self,
                 name: str,
                 company: MatrixCompany,
                 env_visualizer: MatrixEnvVisualizer,
                 store_names: list[str],

                 ):
        super().__init__(name, company, env_visualizer)
        self.env_visualizer: MatrixEnvVisualizer = env_visualizer
        self.company: MatrixCompany = company
        #self.planner: PlanningProblem = get_planing_Type()
        self.store_names: list[str] = store_names

    @property
    def producers_name(self) -> list[str]:
        """"
        brinda el nombre de los productores actuales
        """
        return self.env_visualizer.get_producers_name()

    @property
    def manufacturers_name(self) -> list[str]:
        """
        brinda el nombre de los manufactores actuales
        :return:
        """
        return self.env_visualizer.get_manufacturers_name()

    @property
    def warehouses_name(self) -> list[str]:
        """
        Brinda el nombre de los almacenes actuales
        :return:
        """
        return self.env_visualizer.get_warehouses_name()

    @property
    def distributor_names(self) -> list[str]:
        """
        Brinda el nombre de los distribuidores actuales
        :return:
        """
        return self.env_visualizer.get_distributor_names()

    def _store_want_restock(self, msg: StoreWantRestock):
        """
        cuando una tienda quiere hacer un restock
        :param msg:
        :return:
        """
        store_from_name = msg.company_from
        if not msg.company_from_type == TypeCompany.Store:
            raise Exception(
                f'La empresa {store_from_name} de tipo {msg.company_from_type} no puede pedir productos a la matriz {self.company.name}')

        product_want_name: str = msg.product_want_name
        self.ask_product_all_manufacturer(product_want_name)

    def _make_product_ask(self, product_name: str, company_destination_name: str, company_destination_tag: TypeCompany):
        """
        Hacer preguntas de compra de productos a manufactureras o productores

        :param product_name:
        :param company_destination_name:
        :param company_destination_tag:
        :return:
        """

        return MessageWantProductOffer(
            company_from=self.company.name,
            company_from_type=TypeCompany.Matrix,
            company_destination_name=company_destination_name,
            company_destination_type=company_destination_tag,
            product_want_name=product_name)

    def ask_product_all_manufacturer(self, product_name: str):
        """
        Preguntar a todos los manufactureros el precio y disponibilidad del producto
        :param product_name:
        :return:
        """

        for manu_names in self.producers_name:
            # Mensaje a enviar a las empresas para preguntar precio y disponibilidad
            msg = self._make_product_ask(product_name, manu_names, TypeCompany.BaseProducer)
            # Enviar mensaje a las empresas
            self.send_smg_to_a_agent(msg)

    def recive_msg(self, msg: Message):

        if isinstance(msg, StoreWantRestock):

            self._store_want_restock(msg)

        else:
            self.lanzar_excepcion_por_no_saber_mensaje(msg)
