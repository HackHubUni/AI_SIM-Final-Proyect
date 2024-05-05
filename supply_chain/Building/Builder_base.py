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

    def get_random_int(self,min_value:int,max_value:int)->int:
        """
        Retorna una var aleatoria entera generado con la semilla de esta clase

        :param min_value:
        :param max_value:
        :return:
        """
        return self._random.randint(min_value,max_value)


    def get_random_float(self,min_value:float,max_value:float):
        """
        Retorna un float con los valores de esta clase
        :param min_value:
        :param max_value:
        :return:
        """
        # Genera un número flotante aleatorio entre 1.0 y 10.0
        return self._random.uniform(min_value,max_value)