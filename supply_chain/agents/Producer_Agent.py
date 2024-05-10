from supply_chain.Company.companies_types.Producer_Company import ProducerCompany
from supply_chain.Company.orders.Sell_order import SellOrder
from supply_chain.agents.AgentWrapped import *





class ProducerAgent(AgentWrapped):

    def update_products(self):
        list_products_init_ = self.company.get_name_products_in_stock_now()
        if list_products_init_ is None or len(list_products_init_)<1:
            raise Exception(f'La lista no puede ser None o vacia')
        for product_name in list_products_init_:
            product = ProductWrapped(product_name)
            # Añadir al sist experto
          #  print(product.show())
            self.sistema_experto.add(product)

    def update(self):

        # Upgradear los productos
        self.update_products()

        super().update()

    def __init__(self,
                 name: str,
                 company: ProducerCompany,
                 env_visualizer: EnvVisualizer,
                 min_time_delay=0,
                 max_time_delay=300000,

                 ):
        super().__init__(name, company, env_visualizer,min_time_delay,max_time_delay)
        self.company: ProducerCompany = company

        # Start
        #self.start()

        # guid, Respuesta de la peticion de precio

    def get_delay_time(self):
        return random.randint(self.min_delay_time,self.max_delay_time)

    def sent_msg_response_ofer_cant_supply(self, oferta: MessageWantProductOffer):
        self.sent_msg_response_ofer(oferta, 0, -1.1, self.get_delay_time())

    def get_factor_count_to_sell_producto_to_a_client(self, from_company_name: str, product_want_name: str) -> float:
        """
        Devuelve el factor a multiplicar por la cant de unidades disponibles para vender
        :param from_company_name:
        :param product_want_name:
        :return:
        """
        return self._get_a_factor_to_a_client(from_company_name, product_want_name, PedirCantidad)

    def ask_price_product(self, msg: MessageWantProductOffer):
        #Updatear las creencias
        self.update()
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

        if isinstance(factor_price,bool):
            raise Exception(f'El factor price no debe ser bool ')

        final_price = self.company.get_product_price(product_want_name) * factor_price

        # Cuantas unidades se le puede vender

        factor_to_buy = self.get_factor_count_to_sell_producto_to_a_client(from_company_name, product_want_name)
       # print(f'Factor de venta {factor_to_buy}')

        temp = self.company.stock_manager.get_count_product_in_stock(product_want_name) * factor_to_buy

        final_count_to_supply = int(temp)

        # Enviar la respuesta

        return self.sent_msg_response_ofer(msg, final_count_to_supply, final_price, self.get_delay_time(),
                                           ResponseOfertProductMessaage, False)

    def make_sell_ofert_response(self, msg: BuyOrderMessage, count_to_sell: int):
        """
        Hace los mensaje sque se le envia a la empresa por la compra
        :param msg:
        :return:
        """
        ofer_id = msg.ofer_id

        offer=self.ofer_manager.get_ofer_by_id(ofer_id)
        response = SellResponseMessage(
            company_from=self.company.name,
            company_from_type=self.company.tag,
            company_destination_name=msg.company_from,
            company_destination_type=msg.company_from_type,
            ofer_id=msg.ofer_id,
            count_want=msg.count_want_buy,
            count_sell=count_to_sell,
            total_cost=offer.price_per_unit*count_to_sell,
            logistic_company=msg.logistic_company,
            to_company=msg.to_company

        )
        return response

    def deliver(self, sell_order: SellOrder, time_transport: int, id_company_destination: str):

        a = HacerServicioDeDistribucion(
            matrix_name=sell_order.matrix_name,
            company_from=self.company.name,
            company_from_type=self.company.tag,
            company_destination_name=sell_order.to_company,
            company_destination_type=sell_order.to_company_tag,
            product_name=sell_order.product_name,
            count_move=sell_order.amount_sold,
            time_demora_logistico=time_transport,
            id_to_recive_company=id_company_destination

        )

        self.company.deliver(self.send_smg_to_a_agent, a)

    # TODO:Implementar la logica de esperar cierto tiempo para enviar

    def _get_sell_order(self, ofer: ResponseOfertProductMessaage, msg: BuyOrderMessage):
        """
        La venta
        :param ofer:
        :param msg:
        :return:
        """
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

    def going_to_sell(self, msg: BuyOrderMessage):
        """Cuando te hacen una orden de compra
          se la pasa el id que tiene el logistico para dar el tiempo
        """
        ofer_id = msg.ofer_id

        if not self.ofer_manager.is_ofer_active(ofer_id):
            # Responder con cant a vender cero no hay oferta
            response = self.make_sell_ofert_response(msg, 0)
            self.send_smg_to_a_agent(response)
        ofer: ResponseOfertProductMessaage = self.ofer_manager.get_ofer_by_id(ofer_id)
        return self._get_sell_order(ofer, msg)

    def recive_msg(self, msg: Message):
        # Upgradear la base de conocimiento
        self.update()

        # if isinstance(msg, MessageWantProductOffer):
        #    return self.ask_price_product(msg)
        # elif isinstance(msg, BuyOrderMessage):
        #    sell_order = self.going_to_sell(msg)
        #    # Enviar el producto
        #    self.deliver(sell_order, msg.time_logist, msg.id_contract_destination)

        if isinstance(msg, BuyOrderMessage):
            sell_order = self.going_to_sell(msg)
            # Enviar el producto
            self.deliver(sell_order, msg.time_logist, msg.id_contract_destination)


        else:
            self.lanzar_excepcion_por_no_saber_mensaje(msg)
