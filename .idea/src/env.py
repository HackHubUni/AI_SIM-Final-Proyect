import queue
import time as t
class Env:
    def __init__(self,city):
        self.time =  t.time()
        self.Producer = set()
        self.Product_Producer = {}
        self.city = city
        self.R = 0 # ingreso de solicitudes satisfechas ganacia 
        self.P = 0 # ingreso de solicitudes no satisfechas perdida



    


class EnvionmentEmp:
    def __init__(self, env, stock, emp):
        self.env = env
        self.requestarrival= queue.Queue()
       
        if stock is None:
            self.stock = {}
        else:
            self.stock = stock
        self.need = queue.Queue()
        self.R = 0 # ingreso de solicitudes satisfechas ganacia 
        self.P = 0 # ingreso de solicitudes no satisfechas perdida
        self.emp = emp # agente qe modela a la empresa
        
        

    def time(self):
        return self.env.time
    def replacent_cost(self,env,product, amount): #Costo de reemplazo
        #devuelve el costo de reemplazo de un producto buscando la mejor opcion mirando 
        #el costo de reemplazo de los productos en el ambiente y el precio de tranportacion
        pass
    def  storage_cost(self,env,product, amount):#Costo de almacenaje H
        #devuelve el costo por almacenaje del producto esto lo tiene cada producto
        pass

    #EVENTO DE SOLICITUD ( CUANDO LA TIENDA M PIDE)
    def check_request(self):
        while True:
            t.sleep(1)
            if not self.requestarrival.empty():
                request =self.requestarrival.get()
                
                    


    
    
class ShopRequest:
    def __init__(self,product, amount, time):
        self.product = product
        self.request_time = time
        self.amount = amount

    def print(self):
        return(print("{Product}, cant = {amount}, time = {t}", self.product,self.amount,self.amount))
    
    