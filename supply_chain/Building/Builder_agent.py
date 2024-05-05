from supply_chain.Building.Builder_base import BuilderBase
from supply_chain.Building.building_companys import BuildingProducerCompany, BuilderMatrixCompany
from supply_chain.Company.companies_types.Matrix_Company import *
from supply_chain.agents.Producer_Agent import *
from supply_chain.agents.matrix_agent import *


class BuildingProducerAgent(BuilderBase):

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

    def create_Producer_Agent(self, name: str):
        company_ = self.company_builder.create_producer_company(name)
        ProducerAgent(name, company_, self.env_visualizer)


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


    def create_matrix_agent(self, name: str, store_names: list[str]):
        company_ = self.company_builder.create_matrix_company()
        return MatrixAgent(name, company_, self.env_visualizer, store_names)
