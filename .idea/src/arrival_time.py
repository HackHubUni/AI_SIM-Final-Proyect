from random import random
import math

class Poisson:
    def __init__(self, media, top):
        self.media = media
        self.top = top

    def generar(self):

        # Generar top tiempos de arribo
        tiempos_arribo = []
        for i in range(self.top):
            # Número aleatorio entre 0 y 1
            u = random()

            # Función inversa de la distribución de Poisson
            tiempo_arribo = -math.log(u) / self.media

            tiempos_arribo.append(tiempo_arribo)
        return tiempos_arribo
    


# Distribución de Poisson con media de 5 minutos
lambda_poisson = 1 / 5
