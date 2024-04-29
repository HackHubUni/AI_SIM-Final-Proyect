class SearchProblem:
    """This is the base class for all search problems"""

    def __init__(self, initial_state) -> None:
        self.initial_state = initial_state
        """The initial state of the problem"""

    def get_actions(self, state):
        """This method returns the list of actions that can be applied to the state"""
        pass

    def action_cost(self, state, action) -> float:
        """This method returns the cost of applying the action to the state"""
        return 1

    def apply_action(self, state, action):
        """This method apply an action to a state and return the resulting state"""
        pass

    def is_final(self, state) -> bool:
        """This method return True if the state is a final state, False otherwise"""
        pass
