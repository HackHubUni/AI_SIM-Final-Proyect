from collections import abc
from protocol.productprotocol import *
'''class Believes:
    # conjunto de la info del agente sobre el ambiente
    def __init__(self):
        self.believes = set()

    def add(self, belief):
        self.believes.add(belief)
    
    def remove(self, belief):
        self.believes.remove(belief)
    
    def clear(self):
        self.believes.clear()
    
    def get_all(self):
        return self.believes
    
    def contains(self, belief):
        return belief in self.believes
    
class Belief(abc.Protocol):
    def __init__(self, name,best):
        self.types = name
        self. best = best

class BestBelief(Belief):
    def __init__(self, name,best):
        super.__init__(name,best)
         #name:producto
         # best:lista de los mejores proveedores de un determinado producto

class WordAparenceBelief(Belief):
    def __init__(self, name,best):
        super.__init__(name,best)
        # name: es el tipo a analizar ebn la ciudad ya sea productor monoproducto 
        # best es la lista de instancuias existebntes de este tipo

class ShopBelief(Belief):
    def __init__(self, name,best):
        super.__init__(name,best)
        # name: el nombre de la tienda a analizar
        # best el costo de transportacion de cada tienda
        '''

class Desire():
    def __init__(self, product:Product,shop,price,amount) :
        self.product= product
        self.shop = shop
        self.price = price
        self.amount = amount
class Desires:
    # conjunto de objetivos que el agente quiere alcanzar
    def __init__(self):
        self.desires = set()
    
    def add(self, desire:Desire):
        self.desires.add(desire)
    
    def remove(self, desire):
        self.desires.remove(desire)
    
    def clear(self):
        self.desires.clear()
    
    def get_all(self):
        return self.desires
    
    def contains(self, desire):
        return desire in self.desires

class Intention():
    def __init__(self, desire:Desire, producer_cost, need_product) :
        self.desire = desire
        self.producer_cost = producer_cost
        self.need_product = need_product# lista de producrtos necesarios para satisfacer el deseo
        
        
class Intentions:
    # conjunto de planes que el agente ha decidido seguir
    def __init__(self):
        self.intentions = set()
    
    def add(self, intention:Intention):
        self.intentions.add(intention)
    
    def remove(self, intention):
        self.intentions.remove(intention)
    
    def clear(self):
        self.intentions.clear()
    
    def get_all(self):
        return self.intentions
    
    def contains(self, intention):
        return intention in self.intentions
    

