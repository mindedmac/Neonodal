from neonodal.__init__ import *


class Neonodal:
    def __init__(self):
        pass
    
    class Graph:
        def __init__(self, directed: bool = False, nodes: List[any] = None, edges: List[Tuple[any, any]] = None) -> None:
            self.directed = directed
            self.nodes: List[str] = nodes if nodes is not None else []
            self.edges: List[Tuple[str, str]] = edges if edges is not None else []
            for start, end in self.edges:
                self.add_nodes(start)
                self.add_nodes(end)

        def add(self, start: str, end: str = None) -> None:
            """Add a node or an edge.  If only a node is provided, it adds that node. 
            If both start and end are provided it adds an edge between them. to prevent future errors"""
            if end is None:
                if start not in self.nodes:
                    self.nodes.append(start)
            else:
                if start not in self.nodes:
                    self.nodes.append(start)
                if end not in self.nodes:
                    self.nodes.append(end)
                self.edges.append((start, end))

        def add_nodes(self, nodes: Union[List[int], List[str], str]) -> None:
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
            if isinstance(edges, tuple):
                self.add(*edges)
            else:
                for start, end in edges:
                    self.add(start, end)

        def pull(self, node: any) -> Union[Dict[any, any], int]:
            """Get edges for a node and count timea, or count an edge if a tuple is given."""
            if isinstance(node, tuple):
                return self.count_edge(node)
            
            if node not in self.nodes:
                raise ValueError(f"Node '{node}' does not exist in the graph.")

            edge_count = {}
            for start, end in self.edges:
                if start == node:
                    edge_count[(start, end)] = edge_count.get((start, end), 0) + 1
                elif end == node and not self.directed:
                    edge_count[(end, start)] = edge_count.get((end, start), 0) + 1

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
            adjacency_list = {node: [] for node in self.nodes}
            for start, end in self.edges:
                adjacency_list[start].append(end)
                if start != end and not self.directed:
                    adjacency_list[end].append(start)
            return adjacency_list

        def to_adjacency_matrix(self) -> Dict[any, Dict[any, any]]:
            adjacency_matrix = {node: {n: 0 for n in self.nodes} for node in self.nodes}
            for start, end in self.edges:
                adjacency_matrix[start][end] += 1
                if start != end and not self.directed:
                    adjacency_matrix[end][start] += 1
            return adjacency_matrix

        def to_pure_matrix(self) -> List[List[int]]:
            matrix = [[0] * len(self.nodes) for r in range(len(self.nodes))]
            index = {node: n for n, node in enumerate(self.nodes)}
            for start, end in self.edges:
                matrix[index[start]][index[end]] += 1
                if start != end and not self.directed:
                    matrix[index[end]][index[start]] += 1
            return matrix
        
        def _degrees(self) -> Dict[any, int]:
            return {node: len(neighbors) for node, neighbors in self.to_adjacency_list().items()}
            
        def degrees(self) -> Dict[any, int]:
            return self._degrees() if not self.directed else ValueError('Cannot call degrees on directed graph')

        def out_degrees(self) -> Dict[any, int]:
            return self._degrees() if self.directed else ValueError('Cannot call out_degrees on an undirected graph')
        
        def in_degrees(self) -> Dict[any, int]:
            return {node: (self.net_degrees())[node] - (self.out_degrees())[node] for node in self.nodes}
        
        def net_degrees(self) -> Dict[any, int]:
            self.graph = Neonodal.Graph(False, self.nodes, self.edges)
            return self.graph.degrees() if self.directed else ValueError('Cannot call net_degrees on an undirected graph')

        def show(self) -> None:
            graph = nx.Graph()
            graph.add_edges_from(self.edges)
            nx.draw_networkx(graph)
            plt.show()

        def __repr__(self) -> None:
            print("Nodes:", self.nodes)
            print("Edges:", self.edges)
            print("Adjacency List:", self.to_adjacency_list())
            print("Adjacency Matrix:", self.to_adjacency_matrix())
            print("Pure Matrix:", self.to_pure_matrix())
            
    class Path(Graph):
        def __init__(self, directed: bool = False, nodes: int = 2) -> None:
            self.nodes = range(nodes)
            self.edges = [(u, u + 1)for u in range(nodes - 1)]
            super().__init__(directed, self.nodes, self.edges)
            
        def __repr__(self) -> None:
            super().__repr__()
            
    class Cycle(Graph):
        def __init__(self, directed: bool = False, nodes: int = 2) -> None:
            self.path = self.Path(directed, nodes)
            self.path.append((nodes - 1, ))
            
        def __repr__(self) -> None:
            super().__repr__()
            
    class Complete(Graph):
        def __init__(self, directed: bool = False, nodes: int = 2) -> None:
            self.nodes = range(nodes)
            self.edges = list(combinations(self.nodes, 2))
            super().__init__(directed, self.nodes, self.edges)
            
        def __repr__(self) -> None:
            super().__repr__()
            
    class Star(Graph):
        def __init__(self, directed: bool = False, nodes: int = 2) -> None:
            self.nodes = [i for i in range(nodes)]
            self.edges = [(0, i) for i in range(1, nodes)]
            super().__init__(directed, self.nodes, self.edges)
            
        def __repr__(self) -> None:
            super().__repr__()