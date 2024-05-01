import unittest
from so_sistemaexperto import *
from so_action import Action_Add

class TestExpertSystem(unittest.TestCase):
    def setUp(self):
        self.expert_system = ExpertSystem()

    def test_add_belief(self):
        self.expert_system.add_belief(Belief("A",True))
        self.assertEqual(len(self.expert_system.get_beliefs()), 1)
        a:Belief = self.expert_system.get_belief("A")
        self.assertEqual(a.proposition ,"A")

    def test_delete_belief(self):
        self.expert_system.add_belief(Belief("A",True))
        self.expert_system.delete_belief(self.expert_system.get_belief("A"))
        self.assertEqual(len(self.expert_system.get_beliefs()), 0)
        self.assertIsNone(self.expert_system.get_belief("A"))

    def test_add_rule(self):
        
        self.expert_system.add_rule( Rule( [Belief("IF A THEN B" , True)],[Action_Add("THEN B")]))
        self.assertEqual(len(self.expert_system.rules), 1)
        a = self.expert_system.get_rule(Rule( [Belief("IF A THEN B" , True)],[Action_Add("THEN B")]))
        self.assertEqual(self.expert_system.rules.__contains__(a), True)

    def test_delete_rule(self):
        self.expert_system.add_rule(Rule( [Belief("IF A THEN B" , True)],[Action_Add("THEN B")]))
        self.expert_system.delete_rule(self.expert_system.get_rule(Rule( [Belief("IF A THEN B" , True)],[Action_Add("THEN B")])))
        self.assertEqual(len(self.expert_system.rules), 0)

    def test_add_action(self):
        self.expert_system.add_action(Action("Action 1"))
        self.assertEqual(self.expert_system.action_queue.qsize(), 1)

    def test_execute_next_action(self):
        self.expert_system.add_action(Action_Add("Action 1"))
        a = Set_of_Beliefs()
        self.expert_system.execute_next_action(a) 
        self.assertEqual(self.expert_system.action_queue.qsize(), 0)

    def test_infer_belief(self):
        self.expert_system.add_belief(Belief("A", True))
        self.expert_system.add_rule(Rule([Belief("A" , True)],[Action_Add(" THEN B")]))
        a = Set_of_Beliefs()
        a.add(Belief("A", True))
        self.expert_system.infer_belief(Rule([Belief("A" , True)],[Action_Add(Belief(" THEN B",True))]), a)
        self.assertEqual(self.expert_system.action_queue.qsize(), 0)

   
if __name__ == '__main__':
    unittest.main()