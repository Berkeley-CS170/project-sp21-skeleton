import re
import os

import networkx as nx

import utils

def validate_file(path):
    """File must not exceed 100KB and must contain only numbers and spaces"""
    if os.path.getsize(path) > 100000:
        print(f"{path} exceeds 100KB, make sure you're not repeating edges!")
        return False
    with open(path, "r") as f:
        if not re.match(r"^[\d\.\s]+$", f.read()):
            print(f"{path} contains characters that are not numbers and spaces")
            return False
    return True

def read_input_file(path, max_size=None):
    """
    Parses and validates an input file
    Args:
        path: str, a path
        max_size: int, number of max add_nodes_from
    Returns:
        Networkx graph if input is valid; AssertionError thrown otherwise
    """
    with open(path, "r") as fo:
        n = fo.readline().strip()
        assert n.isdigit(), 'Error in input file format'
        n = int(n)

        lines = fo.read().splitlines()
        fo.close()

        # validate lines
        for line in lines:
            tokens = line.split(" ")

            assert len(tokens) == 3, 'Error in input file format'
            assert tokens[0].isdigit() and int(tokens[0]) < n, 'Error in input file format'
            assert tokens[1].isdigit() and int(tokens[1]) < n, 'Error in input file format'
            assert bool(re.match(r"(^\d+\.\d{1,3}$|^\d+$)", tokens[2])), 'Error in input file format'
            assert 0 < float(tokens[2]) < 100 , 'Error in input file format'

        G = nx.parse_edgelist(lines, nodetype=int, data=(("weight", float),))
        G.add_nodes_from(range(n))

        assert nx.is_connected(G), 'Input Graph is not connected'

        for node, val in G.degree():
            assert val >= 2, 'Every vertex in the input graph should have degree atleast 2'

        return G


def write_input_file(G, path):
    """
    Write a graph to the input file format
    Args:
        G: NetworkX Graph, Graph to write to file
        path: str, path to input file
    Returns:
        None
    """
    with open(path, "w") as fo:
        n = len(G)
        lines = nx.generate_edgelist(G, data=["weight"])
        fo.write(str(n) + "\n")
        fo.writelines("\n".join(lines))
        fo.close()

def read_output_file(G, path):
    """
    Parses and validates an output file

    Args:
        G: input graph corresponding to input file
        path: str, path to output file
    Returns:
        score: the difference between the new and original shortest path
    """
    H = G.copy()
    if len(H) >= 20 and len(H) <= 30:
        max_cities = 2
        max_roads = 15
    elif len(H) > 30 and len(H) <= 50:
        max_cities = 3
        max_roads = 30
    elif len(H) > 50 and len(H) <= 100:
        max_cities = 5
        max_roads = 100
    else:
        print('Input Graph is not of a valid size')

    assert H.has_node(0), 'Source vertex is missing in input graph'
    assert H.has_node(len(G) - 1), 'Target vertex is missing in input graph'

    cities = []
    removed_edges = []

    with open(path, "r") as fo:

        number_of_cities = fo.readline().strip()
        assert number_of_cities.isdigit(), 'Number of cities is not a digit'
        number_of_cities = int(number_of_cities)

        assert number_of_cities <= max_cities, 'Too many cities being removed from input graph'

        for _ in range(number_of_cities):
            city = fo.readline().strip()
            assert city.isdigit(), 'Specified vertex is not a digit'
            city = int(city)
            assert H.has_node(city), 'Specified vertex is not in input graph'
            cities.append(city)

        number_of_roads = fo.readline().strip()
        assert number_of_roads.isdigit(), 'Number of roads is not a digit'
        number_of_roads = int(number_of_roads)

        for _ in range(number_of_roads):
            road = fo.readline().split()
            assert len(road) == 2, 'An edge must be specified with a start and end vertex'
            assert road[0].isdigit() and road[1].isdigit()
            u = int(road[0])
            v = int(road[1])
            assert H.has_edge(u, v), 'Specified edge is not in input graph'
            removed_edges.append((u,v))

    return utils.calculate_score(G, cities, removed_edges)

def write_output_file(G, c, k, path):
    """
    Writes the list of cities and roads to remove to an output file

    Args:
        G: input graph corresponding to input file
        c: list of cities (vertices)
        k: list of roads (edges)
    Returns:
        None
    """
    H = G.copy()

    for road in k:
        assert H.has_edge(road[0],road[1]), "{} is not a valid edge in graph G".format(road)
    H.remove_edges_from(k)
    
    for city in c:
        assert H.has_node(city), "{} is not a valid node in graph G".format(city)
    H.remove_nodes_from(c)

    assert nx.is_connected(H), "The solution is invalid as the graph disconnects"

    with open(path, "w") as fo:
        fo.write(str(len(c)) + "\n")
        for city in c:
            fo.write(str(city) + "\n")
        fo.write(str(len(k)) + "\n")
        for road in k:
            fo.write(str(road[0]) + " " + str(road[1]) + "\n")
        fo.close()
