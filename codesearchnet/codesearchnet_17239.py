def rank_path(graph, path, edge_ranking=None):
    """Takes in a path (a list of nodes in the graph) and calculates a score

    :param pybel.BELGraph graph: A BEL graph
    :param list[tuple] path: A list of nodes in the path (includes terminal nodes)
    :param dict edge_ranking: A dictionary of {relationship: score}
    :return: The score for the edge
    :rtype: int
    """
    edge_ranking = default_edge_ranking if edge_ranking is None else edge_ranking

    return sum(max(edge_ranking[d[RELATION]] for d in graph.edge[u][v].values()) for u, v in pairwise(path))