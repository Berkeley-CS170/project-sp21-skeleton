import networkx as nx
from networkx.algorithms import tree
from scipy.optimize import linprog
from parse import *
from utils import *
import sys
from os.path import basename, normpath
import glob
import time

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
    target = len(H) - 1

    #remove c most vital nodes
    c_list = remove_c_nodes(H, c, target)
    #remove k most vital edges
    J = H.copy()
    k_list = remove_k_edges(H, k, target)
    #k_list = lp_method(J, c, k, target)

    #c_list, k_list = algorithm5(H, c, k, target)


    return c_list, k_list

def lp_method(G, c, k, target, n=50):
    #### ILP Method ####
    # Time for one sample:
    #   Small:
    #   Medium:
    #   Large:
    # Small:
    # Medium:
    # Large:
    # Rank:
    ####################
    # x =
    weights = [e["weight"] for e in G.edges()]
    edges = list(G.edges())
    edges_inv = [(e[1], e[0]) for e in edges]
    E = len(edges)
    V = len(G)

    # z, e, e_inv, f_0, f_1, x_i for i in range n
    c = [0 for i in range((4 + n) * E + 1)]
    c[0] = -1

    A_ub, b_ub, A_eq, b_eq = [], [], [], []

    #all edge indicators must be less than or equal to 1
    for i in range(2 * E):
        temp = [0 for j in range((4 + n) * E + 1)]
        temp[1 + i] = 1
        A_ub.append(temp)
        b_ub.append(1)

    #dont duplicate directed edges
    for i in range(E):
        temp = [0 for j in range((4 + n) * E + 1)]
        temp[1 + i] = 1
        temp[1 + E + i] = 1
        A_eq.append(temp)
        b_eq.append(1)

    #remove max k edges
    temp = [0 for j in range((4 + n) * E + 1)]
    for i in range(2 * E):
        temp[1 + i] = -1
    A_ub.append(temp)
    b_ub.append(k - E)

    #connectivity

    #check if you can reach any other node from node 0

    # make node 0 source with V - 1 flow
    temp = [0 for j in range((4 + n) * E + 1)]
    for i in range(E):
        if edges[i][0] == 0:
            temp[1 + 2 * E + i] = 1
    A_eq.append(temp)
    b_eq.append(V - 1)

    # make all other nodes sinks
    for i in range(1, target):
        temp = [0 for j in range((4 + n) * E + 1)]
        for e in range(E):
            if edges[e][1] == i + 1:
                temp[1 + 2 * E + e] = 1
        A_eq.append(temp)
        b_eq.append(1)

    #check if any other node can reach node 0

    # make node 0 sink with V - 1 flow
    temp = [0 for j in range((4 + n) * E + 1)]
    for i in range(E):
        if edges[i][1] == 0:
            temp[1 + 2 * E + i] = 1
    A_eq.append(temp)
    b_eq.append(V - 1)

    # make all other nodes sources
    for i in range(1, target):
        temp = [0 for j in range((4 + n) * E + 1)]
        for e in range(E):
            if edges[e][0] == i + 1:
                temp[1 + 2 * E + e] = 1
        A_eq.append(temp)
        b_eq.append(1)

    # ensure flows are valid
    for i in range(E):
        temp = [0 for j in range((4 + n) * E + 1)]
        temp[1 + 2 * E + i] = 1
        temp[1 + i] = 1 - V
        temp[1 + E + i] = 1 - V
        A_ub.append(temp)
        b_ub.append(0)

    #shortest paths

    #TODO

    #maximize shortest paths

    for i in range(n):
        temp = [0 for j in range((4 + n) * E + 1)]
        for j in range(E):
            temp[1 + (4 + i) * E + j] = -1 * weights[j]
        A_ub.append(temp)
        b_ub.append(0)

    linprog(c,
            A_ub = A_ub,
            b_ub = b_ub,
            A_eq = A_eq,
            b_eq = b_eq,
            method = 'simplex',
            options = {"maxiter": 100, "disp":True})

    return [], []

