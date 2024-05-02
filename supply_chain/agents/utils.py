from abc import ABC, abstractmethod

from supply_chain.agents.new.logic import *

from enum import Enum

import uuid

def generate_guid():
    return str(uuid.uuid4())

def float_to_string(float_number):
    return str(float_number).replace('.', '_')

def convert_to_float(input_string:str):
    """
    Convierte del lenguaje que se hace las inferencias que devuelve un string
    a un float
    Si no puede devuelve None
    :param input_string:
    :return:
    """
    if input_string.startswith("Float_"):
        without_prefix = input_string[6:]  # Remove the "Float_" prefix
        replaced = without_prefix.replace("_", ".")  # Replace underscores with periods
        return float(replaced)  # Convert to float
    else:
        return None  # Return None if the string does not start with "Float_"

# Usage
input_string = "Float_3_14159"
output = convert_to_float(input_string)
print(output)  # Output: 3.14159

class ValoracionTag(Enum):
    Fatal = 'Fatal'
    Mal = 'Mal'
    Regular = 'Regular'
    Bien = 'Bien'
    MuyBien = 'Muy_bien'
    Excelente = 'Excelente'

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

    def __str__(self):
        return self.show()


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
    """Clase para el inferenciador de los SE de los agentes"""

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
                 value:  float):
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
        return "Float"


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
                 valoracion: ValoracionTag | str
                 ):
        self.client_name: str = client_name
        self.valoracion_str: str = str(valoracion)
        self.valoracion: ValoracionTag | str = valoracion

    @property
    def tag(self):
        return 'Valoracion'

    def show(self) -> str:
        return f'{self.tag}_({self.client_name},{self.valoracion_str})'





class LogicOperatorsWrapped(LogicWrapped):
    def _get_the_show_str(self):
        s = ''

        for expr in self.list_wrapped_original:
            str_expr = expr.show()
            s += f' {str_expr} {self.tag}  '

        return s

    def __init__(self,
                 list_wrapped: list[LogicWrapped]
                 ):
        self.list_wrapped_original: list[LogicWrapped] = list_wrapped

        self.string_: str = f'({self._get_the_show_str()})'

    @property
    @abstractmethod
    def tag(self) -> str:
        pass

    @abstractmethod
    def show(self):
        return self.string_


class NotLogicWrapped(LogicOperatorsWrapped):
    def tag(self) -> str:
        return '~'


class AndLogicWrapped(LogicOperatorsWrapped):

    def tag(self) -> str:
        return '&'


class OrLogicWrapped(LogicOperatorsWrapped):

    def tag(self) -> str:
        return '|'


class ImplicationLogicWrapped(LogicWrapped):

    def to_str(self, lis: list[LogicWrapped]):
        s = ''
        for item in lis:
            s += f' {item.show()}  '

        return s

    def __init__(self,
                 left_part: list[LogicWrapped],
                 right_part: list[LogicWrapped]

                 ):
        self.left_part: list[LogicWrapped] = left_part
        self.right_part: list[LogicWrapped] = right_part
        self.string_: str = f'{self.to_str(self.left_part)} {self.tag} {self.to_str(self.right_part)}'

    @property
    @abstractmethod
    def tag(self) -> str:
        return '==>'

    @abstractmethod
    def show(self):
        return self.string_
