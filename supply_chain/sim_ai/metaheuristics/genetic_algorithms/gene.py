from typing import *
from abc import abstractmethod


class Gene:
    """Base class for all genes"""

    def __init__(self, identifier: str, initial_value=None) -> None:
        self.identifier: str = identifier
        """The unique identifier of the Gene"""
        self.value = initial_value
        """The value of the Gene"""

    @abstractmethod
    def mutate(self) -> None:
        """Mutate the gene in place"""
        pass

    @abstractmethod
    def clone(self, with_mutation: bool = False) -> Self:
        """Returns a clone of this gene"""
        pass

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Gene) and self.identifier == value.identifier
