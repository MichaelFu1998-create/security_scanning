def rank_edges(edges, edge_ranking=None):
    """Return the highest ranked edge from a multiedge.

    :param dict edges: dictionary with all edges between two nodes
    :param dict edge_ranking: A dictionary of {relationship: score}
    :return: Highest ranked edge
    :rtype: tuple: (edge id, relation, score given ranking)
    """
    edge_ranking = default_edge_ranking if edge_ranking is None else edge_ranking

    edges_scores = [
        (edge_id, edge_data[RELATION], edge_ranking[edge_data[RELATION]])
        for edge_id, edge_data in edges.items()
    ]

    return max(edges_scores, key=itemgetter(2))