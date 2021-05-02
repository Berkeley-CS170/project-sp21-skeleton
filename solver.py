import networkx as nx
from parse import *
from utils import *
import sys
from os.path import basename, normpath
import glob


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    c_list = []
    k_list = []
    if len(G) >= 20 and len(G) <= 30:
        c = 1
        k = 15
    elif len(G) > 30 and len(G) <= 50:
        c = 3
        k = 50
    elif len(G) > 50 and len(G) <= 100:
        c = 5
        k = 100

    #start by removing most vital nodes
    #store list of all edges in graph
    #then find edges in maximum spanning tree
    #remove edges from list of all edges
    #afterwards, continue to remove edges until k_list is len(k) or less
    #remove the
    #(it would be less if the graph disconnects if we remove len(k) + 1 edges)
    return c_list, k_list

if __name__ == '__main__':
    path = "inputs/small/small-1.in"
    G = read_input_file(path)
    c, k = solve(G)
    assert is_valid_solution(G, c, k), "Invalid solution (disconnects graph)"
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    write_output_file(G, c, k, 'outputs/small-1.out')

    # assert len(sys.argv) == 2
    # size = sys.argv[1]
    # inputs = glob.glob('inputs/' + size + '/*')
    # for input_path in inputs:
    #     filename = basename(normpath(input_path))[:-3]
    #     output_path = 'outputs/' + filename + '.out'
    #     G = read_input_file(input_path)
    #     c, k = solve(G)
    #     assert is_valid_solution(G, c, k)
    #     distance = calculate_score(G, c, k)
    #     print("Shortest Path Difference for {}: {}".format(filename, distance))
    #     write_output_file(G, c, k, output_path)


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