def remove_k_edges(G, k, target):
    #### ALgorithm 1 ####
    # Small: ?
    # Medium: ?
    # Large: ?
    # Rank: 133
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

    #### Algorithm 2 ####
    # Small: 105.59667
    # Medium: 209.58743666666663
    # Large: ?
    # Rank: 113
    #store list of all edges in graph
    #then find edges in maximum spanning tree
    #remove edges from list of all edges
    #afterwards, continue to remove edges in order of how beneficial itd be to keep them
    #until k_list is len(k) or less
    #(it would be less if the graph disconnects if we remove len(k) + 1 edges)
    #guarantees connectivity via maximum spanning tree
    # k_list = []
    # mst = tree.maximum_spanning_edges(G, data=False)
    # mst_list = list(mst)
    # max_remove = min(k, len(G.edges())-len(mst_list))
    # while len(k_list) < max_remove:
    #     best = nx.shortest_path_length(G, source=0, target=target, weight='weight')
    #     path = nx.shortest_path(G, source=0, target=target, weight='weight')
    #     path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    #     best_edge = (0, 0)
    #     for edge in path_edges:
    #         if edge not in mst_list and edge[::-1] not in mst_list:
    #             G.remove_edge(*edge)
    #             st = nx.shortest_path_length(G, source=0, target=target, weight='weight')
    #             if st >= best:
    #                 best = st
    #                 best_edge = edge
    #             G.add_edge(*edge)
    #     if best_edge != (0, 0):
    #         k_list.append(best_edge)
    #         G.remove_edge(*best_edge)
    #     else:
    #         return k_list[:k]
    ####################

    #### Algorithm 3 ####
    # Small: 147.94377000000003
    # Medium: 223.33226999999994
    # Large: 359.34792666666687
    # Rank: 96
    # Node Fix
    #limited brute force by checking all edges along
    #the shortest path and seeing which removal is optimum
    #originally didn't attempt since I thought checking connectivity for every
    #attempted edge removal would massively affect performance, but its not
    #that much slower than Algorithm 2, and clearly more optimal
    k_list = []
    max_remove = min(k, len(G.edges()))
    while len(k_list) < max_remove:
        best = nx.shortest_path_length(G, source=0, target=target, weight='weight')
        path = nx.shortest_path(G, source=0, target=target, weight='weight')
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        best_edge = (0, 0)
        for edge in path_edges:
            G.remove_edge(*edge)
            if nx.is_connected(G):
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

    return k_list[:k]

def algorithm5(G, c, k, target):
    #### Algorithm 5 ####
    # Small: 67.23221000000001
    # Medium: 113.87769666666665
    # Large: 221.96333666666658
    # Rank: ?
    #limited brute force by checking all edges along
    #the shortest path and nodes along shortest path

    c_list, k_list = [], []

    condition = True
    while condition:
        best_edge, best_node = (0, 0), -1

        best = nx.shortest_path_length(G, source=0, target=target, weight='weight')
        best_n, best_e = best, best
        path = nx.shortest_path(G, source=0, target=target, weight='weight')

        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]

        for node in path[1:-1]:
            edges = list(G.edges(node))
            if G.degree[node] > 1:
                G.remove_node(node)
                if nx.is_connected(G):
                    new_length = nx.shortest_path_length(G, source=0, target=target, weight='weight')
                    if new_length >= best_n:
                        best_n = new_length
                        best_node = node
                G.add_node(node)
                G.add_edges_from(edges)

        for edge in path_edges:
            G.remove_edge(*edge)
            if nx.is_connected(G):
                new_length = nx.shortest_path_length(G, source=0, target=target, weight='weight')
                if new_length >= best_e:
                    best_e = new_length
                    best_edge = edge
            G.add_edge(*edge)

        if len(c_list) < c and best_n >= best_e and best_node != -1:
            c_list.append(best_node)
            G.remove_node(best_node)

        elif len(k_list) < k and best_e >= best_n and best_edge != (0, 0):
            k_list.append(best_edge)
            G.remove_edge(*best_edge)

        else:
            condition = False

    return c_list[:c], k_list[:k]


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
        if H.degree[node] > 1:
            H.remove_node(node)
            if nx.is_connected(H):
                new_length = nx.shortest_path_length(H, source=0, target=target, weight='weight')
                if new_length >= best_length:
                    best_node = node
                    best_length = new_length
    return best_node

if __name__ == '__main__':
    path = "inputs/small/small-1.in"
    start = time.time()
    G = read_input_file(path)
    H = G.copy()
    c, k = solve(H)
    end = time.time()
    print("Time Elapsed", end - start)
    assert is_valid_solution(G, c, k), "Invalid solution (disconnects graph)"
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    write_output_file(G, c, k, 'outputs/small-1.out')

    # assert len(sys.argv) == 2
    # size = sys.argv[1]
    # inputs = glob.glob('inputs/' + size + '/*')
    # total = 0
    # sum = 0
    # for input_path in inputs:
    #     filename = basename(normpath(input_path))[:-3]
    #     output_path = 'outputs/' + size + '/' + filename + '.out'
    #     G = read_input_file(input_path)
    #     c, k = solve(G)
    #     assert is_valid_solution(G, c, k)
    #     distance = calculate_score(G, c, k)
    #     total += 1
    #     sum += distance
    #     print("Shortest Path Difference for {}: {}".format(filename, distance))
    #     write_output_file(G, c, k, output_path)
    # print("Average Shortest Path Difference: {}".format(sum/total))
