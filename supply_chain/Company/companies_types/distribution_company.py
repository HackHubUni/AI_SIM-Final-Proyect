from supply_chain.company import *
from typing import Callable

from supply_chain.sim_event import SimEvent


class LogisticCompany(Company):
    """
    Class for the logistic Company
    """

    def __init__(self,
                 name: str,
                 get_time: Callable[[], int],
                 add_event: Callable[[SimEvent], None],
                 get_price_by_unit_distance: Callable[[int], float],
                 get_time_by_unit_distance: Callable[[int], int],

                 ):
        super().__init__(name=name,
                         get_time=get_time,
                         add_event=add_event,

                         )
        self._get_price_by_unit_distance: Callable[[int], float] = get_price_by_unit_distance
        """Da el precio que se tiene por distancia se le entra la cant de unidades de distancia y da el precio"""

        # TODO:Leismael la idea es que esta función pueda o no cada vez que se le de una cant de unidades de distancia dar el mismo tiempo
        # TODO: Análogo con el precio
        self._get_time_by_unit_distance: Callable[[int], int] = get_time_by_unit_distance
        """Se le dice la cant de unidades de distancia y devuelve el tiempo en unidades de tiempo """

    def get_estimated_time_by_distance_unit(self, count_distance_units: int) -> int:
        """
        Devuelve el tiempo estimado que se demorará en x unidades de tiempo
        :param count_distance_units: cantidad de unidades de distancia
        :return: la cant de unidades de tiempo se espera que demore
        """

        return self._get_time_by_unit_distance(count_distance_units)

    def get_estimated_cost_by_distance_unit(self, count_distance_units: int = 1) -> float:
        """
        Devuelve el costo estimado por las inidades de distancia que se le de de distancia
        por defecto esta uno pero puede hacerse que el lambda a dar menor costo a mayor distancia
        que si lo pidiera unidad a unidad
        ejemplo: Si fuera unidad a unidad el precio seria 1 usd por unidad
        Si fueran 30 unidades el costo seria 30 usd
        Pero si se tiene una que se le pasa 30 unidades de distancia y a esa distancia
        le dice 0.75 usd el km por ser mayor de 10 unidades
        entonces es 22.5 el precio

        :param count_distance_units:Cant de distancia a recorrer en unidades
        :return:

        """
        return self._get_price_by_unit_distance(count_distance_units)

    @property
    def tag(self):
        return TypeCompany.Logistic

    def start(self):
        # TODO: Ver si hace falta logica aca
        return
