from typing import Generator, Any

from supply_chain.agents.new.logic import *
from supply_chain.agents.new.utils import expr
from supply_chain.agents.utils import LogicWrapped, convert_to_float


class SistExperto(FolKB):

    def add(self, wrapped: LogicWrapped):
        """Se añade uno de los wrapped """
        if not isinstance(wrapped,LogicWrapped):
            raise Exception(f'wrapped no es instancia de LogicWrapped es de {type(wrapped)} ')

        self.tell(expr(wrapped.show()))

    def ask(self, query: LogicWrapped) -> bool | str | float:
        """
        Hacer una pregunta
        Retorna un bool o un str
        Si el dicc que devuelve es vacio devuelve un True
        Tratará de devolver un float si puede sino es un string
        """
        ret = super().ask(expr(query.show()))
        if isinstance(ret, bool):
            return ret
        # Dame las llaves
        keys = list(ret.keys())
        # Si esta vacio que retorne True
        if len(keys) < 1:
            return True
        # Chequear que el len sea 1 no haya mas de una posibilidad
        assert len(keys) == 3, f'El len del dicc que devuelve la inferencia tiene len{len(keys)}'

        key = keys[2]
        val = ret[key]
        # Llevar a str
        to_str = str(val)
        # Tratar de convertir a float
        to_float = convert_to_float(to_str)
        # Si es float que lo mande
        if to_float is not None:
            return to_float

        return to_str

    def ask_generator(self, query: LogicWrapped) -> Generator[Any, Any, None]:
        """
        Haces una pregunta y retorna una iterador con lo que paso
        :param query:
        :return:
        """
        return super().ask_generator(expr(query))
