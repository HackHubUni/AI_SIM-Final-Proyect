from terminadas.belief import Set_of_Beliefs

class Action:
    def __init__(self, action, params = None):
        self.action = action
        self.params = params

    def execute(self,beliefs_group: Set_of_Beliefs):
        pass
    
    def __repr__(self):
        return f"Action({self.action} {self.params})"
    


# agregar los otros tipos de action


 
class Action_Add(Action):#creada para que el test se pruebe es una tonteria BORRAR LUEGO)
    def __init__(self, action, params = None):
        super().__init__(action,params)
       
    def execute(self,beliefs_group: Set_of_Beliefs):
        ##print(f"Adding {self.amount} {self.product} to stock")
        print(f"Adding belief: {self.action} {self.params}")
        beliefs_group.add(self.params)