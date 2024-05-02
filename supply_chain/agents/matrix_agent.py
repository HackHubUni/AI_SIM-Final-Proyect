from abc import ABC, abstractmethod

from new.logic import *

from enum import Enum

from supply_chain.agent import Agent

from supply_chain.sim_environment import SimEnvironment

from supply_chain.Company.companies_types.Producer_Company import *


class MatrixAgent(Agent):
    def __init__(self, name: str, company):
        super().__init__(name)





    def ask_productor(self,product_name:str):

        pass