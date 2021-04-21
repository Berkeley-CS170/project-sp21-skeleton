import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
from fibbonaciheap import FibonacciHeap as fib_heap

#modified version which returns all minimum paths?
#definitely need both vertex AND edge paths
#remember s is always 0 and t is always max vertex
def dijkstra(G):
    dist = {}
    prev = {}
    # since python numbers are unbounded, this caps the
    # max value at something higher and ensures Dijkstra works
    max_val = 100 * len(G.nodes)
    for v in G.nodes:
        dist[v] = max_val
    dist[0] = 0
    q = fib_heap()
    # keep dictionary of fib nodes for decreasekey
    fib_nodes = {}
    for v in dist.keys():
        fib_nodes[v] = q.insert(dist[v], v)
    while q.total_nodes > 0:
        u = q.extract_min().value
        for v in G.adj[u]:
            last_dist = dist[v]
            dist[v] = min(dist[v], dist[u] + G[u][v]['weight'])
            if dist[v] < last_dist:
                q.decrease_key(fib_nodes[v], dist[v])
                prev[v] = u
    return dist, prev



#heuristic of 0.001 will guarantee correct answer
def LPA_star(G):
    pass

#Possibly greediness? We know the minimum path is 
#the one that MUST be modified otherwise no change

#preprocess? That is if there s or t are degree one, cut them
# in a preprocess?

def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    pass


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         write_output_file(G, c, k, output_path)
