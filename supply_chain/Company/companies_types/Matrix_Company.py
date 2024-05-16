from supply_chain.company import *



class MatrixCompany(Company):

    def __init__(
        self,
        name: str,
        get_time: Callable[[], int],
        add_event: Callable[[SimEvent], None],
    ) -> None:
        super().__init__(name,get_time,add_event)

    @property

    def tag(self) -> TypeCompany:
        """
        Devuelve el tag del tipo de compañía que es
        :return:
        """
        return TypeCompany.Matrix




    def start(self):
        """
        Esta función es para inicializar las acciones de la empresa
        :return:
        """
        pass

    @property
    def time(self) -> int:
        """
        Retorna el tiempo actual en que se está
        :return:
        """
        return self.get_time()



