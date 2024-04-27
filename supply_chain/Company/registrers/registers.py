from supply_chain.Company.registrers.product_history import ProductRecords

try:
    from supply_chain.company import TypeCompany
except:
    pass


class Registry:
    """This is the class for store useful information of the simulation"""

    def __init__(self) -> None:
        self.sell_registry: dict[int, list[SellRecord]] = {}
        """Stores the sell records of the entire simulation"""
        self.stock_registry: dict[int, dict[str, StockRecord]] = {}
        """Stores the stock records of the entire simulation"""
        self.buy_registry: dict[int, BuyRecord] = {}
        """Stores the buy records of the entire simulation"""
        self.balance_registry: dict[int, BalanceRecord] = {}
        """Stores the balance records of the store in the entire simulation"""
        self.pay_holding_registry: dict[int, PayHoldingRecord] = {}
        """Stores all payments made by the store to the storage service"""

    def add_sell_record(self,
                        time: int,
                        product_name: str,
                        list_products_records: list[ProductRecords],
                        normal_price: float,
                        price_sold: float,
                        amount_asked: int,
                        amount_sold: int,
                        matrix_name: str,
                        from_company_name: str,
                        from_company_tag: TypeCompany,
                        to_company_name: str,
                        to_company_tag: TypeCompany
                        ):
        """Create a SellRecord and stores it in the sell_registry"""
        record = SellRecord(time,
                            product_name=product_name,
                            list_products_record=list_products_records,
                            normal_price=normal_price,
                            price_sold=price_sold,
                            amount_asked=amount_asked,
                            amount_sold=amount_sold,
                            matrix_name=matrix_name,
                            from_company_name=from_company_name,
                            from_company_tag=from_company_tag,
                            to_company_name=to_company_name,
                            to_company_tag=to_company_tag

                            )
        sell_list = self.sell_registry.setdefault(time, [])
        sell_list.append(record)
        self.sell_registry.update()

    def add_stock_record(self, time: int, amount: int, product_name: str):
        """Create a StockRecord and stores it in the stock_registry"""
        actual_stock = self.stock_registry.get(time, None)
        if actual_stock:
            self.stock_registry[time].amount = amount
        else:
            self.stock_registry[time] = StockRecord(time, amount, product_name)

    def add_buy_record(self, time: int, amount: int, cost: int):
        """Create a BuyRecord and stores it in the buy_registry"""
        record = BuyRecord(time, amount, cost)
        self.buy_registry[time] = record

    def add_balance_record(self, time: int, balance: float):
        """Create a BalanceRecord and stores it in the balance_registry"""
        actual_balance = self.balance_registry.get(time)
        if actual_balance:
            self.balance_registry[time].balance = balance
        else:
            self.balance_registry[time] = BalanceRecord(time, balance)

    def add_pay_holding_record(self, time: int, cost: float):
        """Create a PayHoldingRecord and stores it in the pay_holding_registry"""
        record = PayHoldingRecord(time, cost)
        self.pay_holding_registry[time] = record


class Record:
    """Base class for all the information records of the simulation"""

    def __init__(self, time: int = 0) -> None:
        self.time = time


class SellRecord(Record):
    """This record store information about the sell of products at a time"""

    def __init__(self, time: int,
                 product_name: str,
                 list_products_record: list[ProductRecords],
                 normal_price: float,
                 price_sold: float,
                 amount_asked: int,
                 amount_sold: int,
                 matrix_name: str,
                 from_company_name: str,
                 from_company_tag: TypeCompany, to_company_name: str, to_company_tag: TypeCompany) -> None:
        super().__init__(time)
        self.product_name: str = product_name
        """
        The name of the product
        """
        self.list_products_record = list_products_record

        self.amount_asked: int = amount_asked
        """The units that the client asked to buy"""
        self.amount_sold: int = amount_sold
        """The number of units that the store could sell to the client"""

        self.normal_price: float = normal_price
        """
        The price of the product in this time in the company
        """
        self.price_sold: float = price_sold
        """
        The price sold this product to the matrix company
        """
        self.matrix_company_name: str = matrix_name
        """
        The name of the matrix company
        """
        self.from_company_name: str = from_company_name
        """
        The name of the company sells the product 
        """
        self.from_company_tag: TypeCompany = from_company_tag
        """
        The type of the company its come 
        """
        self.to_company_name: str = to_company_name
        """
        The name of the place are going to the product 
        can be a Warehouse a shop or an other company type
        """
        self.to_company_tag: TypeCompany = to_company_tag
        """
        The tag of the place  are going to the product 
        can be a Warehouse a shop or an other company typeF
        """

    def __str__(self) -> str:
        # TODO:COmpletar esto
        return f"SellRecord (time = {self.time}, amount asked = {self.amount_asked}, amount sold = {self.amount_sold})"


class StockRecord(Record):
    """This record store the information of the number of units of the product in storage at a time"""

    def __init__(self, time: int, amount: int) -> None:
        super().__init__(time)
        self.amount: int = amount
        """The number of units of the product that are available in the store"""

    def __str__(self) -> str:
        return f"StockRecord (time = {self.time}, stock amount = {self.amount})"


class BuyRecord(Record):
    """This record store the information of the number of units bought to the provider at a point in time"""

    def __init__(self, time: int, amount: int, cost: int) -> None:
        super().__init__(time)
        self.amount: int = amount
        """The number of units that the store just bought to the provider"""
        self.cost: int = cost
        """How much the store pay for this supply"""

    def __str__(self) -> str:
        return f"BuyRecord (time = {self.time}, number of units received = {self.amount})"


class BalanceRecord(Record):
    """This records represents the balance of the store at this point in time"""

    def __init__(self, time: int, balance: float) -> None:
        super().__init__(time)
        self.balance: float = balance
        """The balance of the store at this point in time"""

    def __str__(self) -> str:
        return f"BalanceRecord (time = {self.time}, actual balance of store = {self.balance})"


class PayHoldingRecord(Record):
    """This record represents the amount of money the store is paying for the storage service at a point in time"""

    def __init__(self, time: int, cost: float) -> None:
        super().__init__(time)
        self.cost: float = cost
        """The amount of money the store is paying for the storage service"""

    def __str__(self) -> str:
        return f"PayHoldingRecord (time = {self.time}, holding cost payed = {self.cost})"
