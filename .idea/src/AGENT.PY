from agentpy import Agent, Belief, Desire, Intention, Plan
from protocol.agentprotocol import Agent as ag
import time as t
from enviorement import EnviorementEmp
from component.component import *

class EmpAgent(Agent, ag):
    def __init__(self, name, beliefs:Believes, desires, intentions, plans, enviorement, empenv:EnviorementEmp):
        self.env = empenv
        self.Believes= beliefs
        
    #metodos sin implementar
    def update_best(product):
        #se encargara en guaradr el mejor productor para un deteermionado producto
        pass



    def brf(self):
        change = 0
        for belief in self.Believes:
            if isinstance(belief,WordAparenceBelief):
                change =-1

        if change is not 0:
            self.Believes.clear()
            self.Believes.add(WordAparenceBelief("Producer",self.env.env.Producer))
            self.Believes.add(WordAparenceBelief("Product",self.env.env.Product))
            for product in self.env.env.Product:
                self.update_best(product)
        

    def options(self):

        



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
