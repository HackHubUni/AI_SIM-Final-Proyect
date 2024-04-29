from supply_chain.agents.agent import Order


class Func:
    def __init__(self, event_type:str, event_time:float, event_location, event_description:Order,price:float):
        """

        :param event_type:
        :param event_time:
        :param event_location:Agent
        :param event_description:
        :param price:
        """
        self.event_type = event_type
        self.event_time = event_time
        self.event_location = event_location
        self.event_description = event_description
        self.price =price

    def __str__(self):
        return f"Event type: {self.event_type}, Time: {self.event_time}, Location: {self.event_location}, Description: {self.event_description}"
    
class Func_restock(Func):
    def __init__(self, event_type, event_time, event_location, event_description,ingredient,price):
        self.event_type = event_type
        self.event_time = event_time
        self.event_location = event_location
        self.event_description = event_description
        self.ingredients = ingredient
        self.price =price

    def __str__(self):
        return f"Event type: {self.event_type}, Time: {self.event_time}, Location: {self.event_location}, Description: {self.event_description}"