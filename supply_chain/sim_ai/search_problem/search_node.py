from typing import *
from .problem import *


class SearchNode:
    """This class represents a node in the search process of a problem solution"""

    def __init__(
        self,
        state,
        parent: Self = None,
        action=None,
        path_cost: float = 0,
    ) -> None:
        self.state = state
        """This represents the actual state in the problem"""
        self.parent: Self = parent
        """This represents the parent node"""
        self.action = action
        """This represents the action applied to the parent node in the problem for creating this instance"""
        self.path_cost: float = path_cost
        """This represents the cost accumulated in the path to this node"""

    def update_parent(self, parent):
        self.parent = parent

    def expand_node(self, problem: SearchProblem) -> list[Self]:
        """
        This method returns a list with the nodes corresponding to the
        reachable states from this node"""
        actions = problem.get_actions(self.state)
        child_nodes: list[SearchNode] = []
        for action in actions:
            cost = problem.action_cost(self.state, action) + self.path_cost
            node = SearchNode(
                state=problem.apply_action(self.state, action),
                parent=self,
                action=action,
                path_cost=cost,
            )
            child_nodes.append(node)
        return child_nodes

    def get_path(self) -> list:
        """
        This method returns the path from the initial
        state of the problem to the state represented by
        this node"""
        path = [self.state]
        node = self
        while node.parent is not None:
            path.append(node.parent.state)
            node = node.parent
        path.reverse()
        return path

    def get_actions(self) -> list:
        """This method returns the list of actions applied from the initial
        state of the problem to the actual state represented by this node"""
        path = [self.action]
        node = self
        while node.parent is not None:
            path.append(node.parent.action)
            node = node.parent
        path.reverse()
        return path

    def __len__(self):
        return 0 if not self.parent else (1 + len(self.parent))

    def __lt__(self, other):
        if not isinstance(other, SearchNode):
            return False
        return self.path_cost < other.path_cost

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, SearchNode):
            return False
        return self.state == value.state

    def __hash__(self) -> int:
        return hash(self.state)
