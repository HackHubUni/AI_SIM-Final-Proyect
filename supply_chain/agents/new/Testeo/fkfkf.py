

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
    return PlanningProblem(initial='Preguntar_precio(Juan,Alto)',
                           goals='Precio(Mantener) ',
                           actions=[
                               Action('Preguntar_precio_x(x)',
                                      precond='Preguntar_precio(x,Alto)',
                                      effect='Precio(Mantener)',
                                      domain='Cliente(x)'),

                           ],

                           domain='Cliente(Juan) & Valoracion(Juan,Buena)  ')





if __name__ =='__main__':
    print(get_solution(new__()))