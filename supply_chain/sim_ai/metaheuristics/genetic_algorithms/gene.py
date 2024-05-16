from uuid import uuid4
from typing import *
from abc import ABC, abstractmethod


class Gene(ABC):
    """This class represents the smallest unit of a part of a problem"""

    def __init__(
        self,
        value,
        identifier: str = str(uuid4()),
    ) -> None:
        self.value = value
        """This is the value of the gene"""
        self.identifier: str = identifier
        """The unique identifier of a gene"""

    @abstractmethod
    def mutate(self) -> Self:
        """This method returns a new gene with a new value"""
        pass

    @abstractmethod
    def clone(self) -> Self:
        """This method returns an identical copy of this gene"""
        pass

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Gene) and self.identifier == value.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)

    def __str__(self) -> str:
        return str(self.value)
