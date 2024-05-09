from supply_chain.Building.Builder_produts import *
from supply_chain.Building.build_stock_manager import *
from supply_chain.Company.companies_types.Matrix_Company import *
from supply_chain.Company.companies_types.Producer_Company import ProducerCompany
from supply_chain.Company.companies_types.Warehouse_Company import WarehouseCompany
from supply_chain.Company.companies_types.distribution_company import LogisticCompany
from supply_chain.Company.companies_types.manufacturer_company import ManufacturerCompany
from supply_chain.Company.companies_types.shop_company import StoreCompany
from supply_chain.Company.stock_manager.productor_stock_manager import *


class TypeProduction(Enum):
    OnlyBaseProducts = 1,
    # RandomOnlyBaseProducts = 5,

    OnlyFinalProducts = 2,
    # RandomOnlyBaseFinal = 6,
    # Toma los dos
    Blended = 3,
    # Toma de los dos
    RandomBlended = 4


class BuildingWareHouseCompany(BuilderBase):

    def __init__(self,
                 seed: int,
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],
                 ):
        super().__init__(seed)
        self.add_event: Callable[[SimEvent], None] = add_event
        self.get_time: Callable[[], int] = get_time
        self._product_builder: ExampleBuilderProduct = ExampleBuilderProduct(seed)

    def _merge_random_elements(self, dict1, dict2, num_elements):
        keys = list(dict1.keys()) + list(dict2.keys())
        new_dict = {}

        for _ in range(num_elements):
            key = random.choice(keys)
            new_dict[key] = dict1.get(key, dict2.get(key))

        return new_dict

    # Ejemplo de uso

    def _get_create_product_lambda(self, type_Production: TypeProduction):
        if type_Production == TypeProduction.OnlyBaseProducts:
            return self._product_builder.create_dict_base_products()
        if type_Production == TypeProduction.OnlyFinalProducts:
            return self._product_builder.create_dict_final_products()
        if type_Production == TypeProduction.Blended:
            return self._product_builder.create_dict_final_products() | self._product_builder.create_dict_base_products()
        if type_Production == TypeProduction.RandomBlended:
            return self._merge_random_elements(self._product_builder.create_dict_final_products(),
                                               self._product_builder.create_dict_base_products(),3)

    def create_company(self,
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

        create_product_lambda = self._get_create_product_lambda(
            type_production)
        stock_manager = BuildWareHouseStockManager(
            min_stock_random=min_stock_random,
            max_stock_random=max_stock_random,
            company_price_max_restock=company_price_max_restock,
            company_price_min_restock=company_price_min_restock,
            company_time_stock_min_time=company_time_stock_min_time,
            company_time_stock_max_time=company_time_stock_max_time,
            company_magic_stock_min_random=company_magic_stock_min_random,
            company_magic_stock_max_random=company_magic_stock_max_random,
            add_event=self.add_event,
            get_time=self.get_time,
            seed=self.seed,
            products_name=self._product_builder.get_finals_products_names()+self._product_builder.get_list_base_products_names(),
            matrix_names=[matrix_name],
            create_product_lambda=create_product_lambda,

        ).get_ware_house_stock_manager()

        return WarehouseCompany(name, self.get_time, self.add_event, stock_manager)


class BuildingProducerCompany(BuilderBase):

    def __init__(self,
                 seed:int,
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],
                 ):
        super().__init__(seed)
        self.add_event: Callable[[SimEvent], None] = add_event
        self.get_time: Callable[[], int] = get_time
        self._product_builder: ExampleBuilderProduct = ExampleBuilderProduct(seed)



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

    def create_matrix_company(self, name: str):
        return MatrixCompany(name, self.get_time, self.add_event)




class BuilderLogisticCompany(BuilderBase):

    def __init__(self,
                 seed:int,
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],
                 min_time:int=60*60*3,
                 max_time:int=60*60*10,
                 min_price:int=10,
                 max_price:int=500,

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


class BuildingManufacturerCompany(BuilderBase):

    def __init__(self,
                 seed: int,
                 get_time: Callable[[], int],
                 add_event: Callable[[SimEvent], None],

                 ):
        super().__init__(seed)
        self.get_time: Callable[[], int] = get_time
        self.add_event: Callable[[SimEvent], None] = add_event

    def create_instance(self, name: str,
                        list_manufactore_products: list[str],
                        list_base_products: list[str],
                        list_sale_products: list[str],
                        create_product_lambda: Dict[str, Callable[[int], List[Product]]],
                        get_time: Callable[[], int],
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
        stock_manager = BuildingManufacterStockManager(
            list_manufactore_products=list_manufactore_products,
            list_base_products=list_base_products,
            list_sale_products=list_sale_products,
            create_product_lambda=create_product_lambda,
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
            max_restock=max_restock,

            seed=self.seed,
            add_event=self.add_event


        ).create_ManufactureStock()

        return ManufacturerCompany(name=name,
                                   get_time=self.get_time,
                                   add_event=self.add_event,
                                   stock_manager=stock_manager
                                   )



class BuilderStoreCompany(BuilderBase):

    def __init__(self,
                 seed:int,
                 add_event: Callable[[SimEvent], None],
                 get_time: Callable[[], int],
                 tasa_de_ocurrencia: int,
                 list_products_name: List[str]
                 ):
        super().__init__(seed)
        self.list_products_name:List[str]=list_products_name
        self.add_event: Callable[[SimEvent], None]=add_event
        self.get_time: Callable[[], int]=get_time
        self.tasa_de_ocurrencia:int=tasa_de_ocurrencia
        self._product_builder: ExampleBuilderProduct = ExampleBuilderProduct(seed)

    def get_dict_lambda_finals_products(self) -> dict[str, Callable[[int], list[Product]]]:
        return self._product_builder.create_dict_final_products()

    def next_client_distribution(self):
          # La tasa de ocurrencia. Ajusta este valor según tus necesidades.
        return np.random.poisson(self.tasa_de_ocurrencia)

    def _create_store_stock_manager(self)->ShopStockManager:
        return BuilderStoreStockManager(self.list_products_name,
                                        self.add_event,
                                        self.get_time,
                                        self.get_dict_lambda_finals_products(),
                                        self.seed).create_ShopStockManager()
    def create_StoreCompany(self, name:str)->StoreCompany:
        """
        Darme una instancia de una tienda dando su nombre
        :param name:
        :return:
        """
        return StoreCompany(name,
                            self.get_time,
                            self.add_event,
                            lambda: self.next_client_distribution(),
                            self._create_store_stock_manager(),
                            )

