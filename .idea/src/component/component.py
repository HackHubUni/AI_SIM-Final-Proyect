class Believes:
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
    

class Desires:
    # conjunto de objetivos que el agente quiere alcanzar
    def __init__(self):
        self.desires = set()
    
    def add(self, desire):
        self.desires.add(desire)
    
    def remove(self, desire):
        self.desires.remove(desire)
    
    def clear(self):
        self.desires.clear()
    
    def get_all(self):
        return self.desires
    
    def contains(self, desire):
        return desire in self.desires

class Intentions:
    # conjunto de planes que el agente ha decidido seguir
    def __init__(self):
        self.intentions = set()
    
    def add(self, intention):
        self.intentions.add(intention)
    
    def remove(self, intention):
        self.intentions.remove(intention)
    
    def clear(self):
        self.intentions.clear()
    
    def get_all(self):
        return self.intentions
    
    def contains(self, intention):
        return intention in self.intentions