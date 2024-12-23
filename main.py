from neonodal.neonodal import Neonodal


initial_nodes = ['A', 'B', 'C']
initial_edges = [('A', 'B'), ('B', 'C'), ('C', 'A'), ('A', 'A'), ('A', 'A')]
graph = Neonodal.Graph(directed=False, nodes=initial_nodes, edges=initial_edges)

graph.__repr__()

graph.add('D')
graph.add('E', 'F') 
graph.add_edges([('C', 'D'), ('D', 'A')]) 
graph.add_nodes(['G', 'H'])  
print('\nUpdated Graph:')
graph.__repr__()

# Pull edges for a specific node
print("\nEdges for node 'A':", graph.pull('A')) 
print("Edges for node 'B':", graph.pull('B'))  
print("Edges for node 'E':", graph.pull('E')) 

print("Count of edge ('A', 'B'):", graph.pull(('A', 'B')))  

print('\nAdjacency List:', graph.convert('adjacency_list'))
print('Adjacency Matrix:', graph.convert('adjacency_matrix'))
print('Pure Matrix:', graph.convert('pure_matrix'))
print(graph.degrees())
print(graph.net_degrees()) ### error as graph is undirected

star = Neonodal.Star(True, 4)
print(star.net_degrees())
print(star.in_degrees())
star.show() ### WIP 