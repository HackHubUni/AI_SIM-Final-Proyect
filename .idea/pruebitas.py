from random import random
import math
# Distribución de Poisson con media de 5 minutos
lambda_poisson = 1 / 5

# Generar 10 tiempos de arribo
tiempos_arribo = []
for i in range(10):
    # Número aleatorio entre 0 y 1
    u = random()

    # Función inversa de la distribución de Poisson
    tiempo_arribo = -math.log(u) / lambda_poisson

    tiempos_arribo.append(tiempo_arribo)

print(tiempos_arribo)


from random import random
from time import sleep

# Distribución exponencial con media de 100 milisegundos
lambda_exp = 1 / 0.1

# Generar 10 tiempos de arribo
tiempos_arribo = []
for i in range(10):
    # Número aleatorio entre 0 y 1
    u = random()

    # Función inversa de la distribución exponencial
    tiempo_arribo = -math.log(u) / lambda_exp

    # Retardo en milisegundos
    sleep(tiempo_arribo * 1000)

    tiempos_arribo.append(tiempo_arribo)

print(tiempos_arribo)
