
from supply_chain.Message import Message
from supply_chain.agents.utils import generate_guid, ImplicationLogicWrapped
from supply_chain.company import Company, TypeCompany
from typing import Callable

class EnvVisualizer:

    def __init__(self,
                 get_time: Callable[[], int], send_msg: Callable[[Message], None],
                 get_dict_valoracion_inicial: Callable[[], dict[TypeCompany, dict[str, float]]],
                 get_logic_implication: Callable[[], list[ImplicationLogicWrapped]],
                 get_distance_in_the_map: Callable[[str, str], float],
                 ):
        self.get_distance_in_the_map: Callable[[str, str], float] = get_distance_in_the_map
        self.get_time: Callable[[], int] = get_time
        self.send_msg: Callable[[Message], None] = send_msg
        self.get_dict_valoracion: Callable[[], dict[TypeCompany, dict[str, float]]] = get_dict_valoracion_inicial
        self.get_logic_implication: Callable[[], list[ImplicationLogicWrapped]] = get_logic_implication
