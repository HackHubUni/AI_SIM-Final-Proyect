
from supply_chain.agents.new.logic import *
from supply_chain.agents.new.utils import expr
from supply_chain.agents.utils import LogicWrapped


class SistExperto(FolKB):

    def add(self, wrapped: LogicWrapped):
        """Se añade uno de los wrapped """
        self.tell(expr(wrapped.show()))

