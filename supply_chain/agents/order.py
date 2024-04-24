from supply_chain.agents.origin import Origin

try:
    from supply_chain.products import Product

except:
    pass


class Order():
    """
    Represent a order agent in the supply chain.
    """

    def __init__(self, product: Product, quantity: int, origin: Origin, request_date, delivery_date):
        self.product: Product = product
        self.quantity: int = quantity
        self.origin: Origin = origin
        self.request_date:int = request_date
        "Tiempo en que se hizo la petición"
        self.delivery_date = delivery_date


