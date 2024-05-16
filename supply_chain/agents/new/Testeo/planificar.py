import itertools
import numpy as np
from supply_chain.agents.new.search import *
from supply_chain.agents.new.utils import *
from supply_chain.agents.new.logic import *
from supply_chain.agents.new.search import *
from supply_chain.agents.new.planning import *


def get_solution(problem):
    solutions = [x.solution() for x in uniform_cost_search(ForwardPlan(problem))]

    # print(type(solution[0]))
    lis = []
    for solution in solutions:
        solution = list(map(lambda action: Expr(action.name, *action.args), solution))
        lis.append(solution)
    return lis


def planing():
    return PlanningProblem(initial='Pedir(Pizza,Primera)',
                           goals='Abastecer(Pizza,Primera) ',
                           actions=[Action('Abastecida_tienda(x,y) ',
                                           precond='Comprar(x,y)',
                                           effect='Abastecer(x,y)',
                                           domain='Tienda(y) & Comida(x)'),

                                    Action('Preguntar_trasnportista_desde_almacen(x,y)',
                                           precond='Cant_en_almacen(x,y)',
                                           effect='Abastecer(x,y) ',
                                           domain=' Producto(x) & Tienda(y)'),

                                    Action('Preguntar_disponibilidad_almacen(x,y)',
                                           precond='Pedir(x,y) & ~Precio_manufacturera(x,y)',
                                           effect='Cant_en_almacen(x,y)  ',
                                           domain=' Producto(x) & Tienda(y)'),

                                    Action('Preguntar_distribuidor_desde_almacen(x,y)',
                                           precond='Preguntar_distribuidor(x,y) & Preguntar_almacen(x,y)',
                                           effect='Abastecer(x,y)  ',
                                           domain=' Producto(x) & Tienda(y)'),

                                    Action('Preguntar_distribuidormm(x,y)',
                                           precond='Preguntar_almacen(x,y)',
                                           effect='Preguntar_distribuidor(x,y)  ',
                                           domain=' Producto(x) & Tienda(y)'),

                                    Action('Preguntar_almacen(x,y)',
                                           precond='Precio_manufacturera(x,y)',
                                           effect='Preguntar_almacen(x,y) ',
                                           domain=' Producto(x) & Tienda(y)'),

                                    Action('Preguntar_precio_manufacturera(x,y)',
                                           precond='Pedir(x,y)',
                                           effect='Precio_manufacturera(x,y) & Cant_en_almacen(x,y)',
                                           domain='Producto(x) & Tienda(y)'),








                                     Action('Pedir_precio_almacen(x,y)',
                                            precond='Precio_manufacturera(x,y)',
                                            effect='Precio_almacen(x,y) ',
                                            domain='Producto(x)  & Manufacturera(y) & Tienda(z) '),

                                     Action('Pedir_precio_distribuidor(x,y,z)',
                                            precond='Precio_almacen(x,y) & Precio_manufacturera(x,z)',
                                            effect='Precio_distribuidor(x,y,z)',
                                            domain='Producto(x) & Almacen(y)  & Manufacturera(z)'),

                                     Action('Pedir_precio_distribuidor(x,y,z)',
                                            precond='Pedir(w) & Precio_almacen(x,y) & Precio_manufacturera(x,z) & Precio_distribuidor(x,y,z)',
                                            effect='Abastecer(x,w)',
                                            domain='Producto(x) & Almacen(y)  & Manufacturera(z) & Tienda(w)'),

                                    ],

                           domain='Tienda(Primera) & Producto(Pizza) & Manufacturera(Manu) & Distribuidor(Dist) ')

def example():
    get_solution(planing())

if __name__ == '__main__':
    print(example())
