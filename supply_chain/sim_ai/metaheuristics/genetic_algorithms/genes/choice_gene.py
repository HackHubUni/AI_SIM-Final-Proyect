import random as rnd
import uuid
from ..gene import *


class ChoiceGene(Gene):
    def __init__(
        self,
        elements: list | str,
        identifier: str = str(uuid.uuid4()),
        initial_value=None,
    ) -> None:
        super().__init__(identifier, initial_value)
        if elements is None or len(elements) == 0:
            raise Exception(f"The elements parameter should not be empty")
        self.elements: list = elements
        self.value = (
            rnd.choice(self.elements)
            if initial_value is None or initial_value not in self.elements
            else initial_value
        )

    def mutate(self) -> None:
        v1, v2 = rnd.sample(self.elements, 2)
        self.value = v1 if self.value == v2 else v2

    def clone(self, with_mutation: bool = False) -> Self:
        return ChoiceGene(
            self.elements, self.identifier, None if with_mutation else self.value
        )

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    def __eq__(self, value: object) -> bool:
        return super().__eq__(value) and isinstance(value, ChoiceGene)
