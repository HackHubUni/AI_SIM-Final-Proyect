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

    def tell(self,info:Message):
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

    def __init__(self, action, order:Order, product_amount:{(Product,int)} = 0):
        self.action = action
        self.order = order
        self.amount = product_amount




class ProducerAgent(Agent):
    """
    Represents a producer agent in the supply chain.
    """

    def __init__(self, name, beliefs:Set_of_Beliefs, env,
                 SE:ExpertSystem, stock:dict[str, int],product_price:dict[str, int]):
        self.name = name
        self.stock = stock
        self.product_price = product_price
        self.env = env

        self.orders:queue.Queue[Order] = queue.Queue()
        self.Beliefs = beliefs
        self.Desires:list[Desire] = []
        self.Intentions:list[Intention] = []
        self.SE = SE
        self.Plans = []

    def brf(self):
        self.SE.run(self.Beliefs)

    def options(self):
    
        while not self.orders.empty():
            order = self.orders.get()
            desire = Desire(order)
            self.Desires.append(desire)

    def filter(self):
        for i in self.Desires:
            self.Intentions =self.SE.get_action(self.Beliefs, i)
        
    def execute(self):
        self.brf()
        self.options()
        self.filter()
        for i in self.Intentions:
            if i.action == "sell":
                self.Plans.append(Func("sell", time.time(), self.name, i.order,i.order.quantity*self.product_price[i.order.product]))
            elif i.action == "no-sell":
                self.Plans.append(Func("no-sell", time.time(), self.name, i.order,i.order.quantity*math.inf))
            else:
                print("Invalid action")

    def tell(self,info: Message):
        self.SE.process_message(self.Beliefs, info)  


    """
    Represents a shipper agent in the supply chain.
    """

    def __init__(self, name, beliefs:Set_of_Beliefs,
                 SE:ExpertSystem, stock:dict[str, int],product_price:dict[str, int]):
        self.name = name
        self.stock = stock
        self.product_price = product_price

        self.orders:queue.Queue[Order] = queue.Queue()
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
        pass     

                    
class ShipperAgent(Agent):
    """
    Represents a shipper agent in the supply chain.
    """

    def __init__(self, name, beliefs:Set_of_Beliefs,
                 SE:ExpertSystem, price_per_km:int, speed:int):
        self.name = name
        self.price_per_km = price_per_km
        self.speed = speed  

        self.orders:queue.Queue[Order] = queue.Queue()
        self.Beliefs = beliefs
        self.Desires:list[Desire] = []
        self.Intentions:list[Intention] = []
        self.SE = SE
        self.Plans = []

    def brf(self):
        self.SE.run(self.Beliefs)

    def options(self):
        while not self.orders.empty():
            order = self.orders.get()
            desire = Desire(order)
            self.Desires.append(desire)

    def filter(self):
        for i in self.Desires:
            self.Intentions =self.SE.get_action(self.Beliefs, i)
        
    def execute(self):
        #aca necesito la implementacion de A*
        pass                    

    def tell(self,info: Message):
        self.SE.process_message(self.Beliefs, info)
            
class ManufacturerAgent(Agent):
    """
    Represents a manufacturer agent in the supply chain.
    """

    def __init__(self, name, beliefs:Set_of_Beliefs,
                 SE:ExpertSystem, stock:dict[str, int],product_price:dict[str, int]):
        self.name = name
        self.stock = stock
        self.product_price = product_price

        self.orders:queue.Queue[Order] = queue.Queue()
        self.Beliefs = beliefs
        self.Desires:list[Desire] = []
        self.Intentions:list[Intention] = []
        self.SE = SE
        self.Plans = []

    def brf(self):
        self.SE.run(self.Beliefs)

    def options(self):
    
        while not self.orders.empty():
            order = self.orders.get()
            desire = Desire(order)
            self.Desires.append(desire)

    def filter(self):
        for i in self.Desires:
            self.Intentions =self.SE.get_action(self.Beliefs, i)
        
    def execute(self):
        self.brf()
        self.options()
        self.filter()
        for i in self.Intentions:
            if i.action == "produce":
                self.Plans.append(Func("produce", time.time(), self.name, i.order,i.order.quantity*self.product_price[i.order.product]))
            elif i.action == "no-produce":
                self.Plans.append(Func("no-produce", time.time(), self.name, i.order,i.order.quantity*math.inf))
            elif i.action == "restock":
                for k,v in i.amount.items():
                    self.Plans.append(Func_restock("restock", time.time(), self.name, i.order,v))
                print("Invalid action")

    def tell(self,info: Message):
        self.SE.process_message(self.Beliefs, info)