from collections import abc
from SE.belief import *
from SE.so_sistemaexperto import *
import queue
from func import Func
import time
import math
from products.product import Product

class Origin:
    def __init__(self, producer,shipper,manuefacturer,shop):
        self.producer = producer
        self.shipper = shipper
        self.manuefacturer = manuefacturer
        self.shop = shop
class Message:
            """
            Represents a message for communication between agents.
            """

            def __init__(self, sender, receiver, content:Belief):
                self.sender = sender
                self.receiver = receiver
                self.content = content

            def to_belief(self)->Belief:
                """
                Converts the message into a belief.
                """
                return self.content
            
class Agent(abc.Protocol):
    def brf(self):
        # partir de una entrada perceptual y el cjto de creencias actuales determina un nuevo cjto de creencias
        pass
    
    def options(self):
        pass


    def filter(self):
        pass

    def execute(self):
        pass

    def tell(info:Message):
        # TODO: Carla must type the info variable because every body in the repo
        # should know how to pass info to the agent
        pass

    

            
class Order():
    """
    Represent a order agent in the supply chain.
    """
    
    def __init__(self, product:Product, quantity:int, origin:Origin, request_date, delivery_date):
        self.product = product
        self.quantity = quantity
        self.origin = origin
        self.request_date = request_date
        self.delivery_date = delivery_date
 
class Desire:
    """
    Represent a desire in the supply chain.
    """

    def __init__(self, order:Order):
        self.order = order

    
class Intention:
    """
    Represents an intention in the supply chain.
    """

    def __init__(self, action, order:Order):
        self.action = action
        self.order = order




class ProducerAgent(Agent):
    """
    Represents a producer agent in the supply chain.
    """

    def __init__(self, name, orders:queue.Queue, beliefs:Set_of_Beliefs,
                 SE:ExpertSystem, stock:dict[str, int],product_price:dict[str, int]):
        self.name = name
        self.stock = stock
        self.product_price = product_price

        self.orders = orders
        self.Beliefs = beliefs
        self.Desires:list[Desire] = []
        self.Intentions:list[Intention] = []
        self.SE = SE
        self.Plans = []

    def brf(self):

        while not self.orders.empty():
            order = self.orders.get()
            belief = Belief(order)
            self.Beliefs.add(belief)

    def options(self):
    
        while not self.orders.empty():
            order = self.orders.get()
            desire = Desire(order)
            self.Desires.append(desire)

    def filter(self):
        for i in self.Desires:
            self.Intentions =self.SE.get_action(self.Beliefs, i)
        

    def execute(self):
        self.events = []
        for i in self.Intentions:
            if i.action == "sell":
                Event("sell", time.time(), self.name, i.order,i.order.quantity*self.product_price[i.order.product])
            elif i.action == "no-sell":
                Event("no-sell", time.time(), self.name, i.order,i.order.quantity*math.inf)
            else:
                print("Invalid action")
            self.events.append(Event)

                    
                    


            
