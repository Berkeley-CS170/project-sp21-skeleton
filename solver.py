import networkx as nx
from networkx.algorithms import tree
from parse import *
from utils import *
import sys
from os.path import basename, normpath
import glob

import matplotlib.pyplot as plt


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    if len(G) >= 20 and len(G) <= 30:
        c = 1
        k = 15
    elif len(G) > 30 and len(G) <= 50:
        c = 3
        k = 50
    elif len(G) > 50 and len(G) <= 100:
        c = 5
        k = 100
    H = G.copy()
    #remove c most vital nodes
    target = len(H) - 1
    c_list = remove_c_nodes(H, c, target)
    #print(c_list)
    #remove k most vital edges
    k_list = remove_k_edges(H, k, target)
    #print(k_list)
    return c_list, k_list

def remove_c_nodes(G, c, target):
    #O(cV^3) overall contribution
    c_list = []
    for i in range(c):
        node = remove_node(G, c, target)
        if node == -1:
            return c_list
        c_list.append(node)
        G.remove_node(node)

    return c_list

def remove_node(G, c, target):
    #remove one node along shortest path via brute force O(V^3)
    shortest_path = nx.shortest_path(G, source=0, target=target, weight='weight')
    best_node = -1
    best_length = nx.shortest_path_length(G, source=0, target=target, weight='weight')
    for node in shortest_path[1:-1]:
        H = G.copy()
        H.remove_node(node)
        if nx.is_connected(H):
            new_length = nx.shortest_path_length(H, source=0, target=target, weight='weight')
            if new_length >= best_length:
                best_node = node
                best_length = new_length
    return best_node



def remove_k_edges(G, k, target):
    #### ALgorithm 1 ####
    #fast algorithm but results are atrocious
    #store list of all edges in graph
    #then find edges in maximum spanning tree
    #remove edges from list of all edges
    #afterwards, continue to remove edges in order of least weight
    #until k_list is len(k) or less
    #(it would be less if the graph disconnects if we remove len(k) + 1 edges)
    #guarantees connectivity via maximum spanning tree
    # k_list = []
    # mst = tree.maximum_spanning_edges(G)
    # G.remove_edges_from(mst)
    # k_list = [(el[0], el[1]) for el in sorted(G.edges(data=True), key=lambda t: t[2].get('weight', 1))]
    # k_list = k_list[:k]
    ####################

    #### ALgorithm 2 ####
    #store list of all edges in graph
    #then find edges in maximum spanning tree
    #remove edges from list of all edges
    #afterwards, continue to remove edges in order of how beneficial itd be to keep them
    #until k_list is len(k) or less
    #(it would be less if the graph disconnects if we remove len(k) + 1 edges)
    #guarantees connectivity via maximum spanning tree
    k_list = []
    mst = tree.maximum_spanning_edges(G, data=False)
    mst_list = list(mst)
    max_remove = min(k, len(G.edges())-len(mst_list))
    while len(k_list) < max_remove:
        best = nx.shortest_path_length(G, source=0, target=target, weight='weight')
        path = nx.shortest_path(G, source=0, target=target, weight='weight')
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        best_edge = (0, 0)
        for edge in path_edges:
            if edge not in mst_list and edge[::-1] not in mst_list:
                G.remove_edge(*edge)
                st = nx.shortest_path_length(G, source=0, target=target, weight='weight')
                if st >= best:
                    best = st
                    best_edge = edge
                G.add_edge(*edge)
        if best_edge != (0, 0):
            k_list.append(best_edge)
            G.remove_edge(*best_edge)
        else:
            return k_list[:k]
    ####################

    #### ALgorithm 3 ####
    #construct up using shortest s-t paths and minimum s-t cut
    #algorithm from paper
    
    ####################
    return k_list[:k]


if __name__ == '__main__':
    # path = "inputs/medium/medium-2.in"
    # G = read_input_file(path)
    # H = G.copy()
    # c, k = solve(H)
    # assert is_valid_solution(G, c, k), "Invalid solution (disconnects graph)"
    # print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    # write_output_file(G, c, k, 'outputs/medium-2.out')

    assert len(sys.argv) == 2
    size = sys.argv[1]
    inputs = glob.glob('inputs/' + size + '/*')
    total = 0
    sum = 0
    for input_path in inputs:
        filename = basename(normpath(input_path))[:-3]
        output_path = 'outputs/' + size + '/' + filename + '.out'
        G = read_input_file(input_path)
        c, k = solve(G)
        assert is_valid_solution(G, c, k)
        distance = calculate_score(G, c, k)
        total += 1
        sum += distance
        print("Shortest Path Difference for {}: {}".format(filename, distance))
        write_output_file(G, c, k, output_path)
    print("Average Shortest Path Difference: {}".format(sum/total))


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
#         filename = basename(normpath(input_path))[:-3]
#         output_path = 'outputs/' + filename + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         print("Shortest Path Difference for {}: {}".format(filename, distance))
#         write_output_file(G, c, k, output_path)
