
from typing import Callable

from supply_chain import CompanyConfidence
from supply_chain.Message import Message
from supply_chain.agents.utils import ImplicationLogicWrapped
from supply_chain.company import TypeCompany


class EnvVisualizer:

    def __init__(self,
                 get_time: Callable[[], int],
                 send_msg: Callable[[Message], None],
                 get_dict_valoracion_inicial: Callable[[], dict[TypeCompany, dict[str, float]]],
                 get_logic_implication: Callable[[], list[ImplicationLogicWrapped]],
                 get_distance_in_the_map: Callable[[str, str], float],
                 ):
        self.get_distance_in_the_map: Callable[[str, str], float] = get_distance_in_the_map
        self.get_time: Callable[[], int] = get_time
        self.send_msg: Callable[[Message], None] = send_msg
        self.get_dict_valoracion: Callable[[], dict[TypeCompany, dict[str, float]]] = get_dict_valoracion_inicial
        self.get_logic_implication: Callable[[], list[ImplicationLogicWrapped]] = get_logic_implication


class MatrixEnvVisualizer(EnvVisualizer):
    def __init__(self,
                 get_time: Callable[[], int],
                 send_msg: Callable[[Message], None],
                 get_dict_valoracion_inicial: Callable[[], dict[TypeCompany, dict[str, float]]],
                 get_logic_implication: Callable[[], list[ImplicationLogicWrapped]],
                 get_distance_in_the_map: Callable[[str, str], float],
                 get_producers_name: Callable[[], list[str]],
                 get_manufacturers_name: Callable[[], list[str]],
                 get_warehouses_name: Callable[[], list[str]],
                 get_distributor_names: Callable[[], list[str]],
                 ):
        super().__init__(get_time=get_time,
                         send_msg=send_msg,
                         get_logic_implication=get_logic_implication,
                         get_dict_valoracion_inicial=get_dict_valoracion_inicial,
                         get_distance_in_the_map=get_distance_in_the_map
                         )

        self.get_producers_name: Callable[[], list[str]] = get_producers_name
        self.get_manufacturers_name: Callable[[], list[str]] = get_manufacturers_name
        self.get_warehouses_name: Callable[[], list[str]] = get_warehouses_name
        self.get_distributor_names: Callable[[], list[str]] = get_distributor_names

        """
        Lambda para retornar dado el nombre de una compañía la confianza que se tiene en esta
        """
