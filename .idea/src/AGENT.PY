from agentpy import Agent, Belief, Desire, Intention, Plan
from protocol.agentprotocol import Agent as ag
import time as t
from enviorement import*
from component.component import *
from protocol.producer import Producer
class EmpAgent( ag):
    def __init__(self, name, beliefs:Believes, desires:Desires, intentions:Intentions, plans, enviorement, empenv:EnviorementEmp,min_stock:int):
        self.env = empenv
        self.Believes= beliefs
        self.Desires = desires
        self.Intentions = intentions
        self.min_stock = min_stock
        
        
    #metodos sin implementar
    def update_product(product):
        #se encargara en guaradr el mejor productor para un deteermionado producto
        pass
    def update_shop(shop) -> float:
        #se encargara en guaradr el costo de llegar a una tienda en cuanto a transporte
        pass
    def update_stock(self,product):# llenar el stock en lo que se le pide

        for i in self.Desires:
                                if isinstance(i,BestBelief) and i.product == need_product[0].product:#tomar el mejor productor
                                    for replacent in self.env.Replacent_Cost:
                                        if replacent[0] == need_product[0]:
                                            cost  = replacent[1]# costo de transporte
    def transport_shop(shop):# costo de transporte hasta la tienda
        pass

    def brf(self):
        change = 0
        for belief in self.Believes:
            if isinstance(belief,WordAparenceBelief):
                if belief.types == "Producer":
                    if belief.best!= self.env.env.Producer:
                        change =-1
                if belief.types == "Product":
                    if belief.best!= self.env.env.Product:
                        change =-1
                if belief.types == "Shop":
                    if belief.best!= self.env.env.Shop:
                        change =-1


        if change is not 0:
            self.Believes.clear()
            self.Believes.add(WordAparenceBelief("Producer",self.env.env.Producer))
            self.Believes.add(WordAparenceBelief("Product",self.env.env.Product))
            self.Believes.add(WordAparenceBelief("Shop",self.env.env.Shop))
            for product in self.env.env.Product:
                self.update_product(product)
            for shop in self.env.env.Shop:
                self.update_shop(shop)
        

    def options(self):
        #se encargara de buscar las opciones de los productos en el ambiente
        self.Desires.clear()
        for request in range(5):
            if not self.env.requestarrival.empty():
                shop_request = self.env.requestarrival.get()
                if len(shop_request.product) >1:
                    count = 0
                    for p in shop_request.product:
                        self.Desires.add(Desire(p,shop_request.Shop,shop_request.amount[count]))
                        count+=1
        

    def filter(self):# desicion de que productos va aprodducir y que tiendas va a visitar ( prductos que no le representes perdidas)
       # analizando stock y costo de reemplazo,transporte y todo

        for desire in self.Desires:
            cost = 0
            need = []
            if isinstance(desire.product,ProcessedProduct):
                for need_product in desire.product.ingredients:
                    if need_product[0] not in self.env.env.Product:
                        raise Exception("No se puede producir el producto, no se encuentra en el ambiente")
                            
                    if need_product[0] is self.env.stock:
                        if  need_product[1] > self.env.stock[need_product[0]]:
                            # si no esta en el stock hay q comprarlo hayq sumar el costo d eso
                            need.append(need_product[0],need_product[1] - self.env.stock[need_product[0]]+self.min_stock)
                            cost += self.update_stock(need_product[0])
            else:
                if desire.product not in self.env.env.Product:
                    raise Exception("No se puede producir el producto, no se encuentra en el ambiente")
                elif not desire.product is self.env.stock:
                    cost+= self.update_stock(desire.product)
                    need.append(desire.product,desire.amount+self.min_stock)               
                elif desire.amount > self.env.stock[desire.product]:
                    cost+= self.update_stock(desire.product)
                    need.append(desire.product,desire.amount-self.env.stock[desire.product] +self.min_stock)
            cost+=self.transport_shop(desire.shop)
            self.Intentions.add(Intention(desire,cost,need))       
                            
    def execute(self):
        self.brf()
        self.options()
        self.filter()
        delivery = []
        #ejecutar las intenciones
        for intention in self.Intentions:
            if intention.desire.price * intention.desire.amount > intention.producer_cost:
                self.env.R +=1
                if not  len(intention.needs_product)is None:
                    for need in intention.needs_product:
                        self.env.update_product(need[0],[need[1]])
                if isinstance(intention.desire.product, BaseProduct):
                    a = self.env.stock[intention.desire.product.name]
                    a = a-intention.desire.amount
                    self.env.stock[intention.desire.product.name] = a
                else:
                    self.stock = intention.desire.product.produce(self.stock)
                self.env.Balance -=intention.producer_cost
                self.Intentions.remove(intention)
                
            delivery.append(ShopDelivery(intention.desire.product,t.time(),intention.desire.shop))
        return delivery


    '''#EVENTO DE SOLICITUD revisar las solicites cada cierto tiempo
    def check_request(self):
        while True:
            t.sleep(1)
            self.execute()'''
                


class ShopAgent(ag):
    def __init__(self, name, beliefs:Believes, desires:Desires, intentions:Intentions, plans, enviorement, empenv,min_stock:int):
        self.env = empenv
        self.Believes= beliefs
        self.Desires = desires
        self.Intentions = intentions
        self.min_stock = min_stock

    def brf(self):
        
    
