from .search_node import *


class Frontier:
    """
    Base class for all frontiers"""

    def push(self, element: SearchNode):
        """
        This method is for adding elements to the frontier"""
        pass

    def is_empty(self) -> bool:
        """
        This method returns true when the frontier has no elements"""
        pass

    def pop(self) -> SearchNode:
        """
        This is the method where all the magic occurs. In here we define
        which node is the next to explore"""
        pass

    def clear(self):
        """
        This method is for clear the frontier"""
        pass

    def contains(self, element: SearchNode) -> bool:
        """Tells if the element is in the frontier"""
        pass

    def count(self) -> int:
        """Returns the number of elements in the frontier"""
        pass

    def __len__(self) -> int:
        return self.count()
