from supply_chain.Building.Builder_base import BuilderBase
from supply_chain.Building.Builder_produts import ExampleBuilderProduct
from supply_chain.Building.building_companys import BuildingProducerCompany, BuilderMatrixCompany, \
    BuilderLogisticCompany, BuilderStoreCompany, BuildingWareHouseCompany, TypeProduction, BuildingManufacturerCompany
from supply_chain.Company.companies_types.Matrix_Company import *
from supply_chain.agents.Producer_Agent import *
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


class BuildingManufacturerAgent(BuilderBase):
    def __init__(self, seed: int,
                 env_visualizer: EnvVisualizer,
                 get_time: Callable[[], int],
                 add_event: Callable[[SimEvent], None],
                 ):
        super().__init__(seed)

        self.env_visualizer: EnvVisualizer = env_visualizer
        self.get_time: Callable[[], int] = get_time
        self.add_event: Callable[[SimEvent], None] = add_event
        self.ExampleBuilderProduct = ExampleBuilderProduct(seed)

    def _get_list_manufcture_products_name(self) -> list[str]:
        return self.ExampleBuilderProduct.get_finals_products_names()

    def _get_list_base_products_need(self) -> list[str]:
        return self.ExampleBuilderProduct.get_list_base_products_names()

    def _get_create_final_product_lambda(self):
        return self.ExampleBuilderProduct.create_dict_final_products()

    def create_manufacturer_agent(self, name: str,

                                  min_product_amount: int = 100,
                                  min_stock_random: int = 3000,
                                  max_stock_random: int = 9000,
                                  min_price: int = 50,
                                  max_price: int = 200,
                                  distribution_min_supply: int = 1,
                                  distribution_max_supply: int = 60,
                                  min_time_restock: int = 60 * 60 * 24,
                                  max_time_restock: int = 60 * 60 * 120,

                                  min_restock: int = 100,
                                  max_restock: int = 50000,

                                  ):
        company = BuildingManufacturerCompany(self.seed, self.get_time, self.add_event)

        company = company.create_instance(name=name,
                                          list_manufactore_products=self._get_list_manufcture_products_name(),
                                          list_base_products=self._get_list_base_products_need(),
                                          list_sale_products=self._get_list_manufcture_products_name(),
                                          create_product_lambda=self._get_create_final_product_lambda(),

                                          get_time=self.get_time,
                                          min_product_amount=min_product_amount,
                                          min_stock_random=min_stock_random,
                                          max_stock_random=max_stock_random,
                                          min_price=min_price,
                                          max_price=max_price,
                                          distribution_min_supply=distribution_min_supply,
                                          distribution_max_supply=distribution_max_supply,
                                          min_time_restock=min_time_restock,
                                          max_time_restock=max_time_restock,

                                          min_restock=min_restock,
                                          max_restock=max_restock
                                          )

        return ManufacturerAgent(name=name, company=company, env_visualizer=self.env_visualizer)



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


class BuilderShopAgent(BuilderBase):
    def __init__(self,
                 seed: int,
                 name: str,
                 company: StoreCompany,
                 get_time: Callable[[], int],
                 send_msg: Callable[[Message], None],
                 matrix_name: str
                 ):
        super().__init__(seed)
        self.name: str = name
        self.company: StoreCompany = company
        self.get_time: Callable[[], int] = get_time
        self.send_msg: Callable[[Message], None] = send_msg
        self.matrix_name: str = matrix_name

    def create_store_agent(self):
        return StoreAgent(self.name, self.company, self.get_time, self.send_msg,
                          self.matrix_name)


class BuildingWareHouseAgent(BuilderBase):
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
        self.company_builder: BuildingWareHouseCompany = BuildingWareHouseCompany(seed, add_event, get_time)

    def get_ware_house_agent(self,
                             name: str,
                             matrix_name: str,
                             type_production: TypeProduction,
                             if_is_random_merge_the_factor: int = 3,
                             min_stock_random: int = 500,
                             max_stock_random: int = 6000,
                             company_magic_stock_min_random: int = 300,
                             company_magic_stock_max_random: int = 3500,
                             company_time_stock_min_time: int = 60 * 60 * 24,
                             company_time_stock_max_time: int = 60 * 60 * 24 * 3,
                             company_price_min_restock: int = 20,
                             company_price_max_restock: int = 650

                             ):
        company = self.company_builder.create_company(name,
                                                      matrix_name,
                                                      type_production,
                                                      if_is_random_merge_the_factor,
                                                      min_stock_random,
                                                      max_stock_random,
                                                      company_magic_stock_min_random,
                                                      company_magic_stock_max_random,
                                                      company_time_stock_min_time,
                                                      company_time_stock_max_time,
                                                      company_price_min_restock,
                                                      company_price_max_restock)

        return WareHouseAgente(name, company, self.env_visualizer)



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

    def create_matrix_agent(self, name: str, stores: list[StoreAgent],
                            get_agent_by_name: Callable[[str], AgentWrapped]):
        company_ = self.company_builder.create_matrix_company(name)
        return MatrixAgent(name, company_, self.env_visualizer, stores, get_agent_by_name)

    def _create_store_company(self, lambda_distribution: int, store_name: str):
        finals_producs_names = ExampleBuilderProduct(self.seed).get_finals_products_names()
        store = BuilderStoreCompany(self.seed
                                    , self.add_event, self.get_time, lambda_distribution,
                                    finals_producs_names
                                    ).create_StoreCompany(store_name)

        return store

    def _create_store_agent(self, shop_agent_name:str,matrix_name,lambda_distribution:int):
        return BuilderShopAgent(self.seed,
                                shop_agent_name,

                                                       self._create_store_company(lambda_distribution,shop_agent_name),
                                                       self.get_time,
                                                       self.env_visualizer.send_msg,
                                                       matrix_name
                                                       ).create_store_agent()

    def create_matrix_for_experiment(self, matrix_name: str, count_normal_stores: int,
                                     lambda_normal_stores: int,
                                     count_event_store: int,
                                     lambda_event_stores: int,
                                     get_agent_by_name: Callable[[str], AgentWrapped]

                                     ):
        """
        Crea una matrix para el experimento con sus propias tiendas
        :param matrix_name: Nombre de la matrix
        :param count_normal_stores: Cant de tiendas normales
        :param lambda_normal_stores: El valor que tiene el lambda de la variable aleatoria para situacion normal
        :param count_event_store: Cant de tiendas influenciadas por el evento
        :param lambda_event_stores: El valor que tiene el lambda de la variable aleatoria para el evento
        :param get_agent_by_name: Lambda que dado un nombre de un agente le devuelve un agente por nombre
        :return:
        """
        lis_normal_stores:list[StoreAgent] = []

        for i in range(1, count_normal_stores + 1):
            name = f'Normal_Shop_{i}'

            lis_normal_stores.append(self._create_store_agent(name,matrix_name,lambda_normal_stores))

        lis_event_stores: list[StoreAgent] = []

        for i in range(1, count_event_store + 1):
            name = f'Event_Shop_{i}'

            lis_event_stores.append(self._create_store_agent(name, matrix_name, lambda_event_stores))
        company_ = self.company_builder.create_matrix_company(matrix_name)
        stores_list=lis_event_stores+lis_normal_stores
        if len(stores_list) < 1:
            raise Exception(f'La lista de tiendas no puede estar vacia')
        return MatrixAgent(matrix_name, company_, self.env_visualizer, stores_list, get_agent_by_name)
