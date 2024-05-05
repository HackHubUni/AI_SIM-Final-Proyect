from abc import ABC
import random


class BuilderBase(ABC):
    def start(self):
        #Añadir el seed de la variable aleatoria
        self._random.seed(self.seed)



    def __init__(self, seed: int):
        self.seed: int = seed
        """
        Semilla para la variable aleatoria
        """
        self._random: random.Random = random.Random()
        """
        Variable aleatioria
        """

        self.start()
