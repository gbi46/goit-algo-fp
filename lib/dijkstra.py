from heapq import heappush, heappop
from collections import defaultdict
from math import inf

class Graph:
    """Directed weighted graph using adjacency lists."""
    def __init__(self, n):
        self.n = n
        self.adj = defaultdict(list)   # vertex -> list of (neighbor, weight)

    def add_edge(self, u, v, w):
        """Add edge u -> v with weight w (non-negative for Dijkstra)."""
        if w < 0:
            raise ValueError("Dijkstra's algorithm does not support negative weights.")
        self.adj[u].append((v, w))

def dijkstra(graph: Graph, src: int):
    """
    Computes the shortest distances from src to all vertices.
    Uses a binary heap (heapq) as a min-priority queue.

    Returns:
      dist: list of shortest path distances (inf if unreachable)
      parent: list of predecessors for path reconstruction
    """
    n = graph.n
    dist = [inf] * n
    parent = [-1] * n
    dist[src] = 0

    # Min-heap of tuples (distance_so_far, vertex)
    heap = [(0, src)]

    visited = [False] * n  # optional optimization to skip already processed nodes

    while heap:
        d, v = heappop(heap)
        if visited[v]:
            continue
        visited[v] = True

        # Skip outdated entries in the heap
        if d != dist[v]:
            continue

        # Relax edges
        for u, w in graph.adj[v]:
            nd = d + w
            if nd < dist[u]:
                dist[u] = nd
                parent[u] = v
                heappush(heap, (nd, u))

    return dist, parent

def reconstruct_path(parent, src, target):
    """Reconstructs one of the shortest paths src -> target using the parent array."""
    if parent[target] == -1 and src != target:
        return None  # unreachable
    path = []
    cur = target
    while cur != -1:
        path.append(cur)
        if cur == src:
            break
        cur = parent[cur]
    path.reverse()
    return path
