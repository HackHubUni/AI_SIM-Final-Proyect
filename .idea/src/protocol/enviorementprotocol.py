from collections import abc

class Envioerment(abc.Protocol):
    def envio(self, origin, destination):
        #devuelve una tupla de tiempo, valor
        pass