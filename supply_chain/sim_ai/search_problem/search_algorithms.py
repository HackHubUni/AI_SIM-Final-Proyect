# from supply_chain.sim_ai.search_problem.search_node import
from supply_chain.sim_ai.search_problem.frontier import *


def basic_search_algorithm(
    problem: SearchProblem, frontier: Frontier, memory_limit=1e6
) -> tuple[bool, SearchNode]:
    """This method execute the common logic of all search algorithms.
    The difference between search algorithms is the choice of the frontier"""
    # visited_nodes:set = set()
    visited_nodes = []
    frontier.clear()
    frontier.push(SearchNode(problem.initial_state))
    while (
        not frontier.is_empty() or (len(visited_nodes) + len(frontier)) < memory_limit
    ):
        node = frontier.pop()
        visited_nodes.append(node.state)
        if problem.is_final(node.state):
            return True, node
        reachable_nodes = node.expand_node(problem)
        for n in reachable_nodes:
            if n.state not in visited_nodes and not frontier.contains(n):
                frontier.push(n)
    return False, None
