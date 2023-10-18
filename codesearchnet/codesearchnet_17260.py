def get_walks_exhaustive(graph, node, length):
    """Gets all walks under a given length starting at a given node

    :param networkx.Graph graph: A graph
    :param node: Starting node
    :param int length: The length of walks to get
    :return: A list of paths
    :rtype: list[tuple]
    """
    if 0 == length:
        return (node,),

    return tuple(
        (node, key) + path
        for neighbor in graph.edge[node]
        for path in get_walks_exhaustive(graph, neighbor, length - 1)
        if node not in path
        for key in graph.edge[node][neighbor]
    )