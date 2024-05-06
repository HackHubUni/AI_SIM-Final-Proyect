
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

    @property
    def this_company_name(self)->str:
        """
        Retorna el nombre de la compania matriz
        :return:
        """
        return self.company.name

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
    #self.ask_product_all_manufacturer(product_want_name)




    def ask_all_warehouses(self,product_name:str,count_want:int):
        """
        Le pregunta a todos los almacenes si tienen un producto en especifico

        :param product_name:
        :param count_want:
        :return:
        """
        for warehouse_name in self.warehouses_name:

            msg_to_ask=AskCountProductInStock(
                company_from=self.this_company_name,
                company_from_type=TypeCompany.Matrix,
                company_destination_name=warehouse_name,
                company_destination_type=TypeCompany.Warehouse,
                product_want_name=product_name
            )

            #Enviar el mensaje
            self.send_smg_to_a_agent(msg_to_ask)

    def ask_all_manufactures_sell_this_product(self,product_name:str,count_want:int):
        """
        Le pregunta a todos los manufactores si venden elaborado ese producto

        :param product_name:
        :param count_want:
        :return:

        """
        for manufactor_name in self.manufacturers_name:
            msg_to_ask=MessageWantProductOffer(
                company_from=self.this_company_name,
                company_from_type=TypeCompany.Matrix,
                company_destination_name=manufactor_name,
                company_destination_type=TypeCompany.SecondaryProvider,
                product_want_name=product_name


            )
            #Enviar el mensaje
            self.send_smg_to_a_agent(msg_to_ask)


    def ask_distributors_price(self,product_name:str,count_want:int,company_from_service_name:str,company_from_service_tag:TypeCompany,company_destination_service_name:str,company_destination_service_tag:TypeCompany):
        """
        Le pregunta a todos los manufactores si venden el producto elaborado
        :param product_name:
        :param count_want:
        :return:
        """
        for distributor_name in self.distributor_names:
            msg_to_ask=AskPriceDistributor(
                company_from=self.this_company_name,
                company_from_type=TypeCompany.Matrix,
                company_destination_name=distributor_name,
                company_destination_type=TypeCompany.Logistic,
                product_to_transport=product_name,
                service_company_from_name=company_from_service_name,
                service_company_from_tag=company_from_service_tag,
                service_company_destination_name=company_destination_service_name,
                service_company_destination_tag=company_destination_service_tag,
                count_to_transport=count_want


            )
            self.send_smg_to_a_agent(msg_to_ask)





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




    def recive_msg(self, msg: Message):

        if isinstance(msg, StoreWantRestock):
            self._store_want_restock(msg)

        elif isinstance(msg,SellResponseMessage):
            pass



        elif isinstance(msg,ResponseOfertProductMessaage):
            pass

        else:
            self.lanzar_excepcion_por_no_saber_mensaje(msg)
