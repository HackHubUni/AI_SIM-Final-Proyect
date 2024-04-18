from queue import Queue
class Belief:
    def __init__(self, proposition, value ):
        ##self.params = params
        self.proposition = proposition
        self.value = value
    
    def __repr__(self):
        return f"Belief({self.proposition}: {self.value})"

class Set_of_Beliefs:
    def __init__(self):
        self.beliefs = set()
    
    def add(self, belief:Belief):
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
    
class Action:
    def __init__(self, action, params = None):
        self.action = action
        self.params = params

    def execute(self,beliefs_group: Set_of_Beliefs):
        pass
    
    def __repr__(self):
        return f"Action({self.action} {self.params})"
 
class Action_Add(Action):
    def __init__(self, action, params = None):
        super().__init__(action,params)
       
    def execute(self,beliefs_group: Set_of_Beliefs):
        ##print(f"Adding {self.amount} {self.product} to stock")
        print(f"Adding belief: {self.action} {self.params}")
        beliefs_group.add(self.params)


class Rule:
    def __init__(self, antecedents: list[Belief], consequent : list[Action]):
        self.antecedents = antecedents
        self.consequent = consequent
    
    def __repr__(self):
        return f"Rule({self.antecedents} -> {self.consequent})"


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
             

        


