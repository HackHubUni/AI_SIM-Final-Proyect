

import itertools
import numpy as np
import search
from utils import *
from logic import *
from search import *
from planning import *


def get_solution(problem):
    solutions = [x.solution() for x in uniform_cost_search(ForwardPlan(problem))]

    #print(type(solution[0]))
    lis=[]
    for solution in solutions:
        solution = list(map(lambda action: Expr(action.name, *action.args), solution))
        lis.append(solution)
    return lis



def new__():
    return PlanningProblem(initial='Pedir(Pizza,Primera)',
                           goals='Abastecer(Pizza,Primera) ',
                           actions=[
                               Action('Preguntar_trasnportista_desde_almacen(x,y)',
                                      precond=' Transportista_desde_almacen(x,y)',
                                      effect='Abastecer(x,y) ',
                                      domain=' Producto(x) & Tienda(y)'),




                               Action('Disponibilidad_almacen(x,y)',
                                      precond='Cant_en_almacen(x,y) ',
                                      effect='Transportista_desde_almacen(x,y) ',
                                      domain=' Producto(x) & Tienda(y)'),


                               Action('Enviar_a_tienda_desde_manufacturero(x,y)',
                                      precond='Enviar_tienda(x,y) ',
                                      effect='Abastecer(x,y) ',
                                      domain=' Producto(x) & Tienda(y)'),

                               Action('Desde_Manufacturero(x,y)',
                                      precond='Preguntar_Manufacturero(x,y)',
                                      effect=' Enviar_tienda(x,y)',
                                      domain=' Producto(x) & Tienda(y)'),


                               Action('Disponibilidad_Manufacturero(x,y)',
                                      precond='Disponibilidad_Manufacturero(x,y) ',
                                      effect='Preguntar_Manufacturero(x,y) ',
                                      domain=' Producto(x) & Tienda(y)'),












                               Action('Iniciar_Preguntas(x,y)',
                                      precond='Pedir(x,y) ',
                                      effect='Cant_en_almacen(x,y) ',
                                      domain=' Producto(x) & Tienda(y)'),
                               Action('Iniciar_Preguntas(x,y)',
                                      precond='Pedir(x,y) ',
                                      effect='Disponibilidad_Manufacturero(x,y) ',
                                      domain=' Producto(x) & Tienda(y)'),











                           ],

                           domain='Tienda(Primera) & Producto(Pizza) & Manufacturera(Manu) & Distribuidor(Dist)  ')





if __name__ =='__main__':
    print(get_solution(new__()))