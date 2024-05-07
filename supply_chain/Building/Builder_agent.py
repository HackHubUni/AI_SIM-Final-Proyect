from supply_chain.Building.Builder_base import BuilderBase
from supply_chain.Building.building_companys import BuildingProducerCompany, BuilderMatrixCompany, \
    BuilderLogisticCompany
from supply_chain.Company.companies_types.Matrix_Company import *
from supply_chain.Company.companies_types.shop_company import StoreCompany
from supply_chain.agents.Distributor_Agent import DistributorAgent
from supply_chain.agents.Producer_Agent import *
from supply_chain.agents.Store_Agent import StoreAgent
from supply_chain.agents.matrix_agent import *


class BuilderAgentsBase(BuilderBase):

    @abstractmethod
    def create_instance(self, name: str):
        """
        Crea una instancia del objeto que tiene el builder
        :return:
        """

    def create_list_instances_by_consecutive_name(self, count: int, name: str):
        """
        Crea una lista de instancias del objeto que hace build con el nombre en name_{i} ejemplo Tienda_1, Tienda_2,
        Tienda_3 ...... Tienda_"n"
        :param count:
        :param name:
        :return:


        """
        if count<1:
            raise Exception(f'Se deben de crear al menos 1 instancia no {count
            }')
        return [self.create_instance(f'{name}_{i}') for i in range(1, count + 1)]


class BuildingProducerAgent(BuilderAgentsBase):

    def __init__(self,
                 seed: int,
                 env_visualizer: EnvVisualizer,
                 get_time: Callable[[], int],

                 add_event: Callable[[SimEvent], None],
                 ):
        super().__init__(seed)
        self.get_time: Callable[[], int] = get_time
        self.add_event: Callable[[SimEvent], None] = add_event
        self.seed: int = seed
        self.env_visualizer: EnvVisualizer = env_visualizer
        self.company_builder: BuildingProducerCompany = BuildingProducerCompany(self.seed, self.add_event,
                                                                                self.get_time)

    def create_instance(self, name: str):
        company_ = self.company_builder.create_producer_company(name)
        return ProducerAgent(name, company_, self.env_visualizer)



class BuildingDistributorAgent(BuilderAgentsBase):
    def __init__(self,
                 seed: int,
                 env_visualizer: EnvVisualizer,
                 get_time: Callable[[], int],

                 add_event: Callable[[SimEvent], None],
                 ):
        super().__init__(seed)
        self.get_time: Callable[[], int] = get_time
        self.add_event: Callable[[SimEvent], None] = add_event
        self.seed: int = seed
        self.env_visualizer: EnvVisualizer = env_visualizer
        self.company_builder: BuilderMatrixCompany = BuilderMatrixCompany(self.seed, self.add_event, self.get_time)

    def create_instance(self,name:str):
        company=BuilderLogisticCompany(self.seed,self.add_event,self.get_time).create_distribution_company(name)
        return DistributorAgent(name=name,
                                company=company,
                                env_visualizer=self.env_visualizer

                                )





class BuildingMatrixAgent(BuilderBase):
    def __init__(self,
                 seed: int,
                 env_visualizer: MatrixEnvVisualizer,
                 get_time: Callable[[], int],

                 add_event: Callable[[SimEvent], None],

                 ):
        super().__init__(seed)
        self.get_time: Callable[[], int] = get_time
        self.add_event: Callable[[SimEvent], None] = add_event
        self.seed: int = seed
        self.env_visualizer: MatrixEnvVisualizer = env_visualizer
        self.company_builder: BuilderMatrixCompany= BuilderMatrixCompany(self.seed,self.add_event, self.get_time)

    def create_matrix_agent(self, name: str, store_names: list[StoreAgent]):
        company_ = self.company_builder.create_matrix_company(name)
        return MatrixAgent(name, company_, self.env_visualizer, store_names)


class Builder_Shop_Agent(BuilderAgentsBase):
    def __init__(self,
                 seed :int,
                 name:str,
                 company:StoreCompany,
                 get_time: Callable[[], int],
                 send_msg: Callable[[Message], None],
                 matrix_name: str
                 ):
        super().__init__(seed)
        self.name: str=name
        self.company: StoreCompany=company
        self.get_time: Callable[[], int]= get_time
        self.send_msg: Callable[[Message], None] = send_msg
        self.matrix_name:str = matrix_name

    def create_store_agent(self):
        return StoreAgent(self.name,self.company,self.get_time,self.send_msg,
                          self.matrix_name)
