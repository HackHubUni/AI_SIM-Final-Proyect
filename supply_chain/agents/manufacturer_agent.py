from supply_chain.Company.companies_types.manufacturer_company import ManufacturerCompany
from supply_chain.Company.orders.Sell_order import ProduceOrder
from supply_chain.agents.Producer_Agent import *
from supply_chain.agents.Recipy_gestor import RecipeGestor


class ManufacturerAgent(ProducerAgent):

    def __init__(self,
                 name: str,
                 company: ManufacturerCompany,
                 env_visualizer: EnvVisualizer,

                 ):
        super().__init__(name, company, env_visualizer)
        self.company: ManufacturerCompany = company

        self.dict_ofert_recipe_gestor: dict[str, RecipeGestor] = {}
        """Por cada id_ oferta de produccion se guarda un gestor de oferta"""

        # Start
        self.start()

    def update_process_products(self):

        for product_name in self.company.get_produce_products:
            exp = ProduceProductWrapped(product_name)
            self.sistema_experto.add(exp)

    def update(self):

        # Llamar para upgradear mis Productos servicios
        self.update_process_products()

        super().update()

    def get_factor_price_to_a_cliente_process_product(self, from_company_name: str, product_want_name: str) -> float:
        """
        Devuelve el factor a ajustar para un cliente dado
        :param from_company_name:
        :param product_want_name:
        :return:
        """
        return self._get_a_factor_to_a_client(from_company_name, product_want_name, PedirProducirPrecio)

    def end_time_process_product_ofert(self):
        return 30000

    def send_msg_response_ofer_produce_product(self, msg: MessageWantProductProduceOffer, final_price: float):

        ingredients = self.company.stock_manager.get_product_ingredients(msg.product_want_name)
        a = ResponseOfertProduceProductMessage(
            company_from=self.company.name,
            company_from_type=self.company.tag,
            company_destination_name=msg.company_from,
            company_destination_type=msg.company_from_type,
            product_name=msg.product_want_name,
            price_per_unit=final_price,
            peticion_instance=msg,
            end_time=self.end_time_process_product_ofert(),
            list_ingredients_recipe=ingredients

        )

        # Guardar la oferta
        self.ofer_manager.add_response_despues_de_negociar_oferta(a)

        # Enviar el producto
        self.send_smg_to_a_agent(a)

    def _ask_price_produce_product(self, msg: MessageWantProductProduceOffer):

        if not msg.company_from_type == TypeCompany.Matrix:
            raise AgentException(
                f'El agente {self.name} de tipo {self.company.tag}  no puede recibir ofertas de un no matriz {msg.company_from} de tipo {msg.company_from_type}')

            # Comprobar que hay en stock este producto
        if not msg.product_want_name in self.company.get_produce_products:
            # Decirle que no  tengo

            self.sent_msg_response_ofer_cant_supply(msg)
            return

        from_company_name = msg.company_from
        product_want_name: str = msg.product_want_name

        factor_price = self.get_factor_price_to_a_cliente_process_product(from_company_name, product_want_name)

        final_price = self.company.get_price_process_product(product_want_name) * factor_price

        # Enviar la respuesta

        self.send_msg_response_ofer_produce_product(msg, final_price)

    def send_sell_order_to_the_matrix(self, msg: HacerServicioDeDistribucion, count_sell: int):
        ofer_id = msg.id_to_recive_company
        response = SellResponseMessage(
            company_from=self.company.name,
            company_from_type=self.company.tag,
            company_destination_name=msg.matrix_name,
            company_destination_type=TypeCompany.Matrix,
            ofer_id=ofer_id,
            count_want=msg.count_move,
            count_sell=count_sell,

        )
        self.send_smg_to_a_agent(response)

    def _recive_produce_ingredients_(self, msg: HacerServicioDeDistribucion):
        """
        Toma un msg de llegada de producto y o añade productos a esperar que se llene la bolsa praa crearlos con la empresa
        o si ya puede crea los productos y los envia
        :param msg:
        :return: un sell_order. buy_order
        """
        ofer_id = msg.id_to_recive_company
        # Revisar si se puede elaborar la receta

        if not ofer_id in self.dict_ofert_recipe_gestor:
            raise Exception(f'No existe la oferta {ofer_id} en el agente {self.name} y en su recipe gestor ')

        recipe_gestor = self.dict_ofert_recipe_gestor[ofer_id]

        recipe_gestor.add_list_ingredient(msg.products_instance)

        if recipe_gestor.is_already_the_recipe():
            # la los ingredientes para la receta
            products_to_recipe = recipe_gestor.get_products()
            # La orden de compra
            buy_order = recipe_gestor.buy_order
            # la instancia hecha
            ofer_instance: ResponseOfertProduceProductMessage = recipe_gestor.firts_offer

            if not isinstance(ofer_instance, ResponseOfertProduceProductMessage):
                raise Exception(
                    f' la oferta en el agente manufacturero {self.name} no es del tipo ResponseOfertProduceProductMessage ')

            # Precio normal del producto por unidad

            product_normal_price = self.company.get_price_process_product(ofer_instance.product_name)
            produce_order = ProduceOrder(
                product_name=ofer_instance.product_name,
                price_sold=ofer_instance.price_per_unit,
                amount_asked=buy_order.count_want_buy,
                amount_sold=buy_order.count_want_buy,
                normal_price_per_unit=product_normal_price,
                matrix_name=ofer_instance.company_from,
                to_company=buy_order.company_destination_name,
                logistic_company=buy_order.logistic_company,
                ingredients=products_to_recipe

            )
            # Se manda a producir
            self.company.sell_process_product(produce_order)

            # retornar la oferta y el buy_order
            sell_order = self._get_sell_order(ofer_instance, buy_order)
            return sell_order, buy_order

    def accept_product_offer(self, msg: BuyOrderMessage) -> bool:
        """Esto dice que se acepto la oferta"""

        ofer_id = msg.ofer_id

        if not self.ofer_manager.is_ofer_active(ofer_id):
            return False

        # Instanciar el gestor de las recetas para cuando se complete hacer el producto
        ofer_instance = self.ofer_manager.get_ofer_by_id(ofer_id)

        if not isinstance(ofer_instance.peticion_instance, MessageWantProductProduceOffer):
            return False

        product_name = ofer_instance.peticion_instance.product_want_name

        recipe_list = self.company.get_product_ingredients(product_name)
        # ahora se espera que lleguen productos de el
        self.dict_ofert_recipe_gestor[ofer_id] = RecipeGestor(recipe_list, buy_order=msg, firts_offer=ofer_instance)

        return True

    def recive_msg(self, msg: Message):
        if isinstance(msg, HacerServicioDeDistribucion):

            sell_order, buy_order = self._recive_produce_ingredients_(msg)

            # Enviar el producto
            self.deliver(sell_order, buy_order.time_logist, buy_order.id_contract_destination)

        elif isinstance(msg, BuyOrderMessage):

            if not self.accept_product_offer(msg):
                # Esto viene de la clase padre
                sell_order = self.going_to_sell(msg)
                # Enviar el producto
                self.deliver(sell_order, msg.time_logist, msg.id_contract_destination)

        elif isinstance(msg, MessageWantProductProduceOffer):
            self._ask_price_produce_product(msg)
        else:
            super().recive_msg(msg)