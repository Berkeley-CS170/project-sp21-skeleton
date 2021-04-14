import networkx as nx

def is_valid_solution(G, c, k):
    """
    Checks whether D is a valid mapping of G, by checking every room adheres to the stress budget.
    Args:
        G: networkx.Graph
        c: List of cities to remove
        k: List of edges to remove (List of tuples)
    Returns:
        bool: false if removing k and c disconnects the graph
    """
    size = len(G)
    H = G.copy()

    for road in k:
        assert H.has_edge(road[0], road[1]), "Invalid Solution: {} is not a valid edge in graph G".format(road)
    H.remove_edges_from(k)
    
    for city in c:
        assert H.has_node(city), "Invalid Solution: {} is not a valid node in graph G".format(city)
    H.remove_nodes_from(c)
    
    assert H.has_node(0), 'Invalid Solution: Source vertex is removed'
    assert H.has_node(size - 1), 'Invalid Solution: Target vertex is removed'

    return nx.is_connected(H)

def calculate_score(G, c, k):
    """
    Calculates the difference between the original shortest path and the new shortest path.
    Args:
        G: networkx.Graph
        c: list of cities to remove
        k: list of edges to remove
    Returns:
        float: total score
    """
    H = G.copy()
    assert is_valid_solution(H, c, k)
    node_count = len(H.nodes)
    original_min_dist = nx.dijkstra_path_length(H, 0, node_count-1)
    H.remove_edges_from(k)
    H.remove_nodes_from(c)
    final_min_dist = nx.dijkstra_path_length(H, 0, node_count-1)
    difference = final_min_dist - original_min_dist
    return difference
