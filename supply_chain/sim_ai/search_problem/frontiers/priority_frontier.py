from typing import *
from queue import PriorityQueue
from supply_chain.sim_ai.search_problem.frontier import *


class PriorityFrontier(Frontier):
    def __init__(self, priority_function: Callable[[SearchNode], int]) -> None:
        self.priority_function = priority_function
        self.frontier = PriorityQueue()

    def push(self, element: SearchNode):
        result = (self.priority_function(element), element)
        self.frontier.put(result)

    def pop(self) -> SearchNode:
        return self.frontier.get()[1]

    def is_empty(self) -> bool:
        return self.frontier.empty()

    def clear(self):
        self.frontier.queue.clear()

    def contains(self, element: SearchNode) -> bool:
        # return element in self.frontier
        elements = list(self.frontier.queue)
        return any(x[1].state == element.state for x in elements)
