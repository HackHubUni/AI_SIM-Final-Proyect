from supply_chain.Company.companies_types.Matrix_Company import MatrixCompany
from supply_chain.Company.registrers.resgister import MatrixRecord
from supply_chain.Mensajes.gestor_peticiones import *
from supply_chain.agents.AgentWrapped import *
from supply_chain.agents.Distributor_Agent import DistributorAgent
from supply_chain.agents.Store_Agent import *
from supply_chain.agents.enviroment_visulizer import MatrixEnvVisualizer
from supply_chain.agents.manufacturer_agent import ManufacturerAgent
from supply_chain.agents.ware_house_agent import WareHouseAgente
from supply_chain.max_flow_min_cost.Optimization_choise_matrix import MatrixOptimizer


class MatrixAgent(AgentWrapped):


    def __init__(self,
                 name: str,
                 company: MatrixCompany,
                 env_visualizer: MatrixEnvVisualizer,
                 stores: list[StoreAgent],
                 get_agent_by_name: Callable[[str], Agent],

                 ):

        self.env_visualizer: MatrixEnvVisualizer = env_visualizer
        self.company: MatrixCompany = company
        #self.planner: PlanningProblem = get_planing_Type()
        self.store_names: list[str] = [store.company.name for store in stores]

        self._get_agent_by_name: Callable[[str], Agent] = get_agent_by_name

        self.stores:list[StoreAgent]=stores

        # Gestor de peticiones por cada tienda
        self.petitions_gestor: MatrixOrderGestor = MatrixOrderGestor()

        self.matrix_record = MatrixRecord(1, self.store_names, self.company.get_time)

        super().__init__(name, company, env_visualizer)

    def start(self):
        """Llamar al inicializar la simulacion"""
        self._update_my_stores()

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

    @property
    def store_agents(self) -> list[StoreAgent]:
        """
        Retorna las tiendas del agente
        :return:
        """
        return self.stores

    @property
    def stores_companys(self) -> list[StoreCompany]:
        return [a.company for a in self.store_agents]

    def _update_my_stores(self):
        """
        Upgradea las tiendas
        :return:
        """
        for store in self.stores:
            store.update_from_matrix(self.matrix_record.get_store_record(store.name), self.name)

    def get_agents_by_name(self, agent_name: str) -> AgentWrapped:
        return self._get_agent_by_name(agent_name)

    def _create_store_order_gestor(self, store_name: str, product_want_name: str, id_pedido: str):
        """
        Crea un gestor de peticiones de tiendas el id_pedido es el que tiene el msg que hace la tienda a esta matrix
        :param store_name:
        :param product_want_name:
        :param id_pedido:
        :return:
        """

        return StoreOrderGestor(store_name=store_name, product_name=product_want_name,
                                store_restock_msg_matrix_id=id_pedido)

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
        id_msg_from_store:str=msg.id_from_matrix

        store_gestor=self._create_store_order_gestor(store_from_name,product_want_name,id_msg_from_store)



        if self.petitions_gestor.is_the_order_in_the_gestor(store_gestor):
            #TODO: Aca la logica si todavia estoy procesando el pedido de la matrix
            return


        #TODO:Simular tiempo de espera


        #TODO Darme el valor que quiero rellenar:

        count_want_restock:int=msg.count_want_restock

        #Llamar a armar la cadena de suministro
        self._restock_store(store_from_name,product_want_name,count_want_restock,store_gestor)

    def crear_tag_de_la_arista_para_el_flujo(self, cost_per_unit: float, count_can_supply: int):
        """
        Crea el tag para el flujo por cada arista
        :param cost_per_unit:
        :param count_can_supply:
        :return:
        """
        return {"capacity": count_can_supply, "weight": cost_per_unit}

    def _restock_store(self,store_name:str,product_name:str,count_want:int,store_gestor:StoreOrderGestor):
        lis_to_see: list[dict[str, dict[str, float]]] = []
        #Llamar a todos los almacenes y preguntar si tienen
        dict_ware_houses_in_stock = self.ask_all_manufactures_sell_this_product(product_name, store_gestor)
        lis_to_see.append(dict_ware_houses_in_stock)
        # Preguntar a los manufactores por vender esa materia
        dict_sell_final_product_from_manufacturer = self.ask_all_manufactures_sell_this_product(product_name,
                                                                                                store_gestor)
        lis_to_see.append(dict_sell_final_product_from_manufacturer)


        optimizer=MatrixOptimizer()
        offert_acept,cost=optimizer.solve_normal_solution(store_name,count_want,lis_to_see)
        print(cost)
    def ask_all_warehouses(self, product_name: str, store_gestor: StoreOrderGestor) -> dict[str, dict[str, float]]:
        """
        Le pregunta a todos los almacenes si tienen un producto en especifico

        :param product_name:
        :param count_want:
        :return:
        """

        dic_: dict[str, dict[str, float]] = {}
        for warehouse_name in self.warehouses_name:

            msg_to_ask=AskCountProductInStock(
                company_from=self.this_company_name,
                company_from_type=TypeCompany.Matrix,
                company_destination_name=warehouse_name,
                company_destination_type=TypeCompany.Warehouse,
                product_want_name=product_name
            )

            #Guardar en el gestor de stock

            # Enviar el mensaje
            # self.send_smg_to_a_agent(msg_to_ask)
            # TOmar al agente
            agent_ = self.get_agents_by_name(warehouse_name)

            if not isinstance(agent_, WareHouseAgente):
                raise Exception(f'Se esperaba un agente Almacen no un {agent_.company.tag} con nombre {agent_.name}')

            response: ResponseStoreProductInStockNow = agent_.process_count_product_in_stock(msg_to_ask, False)

            #Logica si la respuesta es vacia
            count_can_supply=response.count_can_supply
            #Solo tomo las que tienen mas de uno
            if count_can_supply<1:
                continue

            # Llamar a los transportistas y quedarse con el mas barato

            distributor_ = self.get_the_best_distributor(product_name=product_name,
                                                         count_want=count_can_supply,
                                                         company_from_service_name=warehouse_name,
                                                         company_from_service_tag=TypeCompany.Warehouse,
                                                         company_destination_service_name=store_gestor.store_name,
                                                         company_destination_service_tag=TypeCompany.Store,
                                                         store_gestor=store_gestor,

                                                         )

            store_gestor.add_ask_from_matrix_to_another_company(response, [distributor_])

            # Pecio por unidad con respecto al transporte
            cost_per_unit = response.price_per_unit + distributor_.price
            id_=response.id_
            if warehouse_name in dic_:
                raise Exception(f'No se le puede preguntar dos veces al mismo almacen {warehouse_name}')

            dic_[id_] = self.crear_tag_de_la_arista_para_el_flujo(cost_per_unit, count_can_supply)

            # TODO:Poner aca el factor de que tan mal me cae

        return dic_

    def ask_all_manufactures_sell_this_product(self, product_name: str, store_gestor: StoreOrderGestor) -> dict[
        str, dict[str, float]]:
        """
        Le pregunta a todos los manufactores si venden elaborado ese producto

        :param product_name:
        :param count_want:
        :return:

        """
        dict_return: dict[str, dict[str, float]] = {}
        for manufactor_name in self.manufacturers_name:
            msg_to_ask=MessageWantProductOffer(
                company_from=self.this_company_name,
                company_from_type=TypeCompany.Matrix,
                company_destination_name=manufactor_name,
                company_destination_type=TypeCompany.SecondaryProvider,
                product_want_name=product_name


            )
            # Tomar el agente
            manufacturer_agent: ManufacturerAgent = self.get_agents_by_name(manufactor_name)
            response: ResponseOfertProductMessaage = manufacturer_agent.ask_price_product(msg_to_ask)

            if not isinstance(response, ResponseOfertProductMessaage):
                raise Exception(
                    f'EL mensaje de respuesta es debe ser de tipo ResponseOfertProductMessaage no de tipo {type(response)}')

            count_can_supply = response.count_can_supply

            if count_can_supply < 1:
                # TODO:AÑadir cuantos no tenian suministro

                continue

            distributor_ = self.get_the_best_distributor(product_name=product_name,
                                                         count_want=count_can_supply,
                                                         company_from_service_name=product_name,
                                                         company_from_service_tag=TypeCompany.SecondaryProvider,
                                                         company_destination_service_name=store_gestor.store_name,
                                                         company_destination_service_tag=TypeCompany.Store,
                                                         store_gestor=store_gestor,

                                                         )

            store_gestor.add_ask_from_matrix_to_another_company(response, [distributor_])

            # Añadir lo mal que me caen

            price_cost_this_option = response.price_per_unit + distributor_.price
            id_=response.id_
            dict_return[id_] = self.crear_tag_de_la_arista_para_el_flujo(price_cost_this_option,
                                                                                     count_can_supply)

        return dict_return

    def get_the_best_distributor(self,
                                 product_name: str,
                                 count_want: int,
                                 company_from_service_name: str,
                                 company_from_service_tag: TypeCompany,
                                 company_destination_service_name: str
                                 , company_destination_service_tag: TypeCompany,
                                 store_gestor: StoreOrderGestor):

        lis: list[ResponseLogistic] = self.ask_distributors_price(product_name, count_want, company_from_service_name,
                                                                  company_from_service_tag,
                                                                  company_destination_service_name,
                                                                  company_destination_service_tag, store_gestor)

        min_distributor_cost: ResponseLogistic = None

        if len(lis) < 1:
            raise Exception('No puede ser vacia la lista de transportistas')

        for response in lis:
            if min_distributor_cost is None:
                min_distributor_cost = response

            cost_now: float = min_distributor_cost.price

            if cost_now > response.price:
                min_distributor_cost = response

        if min_distributor_cost in None:
            raise Exception('El transportista optimo no puede ser vacio')

        return min_distributor_cost

    def ask_distributors_price(self, product_name: str, count_want: int, company_from_service_name: str,
                               company_from_service_tag: TypeCompany, company_destination_service_name: str,
                               company_destination_service_tag: TypeCompany, store_gestor: StoreOrderGestor) -> list[
        ResponseLogistic]:
        """
        Le pregunta a todos los manufactores si venden el producto elaborado
        :param product_name:
        :param count_want:
        :return:
        """
        lis: list[ResponseLogistic] = []
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

            #Guardar en el gestor de mensajes
            store_gestor.add_ask_from_matrix_to_another_company(msg_to_ask)

            #Enviar mensaje
            agent: DistributorAgent = self.get_agents_by_name(distributor_name)
            # Respuesta del logistico
            response: ResponseLogistic = agent.hacer_orden_de_servicio(msg_to_ask)

            lis.append(response)

            # self.send_smg_to_a_agent(msg_to_ask)
        return lis

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

        elif isinstance(msg, ResponseStoreProductInStockNow):
            #Si es respuesta de cuantos productos hay en el almacen
            pass

        elif isinstance(msg,SellResponseMessage):
            pass



        elif isinstance(msg,ResponseOfertProductMessaage):
            pass

        else:
            self.lanzar_excepcion_por_no_saber_mensaje(msg)
