from neonodal.__init__ import *


class Neonodal:
    def __init__(self):
        pass
    
    """Represents a basic graph structure with nodes and edges."""
    class Graph:
        def __init__(self, directed: bool = False, nodes: List[any] = None, edges: List[Tuple[any, any]] = None) -> None:
            self.directed = directed
            self.nodes: List[str] = nodes if nodes is not None else []
            self.edges: List[Tuple[str, str]] = edges if edges is not None else []
            for u, v in self.edges:
                self.add_nodes(u)
                self.add_nodes(v)

        def add(self, u: str, v: str = None) -> None:
            """Add a node or an edge.  If only a node is provided, it adds that node. 
            If both u and v are provided it adds an edge between them. to prevent future errors."""
            if v is None:
                if u not in self.nodes:
                    self.nodes.append(u)
            else:
                if u not in self.nodes:
                    self.nodes.append(u)
                if v not in self.nodes:
                    self.nodes.append(v)
                self.edges.append((u, v))

        def add_nodes(self, nodes: Union[List[int], List[str], str]) -> None:
            """Add single or multiple nodes to the graph."""
            if isinstance(nodes, str):
                self.add(*nodes)
            else: 
                ### for List[int] and second for List[str]
                try:
                    for i in range(nodes):
                        self.add(i)
                except:
                    for i in nodes:
                        self.add(i)

        def add_edges(self, edges: Union[List[Tuple[any, any]], Tuple[any, any]]) -> None:
            """Add an edge between two nodes, adding the nodes if they do not exist."""
            if isinstance(edges, tuple):
                self.add(*edges)
            else:
                for u, v in edges:
                    self.add(u, v)

        def pull(self, node: any) -> Union[Dict[any, any], int]:
            """Get edges for a node and count timea, or count an edge if a tuple is given."""
            if isinstance(node, tuple):
                return self.count_edge(node)
            
            if node not in self.nodes:
                raise ValueError(f"Node '{node}' does not exist in the graph.")

            edge_count = {}
            for u, v in self.edges:
                if u == node:
                    edge_count[(u, v)] = edge_count.get((u, v), 0) + 1
                elif v == node and not self.directed:
                    edge_count[(v, u)] = edge_count.get((v, u), 0) + 1

            return edge_count if edge_count else {}

        def count_edge(self, edge: Tuple[str, str]) -> int:
            if self.directed:
                return self.edges.count(edge)
            else:
                return self.edges.count(edge) + (self.edges.count((edge[1], edge[0])) if edge[0] != edge[1] else 0)

        def convert(self, to_type: str) -> Union[Dict[str, List[str]], Dict[str, Dict[str, int]], List[List[int]]]:
            if to_type == 'adjacency_list':
                return self.to_adjacency_list()
            
            elif to_type == 'adjacency_matrix':
                return self.to_adjacency_matrix()
            
            elif to_type == 'pure_matrix':
                return self.to_pure_matrix()
            
            else:
                raise ValueError("Invalid conversion type. Choose 'adjacency_list', 'adjacency_matrix', or 'pure_matrix'.")

        def to_adjacency_list(self) -> Dict[any, List[any]]:
            """Convert the graph to an adjacency list representation."""
            adj_list = {node: [] for node in self.nodes}
            for u, v in self.edges:
                adj_list[u].append(v)
                if not self.directed and u != v:
                    adj_list[v].append(u)
            return adj_list

        def to_adjacency_matrix(self) -> Dict[any, Dict[any, any]]:
            adjacency_matrix = {node: {n: 0 for n in self.nodes} for node in self.nodes}
            for u, v in self.edges:
                adjacency_matrix[u][v] += 1
                if u != v and not self.directed:
                    adjacency_matrix[v][u] += 1
            return adjacency_matrix

        def to_pure_matrix(self) -> List[List[int]]:
            """Convert the graph to a pure adjacency matrix representation."""
            index = {node: idx for idx, node in enumerate(self.nodes)}
            matrix = [[0] * len(self.nodes) for _ in range(len(self.nodes))]
            for u, v in self.edges:
                matrix[index[u]][index[v]] += 1
                if not self.directed and u != v:
                    matrix[index[v]][index[u]] += 1
            return matrix
        
        def _degrees(self) -> Dict[any, int]:
            return {node: len(neighbors) for node, neighbors in self.to_adjacency_list().items()}
            
        def degrees(self) -> Dict[any, int]:
            return self._degrees() if not self.directed else ValueError('Cannot call degrees on directed graph.')

        def out_degrees(self) -> Dict[any, int]:
            return self._degrees() if self.directed else ValueError('Cannot call out_degrees on an undirected graph.')
        
        def in_degrees(self) -> Dict[any, int]:
            return {node: (self.net_degrees())[node] - (self.out_degrees())[node] for node in self.nodes}
        
        def net_degrees(self) -> Dict[any, int]:
            self.graph = Neonodal.Graph(False, self.nodes, self.edges)
            return self.graph.degrees() if self.directed else ValueError('Cannot call net_degrees on an undirected graph.')

        def show(self) -> None:
            """Visualize the graph using matplotlib and networkx."""
            graph = nx.DiGraph() if self.directed else nx.Graph()
            graph.add_nodes_from(self.nodes)
            graph.add_edges_from(self.edges)
            nx.draw_networkx(graph)
            plt.show()

        def __repr__(self) -> None:
            return f'Graph(directed={self.directed}, nodes={self.nodes}, edges={self.edges})'
            
    class Path(Graph):
        def __init__(self, directed: bool = False, nodes: int = 0) -> None:
            self.nodes = [i for i in range(nodes)]
            self.edges = [(u, u + 1)for u in range(nodes - 1)]
            super().__init__(directed, self.nodes, self.edges)
            
        def __repr__(self) -> None:
            super().__repr__()
            
    class Cycle(Path):
        def __init__(self, directed: bool = False, nodes: int = 0) -> None:
            super().__init__(directed, nodes)
            super().add_edges((nodes - 1, 0))
            
        def __repr__(self) -> None:
            super().__repr__()
            
    class Complete(Graph):
        def __init__(self, directed: bool = False, nodes: int = 0) -> None:
            self.nodes = [i for i in range(nodes)]
            self.edges = list(combinations(self.nodes, 2))
            super().__init__(directed, self.nodes, self.edges)
            
        def __repr__(self) -> None:
            super().__repr__()
            
    class Star(Graph):
        def __init__(self, directed: Optional[bool] = False, nodes: int = 0) -> None:
            self.nodes = [i for i in range(nodes)]
            self.edges = [(0, i) for i in range(1, nodes)]
            super().__init__(directed, self.nodes, self.edges)
            
        def __repr__(self) -> None:
            super().__repr__()
            
    class Bipartite(Graph):
        def __init__(self, directed: bool = False, crowns: List[int] = []) -> None:
            if len(crowns) != 2: 
                raise ValueError('Bipartite graph can only have two disjoint & independant sets.')
            self.crowns = crowns
            self.nodes = [i for i in range(self.crowns[0] + self.crowns[1])]
            self.edges = [(u, v) for u in range(self.crowns[0]) for v in range(sum(self.crowns)) if u != v and v not in range(self.crowns[0])]
            super().__init__(directed, self.nodes, self.edges)
        
        def __repr__(self) -> None:
            super().__repr__()
            
    class Intertwined_network(Graph):
        def __init__(self, directed: bool = False, depth: int = 0, crowns: List[int] = [], continuous: bool = False ) -> None:
            if depth != len(crowns): 
                raise ValueError('Depth of Bipartite must match length of crowns.')
            self.crowns = crowns
            self.depth = depth
            self.nodes = [i for i in range(sum(self.crowns))]
            self.edges = []
            if continuous:
                self.edges = [(u, v) for u in range(self.crowns[0]) for v in range(sum(self.crowns)) if u != v and v not in range(self.crowns[0])]    
            else:
                self.edges = [(u, v) for i in range(len(crowns) - 1) for u in range(sum(crowns[:i + 1]) - crowns[i], sum(crowns[:i + 1])) for v in range(sum(crowns[:i + 1]), sum(crowns[:i + 2]))]
            if directed:
                self.edges += [(v, u) for (u, v) in self.edges]
            super().__init__(directed, self.nodes, self.edges)
                
        def __repr__(self) -> None:
            super().__repr__()