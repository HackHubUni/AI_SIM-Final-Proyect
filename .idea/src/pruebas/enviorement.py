import queue
import time as t
class Env:
    def __init__(self,city):
        self.time =  t.time()
        self.Producers = set()# lista de productores en la simulacion( empresas monoproductoras o productores)
        self.Products = set()#lista de productos en la simulacion
        self.Shops = set()# lista de tiendas creadas en la simulacion
        self.city = city# ciudades de la simulacion
        self = self.Companies = set()# lista de empresas en la simulacion

        self.Product_Producer = {}# QUE ERA ESTOOOOOOOOOO
        


class EnviorementEmp:
    def __init__(self, env:Env, stock):
        self.env = env #referencia al enviorement general
        self.requestarrival= queue.Queue() # cola de solicitudes de productos
       #stock de la empresa
        if stock is None:
            self.stock = {}
        else:
            self.stock = stock
        self.R = 0 # ingreso de solicitudes satisfechas ganacia 
        self.P = 0 # ingreso de solicitudes no satisfechas perdida
        self.Replacent_Cost =set() # MODIFICAR guarda el costo de llegar de los proveedores ala empresa producer,cost
        self.Balance = 0 # balance de la empresa
        
        
        self.need = queue.Queue()#productos que necesita la empresa NO SE SI ESTA EN USO

    def time(self):
        return self.env.time
    def replacent_cost(self,product, amount): #Costo de reemplazo R
        #devuelve el costo de reemplazo de un producto buscando la mejor opcion mirando 
        #el costo de reemplazo de los productos en el ambiente y el precio de transportacion
        pass
    def  storage_cost(self,env,product, amount):#Costo de almacenaje H
        #devuelve el costo por almacenaje del producto esto lo tiene cada producto
        pass
    def update_product(self,product,amount):# update de stock comprando el producto
        pass

class EnviorementShop:
    def __init__(self,env:Env,) :
        self.env = env
        self.time = t.time()
        self.number_of_arrival = 0
        self.number_of_arrival = 0
        self.arrival_time = {}
        self.departure_time = {}
        self.number_of_clients = 0

    
        

class ShopRequest:
    def __init__(self,product:list, amount:list, time, shop):
        self.Shop = shop
        self.product = product # lista de productos, price
        self.request_time = time
        self.amount = amount

    def print(self):
        return(print("{Product}, cant = {amount}, time = {t}", self.product,self.amount,self.amount))




class ShopDelivery:
    def __init__(self,product:list, amount:list, time, shop):
        self.Shop = shop
        self.product = product # lista de productos
        self.request_time = time
        self.amount = amount

    def print(self):
        return(print("{Product}, cant = {amount}, time = {t}", self.product,self.amount,self.amount))  

#class EnviorementShop():
    
    