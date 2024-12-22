from neonodal.__init__ import *


class Neonodal:
    def __init__(self, directed: bool = False, nodes: List[str] = None, edges: List[Tuple[str, str]] = None):
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

    def add_nodes(self, nodes: Union[List[str], str]) -> None:
        if isinstance(nodes, str):
            self.add(*nodes)
        else:
            for i in nodes:
                self.add(i)

    def add_edges(self, edges: Union[List[Tuple[str, str]], Tuple[str, str]]) -> None:
        if isinstance(edges, tuple):
            self.add(*edges)
        else:
            for start, end in edges:
                self.add(start, end)

    def pull(self, node: str) -> Union[Dict[str, int], int]:
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
            return self.edges.count(edge) + self.edges.count((edge[1], edge[0]))

    def convert(self, to_type: str) -> Union[Dict[str, List[str]], Dict[str, Dict[str, int]], List[List[int]]]:
        if to_type == 'adjacency_list':
            return self.to_adjacency_list()
        
        elif to_type == 'adjacency_matrix':
            return self.to_adjacency_matrix()
        
        elif to_type == 'pure_matrix':
            return self.to_pure_matrix()
        
        else:
            raise ValueError("Invalid conversion type. Choose 'adjacency_list', 'adjacency_matrix', or 'pure_matrix'.")

    def to_adjacency_list(self) -> Dict[str, List[str]]:
        adjacency_list = {node: [] for node in self.nodes}
        for start, end in self.edges:
            adjacency_list[start].append(end)
            if not self.directed:
                adjacency_list[end].append(start)
        return adjacency_list

    def to_adjacency_matrix(self) -> Dict[str, Dict[str, int]]:
        adjacency_matrix = {node: {n: 0 for n in self.nodes} for node in self.nodes}
        for start, end in self.edges:
            adjacency_matrix[start][end] += 1
            if not self.directed:
                adjacency_matrix[end][start] += 1
        return adjacency_matrix

    def to_pure_matrix(self) -> List[List[int]]:
        matrix = [[0] * len(self.nodes) for _ in range(len(self.nodes))]
        index = {node: i for i, node in enumerate(self.nodes)}
        for start, end in self.edges:
            matrix[index[start]][index[end]] += 1
            if not self.directed:
                matrix[index[end]][index[start]] += 1
        return matrix

    def __repr__(self) -> None:
        print("Nodes:", self.nodes)
        print("Edges:", self.edges)
        print("Adjacency List:", self.to_adjacency_list())
        print("Adjacency Matrix:", self.to_adjacency_matrix())
        print("Pure Matrix:", self.to_pure_matrix())