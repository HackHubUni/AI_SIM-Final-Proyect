

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
    return PlanningProblem(initial='Casa(A)',
                           goals='Dormir(J,A) ',
                           actions=[  # Action('DD(x,y) ',
                               #       precond='Comprar(x,y)',
                               #       effect='Abastecer(x,y)',
                               #       domain='Tienda(y) & Comida(x)'),

                               #Action('Dormir_directo(x,y)',
                               #       precond='Casa(y)',
                               #       effect='Dormir(x,y)',
                               #       domain='Casa(y) & Persona(x)'),

                               Action('C(x,y)',
                                      precond='Casa(y)',
                                      effect='Caminarcasa(x,y)',
                                      domain='Casa(y) & Persona(x)'),

                               Action('LLEgar(x,y)',
                                      precond='Casa(y)',
                                      effect='Dormir(x,y)',
                                      domain='Casa(y) & Persona(x) '),

                           ],

                           domain='Casa(A) & Persona(J)')





if __name__ =='__main__':
    print(get_solution(new__()))
