class DeliveryOrder:
    def __init__(self, matrix_name: str, logistic_time: int, product_name: str, count_of_product: int):
        self.matrix_name: str = matrix_name
        self.logistic_time: int = logistic_time
        self.product_name: str = product_name
        self.count_of_product: int = count_of_product

    def _get_delivery_time(self)->int:
        """
        Devuelve el tiempo que se demorará el distribuidor
        en llevar del punto de salida al punto de llegada 
        :return: 
        """"""
     return self.logistic_time