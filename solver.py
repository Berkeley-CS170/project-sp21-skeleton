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

def explore(G, v, visited):
    visited[v] = True
    for u in G.adj[v]:
        if not visited[u]:
            explore(G, u, visited)

def connected(G):
    visited = {}
    for v in G.nodes:
        visited[v] = False
    explore(G, 0, visited)
    for v in visited.values():
        if not v:
            return False
    return True 

#measures total weight of edges summed 
def weight(G, v):
    w = 0
    for u in G.adj[v]:
        w += G[v][u]['weight']
    return w

#method to get shortest nodes from prev
def shortest_path(G, prev):
    t = max(G.nodes)
    path = [t]
    while t != 0:
        path.append(prev[t])
    return path

def smart_greedy(G):
    if len(G.nodes) <= 30:
        k = 15, c = 1
    else if len(G.nodes) <= 50:
        k = 50, c = 3
    else:
        k = 100, c = 5
    d, p = dijkstra(G)
    shortest = shortest_path(G, p)
    while k > 0:
        u = shortest[0]
        v = shortest[1]
        min_e = (u, v)
        for i in range(1, len(shortest) - 1):
            u = shortest[i]
            v = shortest[i + 1]
            e = (u, v)
            if G[u][v]['weight'] < G[min_e[0]][min_e[1]]['weight']:
                min_e = e
        G.remove_edge(min_e[0], min_e[1])
        if connected(G):
            #do something
        d, p = dijkstra(G)
        shortest = shortest_path(G, p)
        k -= 1

def mincut_solve(G):
    pass

#idea: greedy heuristics: remove the lightest nodes on the 
# the shortest path, that don't disconnect G until gone, 
# then remove edges. If not all c is used up, after edges
# are removed, check if more nodes can be deleted
# more intelligent heuristics, check if there are very heavy edges
# on a node, like 80+ heavy, and only delete if there are no very
# heavy edges
# Can we brute force solve the small graphs?
# Do complete graphs have special properties to exploit? (since
# I'm pretty sure everybody generated their big graphs using complete
# ones lol)
# More advanced heuristics: measuring the shortest path v from s to v
# and t to v, and then trying to find the lightest edges in either
# side and deleting them/maximize distance on two ends
# snip bridges on circular graphs

#observations: optimal edges removed between different values of k 
# seem largely unrelated
# for very connected graphs (maybe take degree into account)
# it seems best work backwards and force the path into a long
# one
# observations: the best nodes to remove seem to have an edge
# that needs removal
# there's the game tree alpha-beta pruning approach? since 
# it seems you can union together results cohesively
# special case: circular graphs, just snip connection between start and end

#heuristic of 0.001 will guarantee correct answer
def LPA_star(G):
    pass

#Possibly greediness? We know the minimum path is 
#the one that MUST be modified otherwise no change

#preprocess? That is if there s or t are degree one, cut them
# in a preprocess? !!!!!!!!!!!!

def preprocess(G):
    pass

def solve(G):
    #small k = 15, c = 1
    #medium k = 50, c = 3
    #large k = 100, c = 5
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
