from build_stock_manager import *
from Builder_produts import *
from supply_chain.Company.companies_types.Producer_Company import ProducerCompany
from supply_chain.Company.companies_types.distribution_company import LogisticCompany
from supply_chain.Company.companies_types.shop_company import StoreCompany
from supply_chain.Company.stock_manager.productor_stock_manager import *
from supply_chain.Company.companies_types.Matrix_Company import *
class BuildingProducerCompany(BuilderBase):

    def __init__(self,
                 seed:int,
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],
                 ):
        super().__init__(seed)
        self.add_event: Callable[[SimEvent], None]=add_event
        self.get_time: Callable[[], int]=get_time
        self._product_builder:ExampleBuilderProduct=ExampleBuilderProduct(seed)



    def get_lambda_base_products(self):
        return self._product_builder.create_dict_base_products()

    def _create_Producer_stock_manager(self)->ProductorCompanyStock:
       return BuildProductorStockManager(
            create_product_lambda=self.get_lambda_base_products(),
            list_products_can_sell_name=list(self.get_lambda_base_products().keys()),
            add_event=self.add_event,
            get_time=self.get_time,
            seed=self.seed,


        ).create_ProductorStockManager()



    def create_producer_company(self,name:str):

        return ProducerCompany(
            name=name,
            get_time=self.get_time,
            add_event=self.add_event,
            stock_manager=self._create_Producer_stock_manager()

        )





class BuilderMatrixCompany(BuilderBase):

    def __init__(self,
                 seed:int,
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],
                 ):
        super().__init__(seed)
        self.add_event: Callable[[SimEvent], None]=add_event
        self.get_time: Callable[[], int]=get_time


    def create_matrix_company(self):

        return MatrixCompany("Macdonals",self.get_time,self.add_event)




class BuilderLogisticCompany(BuilderBase):

    def __init__(self,
                 seed:int,
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],
                 min_time:int,
                 max_time:int,
                 min_price:int,
                 max_price:int,

                 ):
        super().__init__(seed)
        self.add_event: Callable[[SimEvent], None]=add_event
        self.get_time: Callable[[], int]=get_time
        self.min_time:int=min_time
        self.max_time:int=max_time
        self.min_price:int=min_price
        self.max_price:int=max_price


    def create_distribution_company(self,name:str):

        return LogisticCompany(name,self.get_time,
                               self.add_event,lambda x: self.get_random_int(self.min_price,self.max_price)*x,
                               lambda x: self.get_random_int(self.min_time,self.max_time)*x)

class BuilderStoreCompany(BuilderBase):

    def __init__(self,
                 seed:int,
                 list_products_name:List[str],
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],
                 tasa_de_ocurrencia:int
                 ):
        super().__init__(seed)
        self.list_products_name:List[str]=list_products_name
        self.add_event: Callable[[SimEvent], None]=add_event
        self.get_time: Callable[[], int]=get_time
        self.tasa_de_ocurrencia:int=tasa_de_ocurrencia


    def next_client_distribution(self):
          # La tasa de ocurrencia. Ajusta este valor según tus necesidades.
        return np.random.poisson(self.tasa_de_ocurrencia)

    def _create_store_stock_manager(self)->ShopStockManager:
       return BuilderStoreStockManager(self.list_products_name,self.add_event,
                                       self.get_time).create_store_stock_manager()
    def create_StoreCompany(self, name:str)->StoreCompany:

        return StoreCompany(name,self.get_time,
                               self.add_event,lambda : self.next_client_distribution(),
                              self._create_store_stock_manager())