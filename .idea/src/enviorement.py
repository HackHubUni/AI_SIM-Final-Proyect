import queue
import time as t
class Env:
    def __init__(self,city):
        self.time =  t.time()
        self.Producer = set()
        self.Product = set()
        self.Shop = set()
        self.Product_Producer = {}
        self.city = city


class EnviorementEmp:
    def __init__(self, env:Env, stock):
        self.env = env
        self.requestarrival= queue.Queue()
       
        if stock is None:
            self.stock = {}
        else:
            self.stock = stock
        self.need = queue.Queue()
        self.R = 0 # ingreso de solicitudes satisfechas ganacia 
        self.P = 0 # ingreso de solicitudes no satisfechas perdida
        
        

    def time(self):
        return self.env.time
    def replacent_cost(self,product, amount): #Costo de reemplazo R
        #devuelve el costo de reemplazo de un producto buscando la mejor opcion mirando 
        #el costo de reemplazo de los productos en el ambiente y el precio de tranportacion
        pass
    def  storage_cost(self,env,product, amount):#Costo de almacenaje H
        #devuelve el costo por almacenaje del producto esto lo tiene cada producto
        pass

     
    
class ShopRequest:
    def __init__(self,product:list, amount:list, time, shop):
        self.Shop = shop
        self.product = product # lista de productos, price
        self.request_time = time
        self.amount = amount

    def print(self):
        return(print("{Product}, cant = {amount}, time = {t}", self.product,self.amount,self.amount))
    

#class EnviorementShop():
    
    