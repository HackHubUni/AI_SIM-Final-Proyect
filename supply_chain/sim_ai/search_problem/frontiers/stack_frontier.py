from supply_chain.sim_ai.search_problem.frontier import *


class StackFrontier(Frontier):
    def __init__(self) -> None:
        self.frontier = []

    def push(self, element: SearchNode):
        self.frontier.append(element)

    def pop(self) -> SearchNode:
        return self.frontier.pop()

    def is_empty(self) -> bool:
        return len(self.frontier) == 0

    def clear(self):
        self.frontier.clear()

    def contains(self, element: SearchNode) -> bool:
        return element in self.frontier
