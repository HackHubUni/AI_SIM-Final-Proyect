from terminadas.belief import Set_of_Beliefs ,Belief
from terminadas.so_rule import Rule 
from terminadas.so_action import Action, Action_Add
from terminadas.city import *
set = Set_of_Beliefs()

set.add(Belief("Producer", True))
set.add(Belief("Product", True))
set.add(Belief("Shop", True))
set.add(Belief("Producer3", False))
set.add(Belief("Product3", False))
set.add(Rule([Belief("Producer", True), Belief("Product", True)], [Action_Add("Buy", Belief("Buy-Product", True))]))

print(set.get_all())

