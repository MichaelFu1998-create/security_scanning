def get_path_effect(graph, path, relationship_dict):
    """Calculate the final effect of the root node to the sink node in the path.

    :param pybel.BELGraph graph: A BEL graph
    :param list path: Path from root to sink node
    :param dict relationship_dict: dictionary with relationship effects
    :rtype: Effect
    """
    causal_effect = []

    for predecessor, successor in pairwise(path):

        if pair_has_contradiction(graph, predecessor, successor):
            return Effect.ambiguous

        edges = graph.get_edge_data(predecessor, successor)

        edge_key, edge_relation, _ = rank_edges(edges)

        relation = graph[predecessor][successor][edge_key][RELATION]

        # Returns Effect.no_effect if there is a non causal edge in path
        if relation not in relationship_dict or relationship_dict[relation] == 0:
            return Effect.no_effect

        causal_effect.append(relationship_dict[relation])

    final_effect = reduce(lambda x, y: x * y, causal_effect)

    return Effect.activation if final_effect == 1 else Effect.inhibition