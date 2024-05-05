from typing import Callable

from sympy.core.evalf import rnd

from supply_chain.Building.Builder_base import BuilderBase
from supply_chain.client_consumer import ConsumerBody, ConsumerAgent
from supply_chain.products.flavor import Flavor
from supply_chain.products.nutritive_properties import NutritiveProperties
from supply_chain.sim_event import SimEvent


class Consumer(BuilderBase):
    def __init__(self,
                 seed:int,
                 get_time: Callable[[], int],
                 add_event: Callable[[SimEvent], None],
                 ):

        super().__init__(seed)
        self.get_time: Callable[[], int]=get_time
        self.add_event: Callable[[SimEvent], None]=add_event

        self.consumer_body:ConsumerBody = self.generate_consumer_body()
        self.consumer_agent:ConsumerAgent = self.generate_basic_consumer_agent(self.get_time, self.add_event)

    def __str__(self):
        return f'Consumer [ConsumerBody: {self.consumer_body}, ConsumerAgent: {self.consumer_agent}]'


    def generate_basic_consumer_agent(self,
        get_time: Callable[[], int],
        add_event: Callable[[SimEvent], None],
    )-> ConsumerAgent:
        """Generates a basic consumer agent"""
        return ConsumerAgent(
            get_time,
            add_event,
            lambda:self.get_random_int(50,50*3) ,
            lambda:self.get_random_int(3,8),
        )


    def generate_consumer_body(self) -> ConsumerBody:
        """Generate a random Consumer Body with tendency to the sweet flavor and high carbohydrates"""
        base_ideal_flavor = Flavor(50, 30, 5, 5, 5)
        base_ideal_nutrition = NutritiveProperties(10, 40, 30)
        return ConsumerBody(
            base_ideal_flavor.get_random_similar_flavor(),
            base_ideal_nutrition.get_random_similar_flavor(),
        )