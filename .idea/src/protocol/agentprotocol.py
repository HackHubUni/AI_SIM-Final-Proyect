from collections import abc

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
    
        ...
