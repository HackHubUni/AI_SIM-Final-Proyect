from agentpy import Agent, Belief, Desire, Intention, Plan
from protocol.agentprotocol import Agent as ag
import time as t
from enviorement import EnviorementEmp
from component.component import *

class EmpAgent(Agent, ag):
    def __init__(self, name, beliefs:Believes, desires:Desires, intentions, plans, enviorement, empenv:EnviorementEmp):
        self.env = empenv
        self.Believes= beliefs
        self.Desires = desires
        
    #metodos sin implementar
    def update_product(product):
        #se encargara en guaradr el mejor productor para un deteermionado producto
        pass
    def update_shop(shop):
        #se encargara en guaradr el costo de llegar a una tienda en cuanto a transporte
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
            if not self.env.need.empty():
                shop_request = self.env.requestarrival.get()
                if len(shop_request.product) >1:
                    count = 0
                    for p in shop_request.product:
                        self.Desires.add(Desire(p,shop_request.Shop,shop_request.amount[count]))
                        count+=1
        

    def filter(self):# desicion de que productos va aprodducir y que tiendas va a visitar ( prductos que no le representes perdidas)
       # analizando stock y costo de reemplazo,transporte y todo
        pass
        



    #EVENTO DE SOLICITUD ( CUANDO LA TIENDA M PIDE)
    def check_request(self):
        while True:
            t.sleep(1)
            if not self.env.requestarrival.empty():
                request =self.env.requestarrival.get()
                self.execute(request)


# Crear una instancia del agente
agent = EmpAgent()

# Ejecutar el agente
agent.run()
