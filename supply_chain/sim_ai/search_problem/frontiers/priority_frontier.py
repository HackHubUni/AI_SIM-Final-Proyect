from typing import *
from ..frontier import *
import heapq


class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""

    def __init__(self, items=(), key=lambda x: x):
        self.key = key
        self.items = []  # a heap of (score, item) pairs
        for item in items:
            self.add(item)

    def clear(self):
        self.items = []

    def contains(self, element) -> bool:
        for item in self.items:
            if item[1] == element:
                return True
        return False

    def add(self, item):
        """Add item to the queue."""
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[1]

    def top(self):
        return self.items[0][1]

    def __len__(self):
        return len(self.items)


class PriorityFrontier(Frontier):
    def __init__(self, priority_function: Callable[[SearchNode], float]) -> None:
        self.priority_function = priority_function
        self.frontier = PriorityQueue(key=priority_function)
        self.n_count = 0

    def push(self, element: SearchNode):
        # result = (self.priority_function(element), element)
        # self.frontier.put(result)
        self.frontier.add(element)
        self.n_count += 1

    def pop(self) -> SearchNode:
        self.n_count -= 1
        return self.frontier.pop()

    def is_empty(self) -> bool:
        return len(self.frontier) == 0

    def clear(self):
        self.frontier.clear()

    def contains(self, element: SearchNode) -> bool:
        # return element in self.frontier
        return self.frontier.contains(element)

    def count(self) -> int:
        return self.n_count
