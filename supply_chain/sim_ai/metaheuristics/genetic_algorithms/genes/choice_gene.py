from ..gene import *
import random as rnd


class ChoiceGene(Gene):
    """This gene selects a value from a pool of available values"""

    def __init__(
        self, available_values: list | str, value=None, identifier: str = str(uuid4())
    ) -> None:
        if available_values is None:
            raise Exception(f"The available values is None")
        if len(available_values) == 0:
            raise Exception(
                "The list of available values must have at least one element"
            )
        if value is None:
            value = rnd.choice(available_values)
        super().__init__(value, identifier)
        self.available_values = available_values
        """The list of available values for choose"""

    def mutate(self) -> Self:
        v1, v2 = rnd.sample(self.available_values, 2)
        new_value = v1 if self.value == v2 else v2
        return ChoiceGene(self.available_values, new_value, self.identifier)

    def clone(self) -> Self:
        return ChoiceGene(self.available_values, self.value, self.identifier)
