import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_solution, calculate_score
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
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    if 20 <= num_nodes <= 30:
        k_max = 15
        c_max = 1
    elif 31 <= num_nodes <= 50:
        k_max = 50
        c_max = 3
    elif 51 <= num_nodes <= 100:
        k_max = 100
        c_max = 5

    c = []
    k = []
    new_G = G.copy()
    while c_max > 0:
        shortest_path = nx.dijkstra_path(new_G, 0, num_nodes - 1)
        node_weights = []
        for i in range(1, len(shortest_path) - 1):
            node_weights.append(new_G[shortest_path[i-1]][shortest_path[i]]["weight"] + new_G[shortest_path[i]][shortest_path[i+1]]["weight"])

        removed = False
        if len(node_weights) == 0:
            # could discuss more here
            break
        while min(node_weights) < 9999 and not removed:
            min_index = node_weights.index(min(node_weights))
            min_node = shortest_path[1 + min_index]
            H = new_G.copy()
            H.remove_node(min_node)
            if nx.is_connected(H):
                c.append(min_node)
                new_G.remove_node(min_node)
                print("removed", min_node)
                c_max -= 1
                removed = True
            else:
                node_weights[min_index] = 9999
        if not removed:
            break
    """print("here")
    all_paths = list(nx.all_simple_paths(new_G, 0, num_nodes - 1))
    print("here!")
    edge_costs = {}
    edge_counts = {}
    print(len(edge_counts))
    for path in all_paths:
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            if edge not in edge_counts:
                edge_counts[edge] = 1
            else:
                edge_counts[edge] += 1
            if edge not in edge_costs:
                edge_costs[edge] = new_G[path[i]][path[i + 1]]["weight"]
    edge_heuristics = {}
    for e in edge_costs:
        edge_heuristics[e] = edge_costs[e] + 10 * edge_counts[e]"""

    while k_max > 0:
        shortest_path = nx.dijkstra_path(new_G, 0, num_nodes - 1)
        edge_weights = [new_G[shortest_path[i]][shortest_path[i+1]]["weight"] + 10 * new_G.degree[shortest_path[i]] + 10 * new_G.degree[shortest_path[i+1]] for i in range(len(shortest_path) - 1)]

        removed = False
        while min(edge_weights) < 9999 and not removed:
            min_index = edge_weights.index(min(edge_weights))
            min_edge = (shortest_path[min_index], shortest_path[min_index + 1])
            H = new_G.copy()
            H.remove_edge(shortest_path[min_index], shortest_path[min_index + 1])
            if nx.is_connected(H):
                k.append(min_edge)
                new_G.remove_edge(shortest_path[min_index], shortest_path[min_index + 1])
                k_max -= 1
                removed = True
            else:
                edge_weights[min_index] = 9999
        if not removed:
            break
        """shortest_path = nx.dijkstra_path(new_G, 0, num_nodes - 1)
        edge_weights = [edge_heuristics[(shortest_path[i], shortest_path[i + 1])] for i in range(len(shortest_path) - 1)]
        removed = False
        while min(edge_weights) < 999999999 and not removed:
            min_index = edge_weights.index(min(edge_weights))
            min_edge = (shortest_path[min_index], shortest_path[min_index + 1])
            H = new_G.copy()
            H.remove_edge(shortest_path[min_index], shortest_path[min_index + 1])
            if nx.is_connected(H):
                k.append(min_edge)
                new_G.remove_edge(shortest_path[min_index], shortest_path[min_index + 1])
                edge_heuristics.pop(min_edge)
                k_max -= 1
                removed = True
            else:
                edge_weights[min_index] = 9999
        if not removed:
            break"""

    print(c, k)
    return c, k

def edge_heuristic(G, e):
    return


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

"""if __name__ == '__main__':

    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    c, k = solve(G)
    assert is_valid_solution(G, c, k)
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    write_output_file(G, c, k, 'outputs/small/small-100.out')"""


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)

"""if __name__ == '__main__':
    inputs = glob.glob('inputs/medium/*')
    for input_path in inputs:
        print(input_path)
        output_path = 'outputs/medium/' + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        c, k = solve(G)
        print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
        assert is_valid_solution(G, c, k)
        distance = calculate_score(G, c, k)
        write_output_file(G, c, k, output_path)"""

if __name__ == '__main__':
    inputs = glob.glob('inputs/large/*')
    count = 1
    for input_path in inputs:
        output_path = 'outputs/large/' + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        """resultc, resultk, largest = None, None, 0
        for i in range(50):
            c, k = solve(G)
            if not is_valid_solution(G, c, k):
                continue
            currentScore = calculate_score(G, c, k)
            if largest < currentScore:
                resultc, resultk = c, k
                largest = currentScore"""
        c, k = solve(G)
        currentScore = calculate_score(G, c, k)
        existingSol = read_output_file(G, output_path)
        if currentScore > existingSol:
            write_output_file(G, c, k, output_path)
            print("enhanced by: " + str(currentScore - existingSol))
        print(str(count) + " out of " +str(len(inputs)) + " Done.")
        count += 1
