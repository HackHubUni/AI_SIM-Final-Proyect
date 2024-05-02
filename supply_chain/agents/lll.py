

class A:
   def __init__(self,name):
       self.name=name



class B:

    def __init__(self, name):
        self.name = name





def get(type_class):
    return type_class(5)


print(type(get(A)))


