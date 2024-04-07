from collections import abc

class Product(abc.Protocol):

    def price(self):
         pass
    
    def proper_temperature(self, temperature):
        #si la temperatura wes adecuada
        pass    
    def proper_humidity(self, humidity):
        pass

class BaseProduct(Product):
    def __init__(self, name, quality, gross_price, ideal_temperature,ideal_humidity, time_to_produce):
        self.name = name
        self.quality = quality
        self.gross_price = gross_price
        self.ideal_temperature = ideal_temperature
        self.time_to_produce = time_to_produce
        
        self.ideal_humidity = ideal_humidity

    
    def price(self):
        return self.quality * self.gross_price
    
    def proper_temperature(self, temperature):
        if not self.ideal_temperature - temperature < 2:
            self.quality -= 1
    
    def proper_humidity(self, humidity):
        if not self.ideal_humidity - humidity < 2:
            self.quality -= 1


   
class ProcessedProduct(BaseProduct, Product):
    def __init__(self, name, quality, gross_price, time_to_produce, ideal_temperature, ideal_humidity,ingredients:list):
        super().__init__(name, quality, gross_price, ideal_temperature, ideal_humidity, time_to_produce)
        self.ingredients = ingredients#(Product, int)
        self.create = False

    def price(self):
        return self.quality * self.gross_price
    
    def proper_temperature(self, temperature):
        if not self.ideal_temperature - temperature < 2:
            self.quality -= 1

    def proper_humidity(self, humidity):
        if not self.ideal_humidity - humidity < 2:
            self.quality -= 1

    def produce(self, ingredients):
        count = 0
        qualities = 0
        for ingredient in self.ingredients:
            for i in ingredients:
                if ingredient[0].name == i[0].name:
                    count += 1
                    if i[1] < ingredient[1]:
                        return False
                    qualities += i[0].quality
        if count == len(self.ingredients):
            self.quality =  qualities/count  
            self.create = True
           
                


    