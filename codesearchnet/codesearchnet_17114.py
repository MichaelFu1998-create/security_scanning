def is_unweighted_source(graph: BELGraph, node: BaseEntity, key: str) -> bool:
    """Check if the node is both a source and also has an annotation.

    :param graph: A BEL graph
    :param node: A BEL node
    :param key: The key in the node data dictionary representing the experimental data
    """
    return graph.in_degree(node) == 0 and key not in graph.nodes[node]