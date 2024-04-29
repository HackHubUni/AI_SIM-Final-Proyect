# from supply_chain.sim_ai.search_problem.search_node import
from .frontier import *
from .frontiers.priority_frontier import (
    PriorityFrontier,
)
from .frontiers.queue_frontier import QueueFrontier


def basic_search_algorithm(
    problem: SearchProblem,
    frontier: Frontier,
) -> tuple[bool, SearchNode]:
    """This method execute the common logic of all search algorithms.
    The difference between search algorithms is the choice of the frontier"""
    node = SearchNode(problem.initial_state)
    visited_nodes = {node.state: node}
    frontier.clear()
    frontier.push(node)
    while not frontier.is_empty():
        node = frontier.pop()
        if problem.is_final(node.state):
            return True, node
        reachable_nodes = node.expand_node(problem)
        for child in reachable_nodes:
            child_state = child.state
            if (
                child_state not in visited_nodes
                or child.path_cost < visited_nodes[child_state].path_cost
            ):
                visited_nodes[child_state] = child
                frontier.push(child)
    return False, None


def a_star_search(
    problem: SearchProblem,
    heuristic_function: Callable[[SearchNode], float],
) -> tuple[bool, SearchNode]:
    frontier = PriorityFrontier(
        lambda node: node.path_cost + heuristic_function(node)
    )  # This is the same as the 'g(n) + h(n)' of the A*
    return basic_search_algorithm(problem=problem, frontier=frontier)


def breadth_first_search(
    problem: SearchProblem,
) -> tuple[bool, SearchNode]:
    frontier = QueueFrontier()
    return basic_search_algorithm(problem, frontier)
