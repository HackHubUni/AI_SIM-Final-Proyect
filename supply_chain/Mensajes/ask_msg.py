from abc import ABC

from supply_chain.Company.companies_types.distribution_company import LogisticCompany
from supply_chain.Message import Message
from supply_chain.agents.utils import generate_guid, ImplicationLogicWrapped
from supply_chain.company import Company, TypeCompany
from typing import Callable

import uuid
from typing import Callable
import heapq

from supply_chain.products.product import Product


class MessageWantProductOffer(Message):
    """Clase para mensajes ResponseOfertProductMessaage"""

    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 product_want_name: str,
                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type)
        self.product_want_name: str = product_want_name


class MessageWantProductProduceOffer(MessageWantProductOffer):
    pass


class AskPriceWareHouseCompany(MessageWantProductOffer):
    pass

class AskCountProductInStock(AskPriceWareHouseCompany):
    pass


class BuyOrderMessage(Message):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 ofer_id: str,
                 count_want: int,
                 logistic_company_name: str,
                 id_contract_logistic: str,
                 id_contract_destination: str,  # Si es una tienda poner el id en -1
                 to_company: str,
                 price_logist: float,
                 time_logist: int,

                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type)
        self.id_contract_logistic: str = id_contract_logistic
        self.ofer_id: str = ofer_id
        self.price_logist: float = price_logist
        self.time_logist: int = time_logist
        self.count_want_buy = count_want
        self.logistic_company: str = logistic_company_name
        self.to_company: str = to_company
        self.id_contract_destination: str = id_contract_destination


class SellResponseMessage(BuyOrderMessage):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 ofer_id: str,
                 count_want: int,
                 count_sell: int,
                 total_cost: int,
                 logistic_company: LogisticCompany,
                 to_company: Company

                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type,
                         ofer_id,
                         count_want)

        self.count_sell = count_sell

        self.total_cost = total_cost






class HacerServicioDeDistribucion(Message):
    def __init__(self,
                 matrix_name: str,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 product_name: str,
                 count_move: int,
                 id_to_recive_company:str,

                 time_demora_logistico: int,
                 ):
        super().__init__(company_from=company_from,
                         company_from_type=company_from_type,
                         company_destination_name=company_destination_name,
                         company_destination_type=company_destination_type,
                         )
        self.matrix_name: str = matrix_name
        self.product_name: str = product_name
        self.count_move: int = count_move
        self.products_instance: list[Product] = []
        self.time_demora_logistico: int = time_demora_logistico
        self. id_to_recive_company:str=id_to_recive_company

    def set_list_product(self, products: list[Product]):
        self.products_instance = products





