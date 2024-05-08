
graph = { 'source':{'f':(303934,455,0)},
                    #    Capacidad max, coste, cuanto se movio si es mayor que cero es importante
    'f': {'A': (5, 1, 0), 'D': (2, 2, 0)},
    'A': {'C': (12, 3, 0),'sink':(4,7,0)},
    'C': { 'D': (20, 7, 0)},
    'D': {'C': (7, 8, 0), 'sink': (6, 9, 0)},
    'sink': {}
}

# Nombre de destino : llegadas

def min_cost_max_flow(graph, source, sink):
    max_flow = 0
    parent = {}

    def bfs():
        visited = set()
        queue = [(source, float("Inf"))]

        while queue:
            node, path_flow = queue.pop(0)
            visited.add(node)

            for neighbor, (capacity, cost, flow) in graph[node].items():
                if neighbor not in visited and capacity > flow:
                    parent[neighbor] = (node, min(path_flow, capacity - flow))
                    if neighbor == sink:
                        return parent[neighbor][1]
                    queue.append((neighbor, parent[neighbor][1]))

        return 0

    while True:
        path_flow = bfs()
        if path_flow == 0:
            break

        max_flow += path_flow
        v = sink
        while v != source:
            u, flow = parent[v]
            graph[u][v] = (graph[u][v][0], graph[u][v][1], graph[u][v][2] + path_flow)
            if v in graph and u in graph[v]:
                graph[v][u] = (graph[v][u][0], graph[v][u][1], graph[v][u][2] - path_flow)
            else:
                graph[v][u] = (0, -graph[u][v][1], -path_flow)
            v = u
    print(graph)
    return max_flow, graph

source = 'source'
sink = 'sink'

max_flow,graph = min_cost_max_flow(graph, source, sink)
print(f"Flujo máximo con costo mínimo: {max_flow}")