from agentpy import Agent, Belief, Desire, Intention, Plan
from protocol.agentprotocol import Agent as ag
import time as t
from enviorement import EnviorementEmp
class EmpAgent(Agent, ag):
    def __init__(self, name, beliefs, desires, intentions, plans, enviorement, empenv:EnviorementEmp):
        super().__init__(name, beliefs, desires, intentions, plans, enviorement)
        self.env = empenv
        
    

    def brf(self):

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
