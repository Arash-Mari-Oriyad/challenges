def get_vertex_input_capacity(adjacency_matrix, vertex):
    input_capacity = 0
    for row in adjacency_matrix:
        input_capacity += row[vertex] if row[vertex] > 0 else 0
    return input_capacity


def get_vertex_output_capacity(adjacency_matrix, vertex):
    return sum(adjacency_matrix[vertex])


def manipulate_graph(adjacency_matrix, vertex_types):
    sources = [i for i, x in enumerate(vertex_types) if x == 1]
    sinks = [i for i, x in enumerate(vertex_types) if x == 2]
    n_vertices = len(vertex_types) + 2
    new_vertex_types = [0 if i < n_vertices - 2 else i - n_vertices + 3 for i in range(n_vertices)]
    new_adjacency_matrix = [adjacency_matrix[i] + [0, 0] if i < n_vertices - 2 else [0 for _ in range(n_vertices)]
                            for i in range(n_vertices)]
    for source in sources:
        new_adjacency_matrix[n_vertices - 2][source] = get_vertex_output_capacity(adjacency_matrix, source)
    for sink in sinks:
        new_adjacency_matrix[sink][n_vertices - 1] = get_vertex_input_capacity(adjacency_matrix, sink)
    return new_adjacency_matrix, new_vertex_types


def create_graph():
    n_vertices = int(input())
    adjacency_matrix = [[0 for __ in range(n_vertices)] for _ in range(n_vertices)]
    vertex_types = list(map(int, input().strip().split()))
    n_edges = int(input())
    for i in range(n_edges):
        x, y, c = tuple(map(int, input().strip().split()))
        adjacency_matrix[x - 1][y - 1] = c
    adjacency_matrix, vertex_types = manipulate_graph(adjacency_matrix, vertex_types)
    return adjacency_matrix, vertex_types


class Graph:
    def __init__(self):
        self.adjacency_matrix, self.vertex_types = create_graph()
        self.n_vertices = len(self.vertex_types)
        self.source = self.n_vertices - 2
        self.sink = self.n_vertices - 1
        self.max_flow = 0
        self.FordFulkerson()
        return

    def BFS(self, s, t, parent):
        visited = [False] * self.n_vertices
        queue = [s]
        visited[s] = True
        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.adjacency_matrix[u]):
                if visited[ind] is False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
        return True if visited[t] else False

    def FordFulkerson(self):
        self.max_flow = 0
        parent = [-1] * self.n_vertices
        while self.BFS(self.source, self.sink, parent):
            print(parent)
            path_flow = float("Inf")
            s = self.sink
            while s != self.source:
                path_flow = min(path_flow, self.adjacency_matrix[parent[s]][s])
                s = parent[s]
            self.max_flow += path_flow
            v = self.sink
            while v != self.source:
                u = parent[v]
                self.adjacency_matrix[u][v] -= path_flow
                self.adjacency_matrix[v][u] += path_flow
                v = parent[v]
        return


def main():
    graph = Graph()
    print(graph.max_flow)


if __name__ == '__main__':
    main()
