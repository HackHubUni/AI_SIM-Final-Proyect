try:
    from supply_chain.company import Company, TypeCompany
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

    def get_pipeline_names(self):
        """
        Este método devuelve el nombre de la empresa matriz,la empresa desde donde sale la orden, la empresa a donde
        va la orden :return:tuple(matrix name:str, from_company:name,from_company_tag:TypeCompany,
        to_company_name:str,to_company_tag:TypeCompany)
        """
        matrix_name = self.Matrix.name
