from abc import ABC, abstractmethod

from supply_chain.agents.new.logic import *

from enum import Enum


def float_to_string(float_number):
    return str(float_number).replace('.', '_')


class ValoracionTag(Enum):
    Mal = 'Mal'
    Bien = 'Bien'
    MuyBien = 'Muy_bien'

    def __str__(self):
        return self.value


class LogicWrapped(ABC):

    @property
    @abstractmethod
    def tag(self) -> str:
        pass

    @abstractmethod
    def show(self):
        pass

    def _float_to_string(self, float_number):
        return str(float_number).replace('.', '_')


class StringWrapped(LogicWrapped):
    def __init__(self,
                 name: str | int | float):
        self.name: str = str(name)
        self.original_name = name

    @property
    @abstractmethod
    def tag(self):
        pass

    @property
    def wrapped(self):
        return f'{self.tag}({self.name})'

    def show(self) -> str:
        """PAra mandar al inferenciador"""
        return self.wrapped

    @property
    def get_original_name(self):
        """Devuelve el nombre sin wrapped"""
        return self.original_name

    @property
    def get_wrapped_name(self):
        """Devuelve el nombre wrappeado para el inferenciador"""
        return self.wrapped

    def __repr__(self):
        return self.wrapped


class ClientWrapped(StringWrapped):
    def __init__(self,
                 name: str):
        super().__init__(name)

    @property
    def tag(self):
        return 'Client'


class ProductWrapped(StringWrapped):
    def __init__(self,
                 name: str):
        super().__init__(name)

    @property
    def tag(self):
        return 'Product'


class NumberWrapped(StringWrapped):
    def float_to_string(self, float_number):
        self.name = str(float_number).replace('.', '_')

    def __init__(self,
                 value: int | float):
        super().__init__(value)
        self.number_inst = value
        self.float_to_string(value)

    @property
    def wrapped(self):
        return f'{self.tag}_{self.name}'

    def show(self) -> str:
        """PAra mandar al inferenciador"""
        return self.wrapped

    @property
    def tag(self):
        return "Int" if isinstance(self.number_inst, float) else "Float"


class PedirBase(LogicWrapped):
    def __init__(self,
                 client: str | StringWrapped,
                 product_want: str | StringWrapped,
                 count: NumberWrapped | str):
        self.client_name: str = client.original_name if isinstance(client, StringWrapped) else client
        self.client: ClientWrapped | str = client
        self.product_want_name: str = product_want.get_original_name if isinstance(product_want,
                                                                                   StringWrapped) else product_want
        self.product_want: ProductWrapped | str = product_want
        self.count_value: str = count.get_original_name if isinstance(count, NumberWrapped) else count
        self.count: NumberWrapped | str = count

    @property
    @abstractmethod
    def tag(self):
        pass

    def _show(self):
        client_str = self.client.get_wrapped_name if isinstance(self.client,
                                                                ClientWrapped) else self.client

        product_str = self.product_want.get_wrapped_name if isinstance(self.product_want,
                                                                       ClientWrapped) else self.product_want_name

        count_str = self.count.get_wrapped_name if isinstance(self.count,
                                                              NumberWrapped) else float_to_string(self.count_value)

        return f'{self.tag}({client_str},{product_str},{count_str})'

    def show(self) -> str:
        return self._show()

    def __repr__(self):
        return self._show()

    def start(self):
        self._show()


class PedirCantidad(PedirBase):
    def __init__(self,
                 client: str | StringWrapped,
                 product_want: str | StringWrapped,
                 count: str | NumberWrapped):
        super().__init__(client, product_want, count)

    @property
    def tag(self):
        return 'Pedir_cantidad'


class PedirPrecio(PedirBase):
    def __init__(self,
                 client: str | StringWrapped,
                 product_want: str | StringWrapped,
                 count: str | NumberWrapped

                 ):
        super().__init__(client=client,
                         product_want=product_want,
                         count=count)

    @property
    def tag(self):
        return 'Pedir_precio'


class Valoracion(LogicWrapped):
    def __init__(self,
                 client_name: str,
                 valoracion: ValoracionTag
                 ):
        self.client_name: str = client_name
        self.valoracion_str: str = str(valoracion)
        self.valoracion: ValoracionTag = valoracion

    @property
    def tag(self):
        return 'Valoracion'

    def show(self) -> str:
        return f'{self.tag}_({self.client_name},{self.valoracion_str})'


def main():
    """A knowledge base consisting of first-order definite clauses.
       >>> kb0 = FolKB([expr('Farmer(Mac)'), expr('Rabbit(Pete)'),
       ...              expr('(Rabbit(r) & Farmer(f)) ==> Hates(f, r)')])
       >>> kb0.tell(expr('Rabbit(Flopsie)'))
       >>> kb0.retract(expr('Rabbit(Pete)'))
       >>> kb0.ask(expr('Hates(Mac, x)'))[x]
       Flopsie
       >>> kb0.ask(expr('Wife(Pete, x)'))
       False


       """

    kb0 = FolKB([expr('Cliente(Juan)'), expr('Valoracion(Juan,Buena)'), expr('Producto(Tomate)'),
                 expr('Cliente(x) & Valoracion(x,Buena) & Producto(y)  ==> Preguntar_precio(x,y,Mantener)')])
    # print(kb0.tell(expr('Rabbit(Flopsie)')))
    # print(kb0.retract(expr('Rabbit(Pete)')))
    print(kb0.ask(expr('Preguntar_precio(Juan,Tomate,x)'))[x])


def main2():
    cliente = ClientWrapped("Juan").show()
    print(cliente)
    valoracion = Valoracion('Juan', ValoracionTag.Bien).show()
    print(valoracion)

    producto = ProductWrapped('Tomate').show()
    print(producto)

    cliente_x = ClientWrapped('x').show()
    valoracion_x_bien = Valoracion("x", ValoracionTag.Bien).show()

    product_y = ProductWrapped('y').show()

    pedir_precio_ = PedirPrecio('Juan', 'Tomate', "x").show()
    print(pedir_precio_)

    pedir_precio_hecho = PedirPrecio('x', 'y', NumberWrapped(1))

    kb0 = FolKB()

    lis = [expr(cliente), expr(valoracion), expr(producto),
           expr(
               f'({cliente_x} & ({valoracion_x_bien} & {product_y}))  ==> {pedir_precio_hecho}')

           ,# f'{Valoracion('x',ValoracionTag.Bien).show()} ==> {Valoracion('Juan',ValoracionTag.Bien).show()}'
           ]
    print(lis)
    for item in lis:
        kb0.tell(item)


    print(kb0.ask(expr(pedir_precio_))[x])
    query=Valoracion('Juan', 'x').show()
    print(query)
    fcf:dict=kb0.ask(expr(query))

    key=list(fcf.keys())
    print(key)
    print(type(fcf[key[0]]))
    s=str(fcf[key[0]])
    print(s)


if __name__ == "__main__":
    main2()
