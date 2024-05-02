from abc import ABC
from supply_chain.company import TypeCompany


class Message(ABC):
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



class DeliveryMessage(Message):

    def __init__(self,
                 company_from: str,
                 company_from_type: TypeCompany,
                 company_destination_name: str,
                 company_destination_type: TypeCompany,
                 matrix_name:str,
                 product_name:str,
                 id_destino:str,

                 ):
        super().__init__(company_from,
                         company_from_type,
                         company_destination_name,
                         company_destination_type)

        self.matrix_name: str=matrix_name
        self.product_name: str=product_name
        self.id_destino: str=id_destino




