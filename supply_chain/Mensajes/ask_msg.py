from supply_chain.Message import Message
from supply_chain.company import TypeCompany

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
    """
    Preguntar al agente alamacen cuanto productos tiene de una compañia matriz
    """
    pass


class StoreWantRestock(MessageWantProductOffer):
    """
    Pedir a la matriz reabastecerse
    """

    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 product_want_name: str,
                 count_want_restock: int
                 ):
        self.company_from: str = company_from
        self.company_from_type: TypeCompany = company_from_type
        self.company_destination_name: str = company_destination_name
        self.company_destination_type: TypeCompany = company_destination_type
        self.product_want_name: str = product_want_name
        self.count_want_restock: int = count_want_restock




class AskPriceDistributor(Message):
    """
    Clase para preguntarle el precio por servicio desde la empresa matriz al distribuidor
    """

    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 product_to_transport: str,
                 count_to_transport:int,
                 service_company_from_name: str,
                 service_company_from_tag: TypeCompany,
                 service_company_destination_name: str,
                 service_company_destination_tag: TypeCompany,
                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type)
        self.product_to_transport: str = product_to_transport
        """
        Producto a transportar
        """
        self.service_company_from_name: str = service_company_from_name
        """
        Compañia desde la cual partiría el servicio osea se recoge el producto
        """
        self.service_company_from_tag: TypeCompany = service_company_from_tag
        """
        Tipo de compania donde se recoge el producto
        """
        self.service_company_destination_name: str = service_company_destination_name
        """
        Nombre de la compañia donde se entrega el producto
        """
        self.service_company_destination_tag: TypeCompany = service_company_destination_tag
        """
        Tipo de la compañia donde se entrega el producto
        """
        self.count_to_transport:int=count_to_transport
        """
        Cant del producto a transportar
        
        """





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


class Notification(Message):
    """
    Clase para que las tiendas notifiquen  a su matrix que llego una mercancia
    """
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 ofer_id: str,
                 count_enter: int,
                 logistic_company: str,
                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type, )
        self.ofer_id: str=ofer_id
        self.count_enter: int=count_enter
        self.logistic_company: str=logistic_company



class SellResponseMessage(Notification):
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 ofer_id: str,
                 count_want: int,
                 count_sell: int,
                 total_cost: float,
                 logistic_company:str,
                 to_company:str

                 ):

        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type,
                         ofer_id,
                         count_sell,
                         logistic_company



                         )

        self.ofer_id: str=ofer_id
        self.count_want: int=count_want

        self.count_sell = count_sell

        self.total_cost = total_cost

        self.logistic_company: str=logistic_company
        self.to_company: str=to_company






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
        """
        Nombre de la empresa matriz que lo envia
        """
        self.product_name: str = product_name
        """
        Producto a distribuir
        """

        self.count_move: int = count_move
        """
        Cantidad de producto a distribuir
        """

        self.products_instance: list[Product] = []
        """
        Instancia de los prodcutos
        """

        self.time_demora_logistico: int = time_demora_logistico
        self. id_to_recive_company:str=id_to_recive_company

    def set_list_product(self, products: list[Product]):
        self.products_instance = products





