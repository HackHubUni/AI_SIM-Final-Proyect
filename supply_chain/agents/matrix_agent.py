from supply_chain.Company.companies_types.Matrix_Company import MatrixCompany
from supply_chain.Company.registrers.resgister import MatrixRecord
from supply_chain.CompanyConfidence import CompanyConfidence
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
        """
        Gestiona las peticiones que hace una tienda 
        """

        self.matrix_record = MatrixRecord(1, self.store_names, self.company.get_time)

        super().__init__(name, company, env_visualizer)

        self.count_want_restock = 0

    def compute_the_value_per_confidence(self, company_confidence: CompanyConfidence):
        """
        Dado el tag de confianza de una compañia devuelve un valor que debe multiplicarse el precio
        :param company_confidence:
        :return:
        """
        # Fatal = "Fatal"
        # Mal = "Mal"
        # Regular = "Regular"
        # Bien = "Bien"
        # MuyBien = "Muy_bien"
        # Excelente = "Excelente"

        if company_confidence == CompanyConfidence.Excelente:
            return 0.5
        if company_confidence == CompanyConfidence.MuyBien:
            return 0 * 8
        if company_confidence == CompanyConfidence.Bien:
            return 1
        if company_confidence == CompanyConfidence.Mal:
            return 1.5
        if company_confidence == CompanyConfidence.Fatal:
            return 2



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

        if not self.petitions_gestor.can_process_this_store_order(store_from_name, product_want_name):
            # TODO: Aca la logica si todavia estoy procesando el pedido de la matrix
            return

        id_msg_from_store: str = msg.id_from_matrix

        store_gestor = self.petitions_gestor.create_store_order_gestor(store_from_name, product_want_name,
                                                                       id_msg_from_store)





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

    def make_buy_order_msg_and_send(self,
                                    company_destination_name: str
                                    , company_destination_tag: TypeCompany
                                    , offer_id: str
                                    , count_want: int,
                                    id_contact_destination: str,
                                    company_destination_the_product: str,
                                    time_logistic: int
                                    ):

        """
        Crea y envia una orden de compra a alguien
        :param company_destination_name:
        :param company_destination_tag:
        :param offer_id:
        :param count_want:
        :param id_contact_destination:
        :param company_destination_the_product:
        :param time_logistic:
        :return:
        """

        msg = BuyOrderMessage(

            company_from=self.company.name,
            company_from_type=TypeCompany.Matrix,
            company_destination_name=company_destination_name,
            company_destination_type=company_destination_tag,
            ofer_id=offer_id,
            count_want=count_want,
            logistic_company_name="Alguna",
            id_contract_logistic='0',
            id_contract_destination=id_contact_destination,
            to_company=company_destination_the_product,
            price_logist=-1,
            time_logist=time_logistic

        )

        self.send_smg_to_a_agent(msg)

    def make_buy_order_from_manufufactuer_or_ware_house_finale_products_to_store(self, ofer: Oferta,
                                                                                 logistic_ofer: ResponseLogistic,
                                                                                 count_want: int):
        """
        Llamar al almacen o al manufacturero para comprar x cant de productos finales
        :param ofer:
        :param logistic_ofer:
        :param count_want:
        :return:
        """
        self.make_buy_order_msg_and_send(
            company_destination_name=ofer.company_from,
            company_destination_tag=ofer.company_from_type,
            offer_id=ofer.id_,
            count_want=count_want,
            id_contact_destination='-1',
            company_destination_the_product=logistic_ofer.destino_producto_compania_nombre,
            time_logistic=logistic_ofer.end_time

        )

    def response_ware_house_or_manufacter_buy_final_product(self,
                                                            ofer: Oferta,
                                                            logistic_ofer: ResponseLogistic,

                                                            count_want: int,
                                                            store_gestor: StoreOrderGestor):
        """
        Decirle a una empresa almacen x que me suppla tal cant de productos
        :param ofer:
        :return:
        """

        if not isinstance(ofer, ResponseOfertProductMessaage) and not issubclass(type(ofer),
                                                                                 ResponseOfertProductMessaage):
            raise Exception(f'ofer {ofer} debe ser de tipo  ResponseStorageProductOffer no de {type(ofer)}')

        id_from_store = store_gestor.store_restock_msg_matrix_id

        self.matrix_record.add_buy_record(
            store_want_product_id=id_from_store,
            store_to_supply=store_gestor.store_name,
            order_supply_store_id=id_from_store,

            company_make_buss_name=ofer.company_from,
            company_make_buss_type=ofer.company_from_type,
            company_destination_process_name=logistic_ofer.destino_producto_compania_nombre,
            company_destination_process_type=logistic_ofer.destino_producto_compania_tag,

            product_buy_name=ofer.product_name,
            product_count_buy=count_want,

            time_process_the_buy_order=self.time + logistic_ofer.delivery_time,
            price_cost_per_unit=ofer.price_per_unit + logistic_ofer.price,
            logistic_name=logistic_ofer.company_from

        )
        self.make_buy_order_from_manufufactuer_or_ware_house_finale_products_to_store(ofer, logistic_ofer, count_want)

    def response_ware_house_or_buy_final_product_manufacturer(self, to_accept: dict[str, int],
                                                              store_gestor: StoreOrderGestor):
        # Por cada respuesta a aceptar

        for key in to_accept:
            count = to_accept[key]

            pip_line = store_gestor.get_to_acept_offer_pipe_line(key)

            company_sell = pip_line[0]

            distributor = pip_line[1]

            if len(pip_line) != 2:
                raise Exception(f'El pip line de los almacenes y los logisticos debe de tener un distribuidor')

            self.response_ware_house_or_manufacter_buy_final_product(company_sell, distributor, count, store_gestor)













    def _restock_store(self,store_name:str,product_name:str,count_want:int,store_gestor:StoreOrderGestor):
        lis_to_see: list[dict[str, dict[str, float]]] = []
        #Llamar a todos los almacenes y preguntar si tienen
        dict_ware_houses_in_stock = self.ask_all_warehouses(product_name, store_gestor)
        lis_to_see.append(dict_ware_houses_in_stock)
        # Preguntar a los manufactores por vender esa materia
        dict_sell_final_product_from_manufacturer = self.ask_all_manufactures_sell_this_product(product_name,
                                                                                                store_gestor)
        lis_to_see.append(dict_sell_final_product_from_manufacturer)


        optimizer=MatrixOptimizer()
        offert_acept,cost=optimizer.solve_normal_solution(store_name,count_want,lis_to_see)
        self.response_ware_house_or_buy_final_product_manufacturer(offert_acept, store_gestor)


    def ask_all_warehouses(self, product_name: str, store_gestor: StoreOrderGestor) -> dict[str, dict[str, float]]:
        """
         Le pregunta a todos los almacenes si tienen un producto en especifico
        :param product_name:
        :param store_gestor:
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
                                                         company_from_service_name=manufactor_name,
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
        """
        De todas las ofertas de transportistas toma la mejor de todas
        :param product_name:
        :param count_want:
        :param company_from_service_name:
        :param company_from_service_tag:
        :param company_destination_service_name:
        :param company_destination_service_tag:
        :param store_gestor:
        :return:
        """

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

        if min_distributor_cost is None:
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

    def _process_notificacion(self, msg: Notification):
        """
        Procesa una notificación de que una tienda llego algo
        :param msg:
        :return:
        """

        store_name: str = msg.company_from
        company_from_tag: TypeCompany = msg.company_from_type
        products_names: list[str] = msg.products_names

        if company_from_tag != TypeCompany.Store:
            raise Exception(
                f'Solo pueden llegar notificaciones de tiendas no de {company_from_tag} de la empresa {store_name}')
        if products_names is None or len(products_names) < 1 or not all(x == products_names[0] for x in products_names):
            raise Exception(f'No se recibieron los productos correctos {products_names}')

        if self.petitions_gestor.can_process_this_store_order(store_name, products_names[0]):
            # Eso implica que ya se puede rralizar un pedido osea que no se debe eliminar dado que no existe store order
            return
        self.petitions_gestor.delete_store_order(store_name, products_names[0])

    def recive_msg(self, msg: Message):

        if isinstance(msg, StoreWantRestock):
            self._store_want_restock(msg)
            self.count_want_restock += 1
        # print(f'La tienda {msg.company_from} en el pedido{self.count_want_restock}')

        elif isinstance(msg, Notification):
            # LLega la notificacion de una tienda de que un pedido ha llegado
            # Se pasa a que puede enviarse mas producto
            self._process_notificacion(msg)
