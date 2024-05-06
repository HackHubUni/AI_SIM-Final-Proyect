from abc import ABC

from supply_chain.agents.utils import generate_guid
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

        self.id_from_matrix=generate_guid()
        """
        Id para que la matriz registre todos los valores 
        """





