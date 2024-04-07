from collections import abc
from productprotocol import *

class Producer():
    def __init__(self,product:Product, name):
        self.name = name
        self.product = product  