import random
import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score, node_diff, edge_diff
import sys
from os.path import basename, normpath
import glob

MAX_EDGES_REMOVED = 30
MAX_NODES_REMOVED = 15


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    return simulatedAnnealing(0.9, G)


def simulatedAnnealing(initialTreshold, G):
    G = G.copy()
    endNode = len(G.nodes) - 1
    deletedEdges, deletedNodes = [], []
    def nodeRemover(threshold, nodesRemoved):
        if nodesRemoved > MAX_NODES_REMOVED or threshold >= 1:
            return
        largestYet, diff = None, 0 
        for i in G.nodes():
            if i == 0 or i == endNode:
                continue
            currentDiff = node_diff(G, i, endNode)
            if currentDiff and random.random() > threshold:
                largestYet = i
                break
            elif currentDiff and currentDiff > diff:
                largestYet = i
                diff = currentDiff
        if largestYet:
            deletedNodes.append(largestYet)
            G.remove_node(largestYet)
        return nodeRemover(threshold + 0.01, nodesRemoved + 1)
    
    def edgeRemover(threshold, edgesRemoved):
        if edgesRemoved > MAX_EDGES_REMOVED or threshold >= 1:
            return
        largestYet, diff = None, 0 
        for i in G.edges():
            currentDiff = edge_diff(G, i, endNode)
            if currentDiff and random.random() > threshold:
                largestYet = i
                break
            elif currentDiff and currentDiff > diff:
                largestYet = i
                diff = currentDiff
        if largestYet:
            deletedEdges.append(largestYet)
            G.remove_edge(largestYet[0],largestYet[1])
        return edgeRemover(threshold + 0.01, edgesRemoved + 1)

    
    nodeRemover(initialTreshold, 0)
    edgeRemover(initialTreshold, 0)
    
    print(deletedEdges, deletedNodes)
    return deletedNodes, deletedEdges

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
     assert len(sys.argv) == 2
     path = sys.argv[1]
     G = read_input_file(path)
     resultc, resultk, largest = None, None, 0
     for i in range(20):
        c, k = solve(G)
        if not is_valid_solution(G, c, k):
            continue
        currentScore = calculate_score(G, c, k)
        if largest < currentScore:
            resultc, resultk = c, k
            largest = currentScore
     print("Shortest Path Difference: {}".format(largest))
     write_output_file(G, c, k, 'outputs/small-1.out')
     print("Reference Shortest Score: " + str(calculate_score(G, [1], [(0, 27), (24, 29), (26, 29), (20, 16)])))


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
