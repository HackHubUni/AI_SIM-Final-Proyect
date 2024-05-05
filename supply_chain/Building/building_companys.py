from build_stock_manager import *
from Builder_produts import *
from supply_chain.Company.companies_types.Producer_Company import ProducerCompany
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






