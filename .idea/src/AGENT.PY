from agentpy import Agent, Belief, Desire, Intention, Plan
from agentprotocol import Agent as ag
class MonoEmpAgent(Agent, ag):
    def __init__(self, name, beliefs, desires, intentions, plans, enviorement):
        super().__init__(name, beliefs, desires, intentions, plans, enviorement)
        
    

    def brf(self):
        
        pass



    def perceive(self, perception):
        # Actualizar las creencias del agente con la nueva percepción
        ...

    def act(self):
        # Seleccionar una acción para realizar
        ...

    def plan(self):
        # Generar un nuevo plan para alcanzar el objetivo
        ...

# Crear una instancia del agente
agent = MyAgent()

# Ejecutar el agente
agent.run()
