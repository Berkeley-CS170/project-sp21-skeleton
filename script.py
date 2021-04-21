import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
from solver import dijkstra

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    d, p = dijkstra(G)
    t = len(G.nodes) - 1
    print(d[t])
    print("Path:")
    while t != 0:
        print(p[t])
        t = p[t]
    
    #c, k = solve(G)
    #assert is_valid_solution(G, c, k)
    #print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    #write_output_file(G, c, k, 'outputs/small-1.out')