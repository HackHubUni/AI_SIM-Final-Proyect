from terminadas.belief import Belief
from terminadas.so_action import Action


class Rule:
    def __init__(self, antecedents: list[Belief], consequent : list[Action]):
        self.antecedents = antecedents
        self.consequent = consequent
    
    def __repr__(self):
        return f"Rule({self.antecedents} -> {self.consequent})"

