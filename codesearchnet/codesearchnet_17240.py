def find_root_in_path(graph, path_nodes):
    """Find the 'root' of the path -> The node with the lowest out degree, if multiple:
         root is the one with the highest out degree among those with lowest out degree
    
    :param pybel.BELGraph graph: A BEL Graph
    :param list[tuple] path_nodes: A list of nodes in their order in a path
    :return: A pair of the graph: graph of the path and the root node
    :rtype: tuple[pybel.BELGraph,tuple]
    """
    path_graph = graph.subgraph(path_nodes)

    # node_in_degree_tuple: list of tuples with (node,in_degree_of_node) in ascending order
    node_in_degree_tuple = sorted([(n, d) for n, d in path_graph.in_degree().items()], key=itemgetter(1))
    # node_out_degree_tuple: ordered list of tuples with (node,in_degree_of_node) in descending order
    node_out_degree_tuple = sorted([(n, d) for n, d in path_graph.out_degree().items()], key=itemgetter(1),
                                   reverse=True)

    # In case all have the same in degree it needs to be reference before
    tied_root_index = 0

    # Get index where the min in_degree stops (in case they are duplicates)
    for i in range(0, (len(node_in_degree_tuple) - 1)):
        if node_in_degree_tuple[i][1] < node_in_degree_tuple[i + 1][1]:
            tied_root_index = i
            break

    # If there are multiple nodes with minimum in_degree take the one with max out degree
    # (in case multiple have the same out degree pick one random)
    if tied_root_index != 0:
        root_tuple = max(node_out_degree_tuple[:tied_root_index], key=itemgetter(1))
    else:
        root_tuple = node_in_degree_tuple[0]

    return path_graph, root_tuple[0]