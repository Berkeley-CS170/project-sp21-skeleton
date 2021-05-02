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
    c_list = remove_c_nodes(H, c)
    #print(c_list)
    #remove k most vital edges
    k_list = remove_k_edges(H, k)
    #print(k_list)
    return c_list, k_list

def remove_c_nodes(G, c):
    #O(cV^3) overall contribution
    target = len(G) - 1
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



def remove_k_edges(G, k):
    #store list of all edges in graph
    #then find edges in maximum spanning tree
    #remove edges from list of all edges
    #afterwards, continue to remove edges until k_list is len(k) or less
    #remove the
    #(it would be less if the graph disconnects if we remove len(k) + 1 edges)
    mst = tree.maximum_spanning_edges(G, data=False)
    #print(list(mst))
    k_list = []
    return k_list


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
