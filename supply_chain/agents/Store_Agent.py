from typing import Callable

from supply_chain.Company.companies_types.shop_company import StoreCompany, TypeCompany
from supply_chain.Company.registrers.resgister import ShopRecord
from supply_chain.Mensajes.ask_msg import HacerServicioDeDistribucion, StoreWantRestock, Notification
from supply_chain.agent import *
from supply_chain.agents.expert_system.Sistema_experto import SistExperto


class StoreAgent(Agent):

    def update_shop(self):
        self.company.add_from_the_agent(self._shop_record,self.call_to_restock_shop)


    def __init__(
            self,

            name: str,
            company: StoreCompany,
            get_time: Callable[[], int],
            send_msg: Callable[[Message], None],
            matrix_name:str

    ) -> None:
        super().__init__(name)
        self.matrix_name: str = matrix_name
        self.company: StoreCompany = company
        self.get_time: Callable[[], int] = get_time
        self.send_msg: Callable[[Message], None] = send_msg
        self.sistema_experto: SistExperto = SistExperto()

        self._shop_record:ShopRecord=None
        """
        Record de la tienda la tiene que pasar la matrix antes de funcionar esto
        """
        self.update_thinks_from_matrix=False



    def update_from_matrix(self,shop_record:ShopRecord):
        self._shop_record=shop_record



        #Update the shop
        self.update_shop()

        self.update_thinks_from_matrix=True




    def call_to_restock_shop(self,dict_pro_count_want:dict[str,int]):
        for product_name in dict_pro_count_want.keys():
            count=dict_pro_count_want[product_name]
            #llamar a reabastecer
            self.make_order(product_name,count)


    def make_order(self, product_name: str, count_want: int):
        """ Hace una orden y se la envia a la empresa matriz"""

        msg= StoreWantRestock(
            company_from=self.company.name,
            company_destination_type=self.company.tag,
            product_want_name=product_name,
            company_destination_name=self.matrix_name,
            company_from_type=TypeCompany.Matrix,
            count_want_restock=count_want,
        )
        #Enviar el mensaje
        self.send_msg(msg)



    def restock(self,msg:HacerServicioDeDistribucion):
        """
        Se reabastece la tienda
        :param msg:
        :return:
        """
        list_products=msg.products_instance
        self.company.store_stock_manager.add_list_products(list_products)

        #Enviar mensaje a la matrix de que llegaron productos

        notification = Notification(
            company_from=self.company.name,
            company_from_type=self.company.tag,
            company_destination_name=self.matrix_name,
            company_destination_type=TypeCompany.Matrix,
            logistic_offer_id=msg.id_to_recive_company

        )

        # Enviar la notificacion de arribo a la matrix
        self.send_msg(notification)





    def recive_msg(self, msg: Message):

        if not self.update_thinks_from_matrix:
            raise Exception(f'No se puede instanciar el agente tienda {self.name} si la matrix no ha actualizado cosas')

        if isinstance(msg,HacerServicioDeDistribucion):
            self.restock(msg)
        else:
            raise Exception(f'La tienda solo pude recibir mensajes de llegar productos no de {type(msg)}')

