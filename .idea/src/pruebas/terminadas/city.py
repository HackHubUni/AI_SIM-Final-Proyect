class Node:
    def __init__(self, value):
        self.value = value
        self.neighbors = []
        self.visited = False
    
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
    
    def __repr__(self):
        return f"Node({self.value})"
    
    def delete_neighbor(self, neighbor):
        self.neighbors.remove(neighbor)
    
    
