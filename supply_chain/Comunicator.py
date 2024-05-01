from supply_chain.company import Company, TypeCompany


class Message:
    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,

                 ):
        self.company_from: str = company_from
        self.company_from_type: TypeCompany = company_from_type
        self.company_destination_name: str = company_destination_name
        self.company_destination_type: TypeCompany = company_destination_type
class MessageWantProductOffer(Message):
    """Clase para mensajes oferta"""

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


class Comunicator:

    def __init__(self,
                 productor_list: list[Company],
                 ):
        self.productor_list = productor_list

    def sent_want_product_msg(self, msg: MessageWantProductOffer):
        productor_name = msg.company_destination_name
        for productor in self.productor_list:
            if productor.name == productor_name:
        # TODO: Agregar aca  el enviar al agente
