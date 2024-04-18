from queue import Queue
from belief import Belief , Set_of_Beliefs
from so_action import Action 
from so_rule import Rule

class ExpertSystem:
    def __init__(self):
        self.belief_base = set()
        self.action_queue: Queue[Action] = Queue()
        self.rules = set()

    def add_belief(self, belief:Belief):
        self.belief_base.add(belief)
    
    def get_belief(self, proposition):
        belief = None 
        for belief in self.belief_base:
            if belief.proposition == proposition:
                return belief
        return belief

    def get_beliefs(self):
        return self.belief_base
    
    def delete_belief(self, belief):
        self.belief_base.remove(belief)    

    def add_rule(self, rule):
        self.rules.add(rule)
     
    def get_rule(self, rule:Rule):
        rule = None 
        for rule in self.rules:
            if rule.antecedents[0] == rule.antecedents[0] and rule.consequent[0] == rule.consequent[0]:
                return rule
        return None
    
    def delete_rule(self, rule):
        self.rules.remove(rule)
    
    def add_action(self, action):
        self.action_queue.put(action)
    
    def execute_next_action(self, beliefs_group: Set_of_Beliefs):
        action = self.action_queue.get()
        action.execute(beliefs_group)
        print(f"Executing action: {action.action}")
   
    def infer_belief(self, rule :Rule, beliefs_group: Set_of_Beliefs):
        # Check if the rule's antecedents are already in the belief base
        antecedents = rule.antecedents
        beliefs_met = False
       
        if all(any(belief.proposition == antecedent.proposition and belief.value == antecedent.value for belief in beliefs_group.beliefs) for antecedent in antecedents):
            beliefs_met = True

        if beliefs_met:
            # Apply the rule if all antecedents are met
            consequent = rule.consequent
            for action in consequent:
                self.add_action(action)

        # Execute actions from the queue
        while  not self.action_queue.empty():
            self.execute_next_action(beliefs_group) 
             

        


