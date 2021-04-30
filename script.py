import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
from solver import dijkstra, connected, weight, smart_greedy, mixed_greedy

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    edges, shortest = smart_greedy(G)#mixed_greedy(G)
    """d, p = dijkstra(G)
    t = max(G.nodes)
    print(d[t])
    print("Path:")
    while t != 0:
        print(p[t])
        t = p[t]
    print(connected(G))
    print(weight(G, 0))
    G.remove_node(6)
    print(connected(G))
    G.remove_node(9)
    G.remove_edge(2, 6)
    G.remove_edge(0, 1)
    G.remove_edge(1, 2)
    #the above two edges removed result in same shortest path
    G.remove_edge(5, 6)
    G.remove_edge(6, 8)
    d, p = dijkstra(G)
    t = max(G.nodes)
    print(d[t])
    print("Path:")
    while t != 0:
        print(p[t])
        t = p[t]"""
    
    #c, k = solve(G)
    #assert is_valid_solution(G, c, k)
    #print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    #write_output_file(G, c, k, 'outputs/small-1.out')