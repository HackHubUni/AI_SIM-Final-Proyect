import networkx as nx
import matplotlib.pyplot as plt

# Definir los nodos y aristas
nodes = ["Intersección 1", "Intersección 2", "Edificio A", "Parque"]
edges = [("Intersección 1", "Intersección 2"), ("Intersección 1", "Edificio A"), ("Intersección 2", "Parque")]

# Crear el grafo
grafo = nx.Graph()
grafo.add_nodes_from(nodes)
grafo.add_edges_from(edges)

# Agregar atributos
nx.set_node_attributes(grafo, {"tipo": {"Intersección 1": "interseccion", "Intersección 2": "interseccion", "Edificio A": "edificio", "Parque": "parque"}})
nx.set_edge_attributes(grafo, {"longitud": {"Intersección 1": {"Intersección 2": 100, "Intersección 1": {"Edificio A": 50, "Intersección 2": {"Parque": 200}}}}})

# Visualizar el grafo
pos = nx.spring_layout(grafo)
nx.draw(grafo, pos, with_labels=True)
labels = nx.get_edge_attributes(grafo, "longitud")
nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)
plt.show()
