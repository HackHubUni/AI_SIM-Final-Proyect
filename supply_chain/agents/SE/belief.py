
class Belief():
    def __init__(self, proposition:str, params, value:bool ):
        ##self.params = params
        self.proposition = proposition
        self.params = params
        self.value = value
    
    def __repr__(self):
        return f"Belief({self.proposition}({self.params}): {self.value})"


# agregar los otros tipos de belief





# conjunto de creencias SO

class Set_of_Beliefs:
    def __init__(self):
        self.beliefs = set()
    
    def add(self, belief):
        self.beliefs.add(belief)
    
    def remove(self, belief):
        self.beliefs.remove(belief)
    
    def clear(self):
        self.beliefs.clear()
    
    def get_all(self):
        return self.beliefs
    
    def contains(self, belief):
        return belief in self.beliefs
    
    def __repr__(self):
        return f"Set_of_Beliefs({self.beliefs})"
    
