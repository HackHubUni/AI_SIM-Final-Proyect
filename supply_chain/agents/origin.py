try:
    from supply_chain.company_protocol import Company
except:
    pass


class Origin:
    def __init__(self, producer: Company, shipper: Company, manuefacturer: Company, Matrix: Company):
        self.producer: Company = producer
        self.shipper: Company = shipper
        self.manuefacturer: Company = manuefacturer
        self.Matrix: Company = Matrix
        """
        Empresa matriz 
        """
