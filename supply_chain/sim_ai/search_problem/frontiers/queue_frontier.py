from ..frontier import *


class QueueFrontier(Frontier):
    def __init__(self) -> None:
        self.frontier = []

    def push(self, element: SearchNode):
        self.frontier.append(element)

    def pop(self) -> SearchNode:
        return self.frontier.pop(0)

    def is_empty(self) -> bool:
        return len(self.frontier) == 0

    def clear(self):
        self.frontier.clear()

    def contains(self, element: SearchNode) -> bool:
        return element in self.frontier

    def count(self) -> int:
        return len(self.frontier)
