def get_subgraph_edges(graph: BELGraph,
                       annotation: str,
                       value: str,
                       source_filter=None,
                       target_filter=None,
                       ):
    """Gets all edges from a given subgraph whose source and target nodes pass all of the given filters

    :param pybel.BELGraph graph: A BEL graph
    :param str annotation:  The annotation to search
    :param str value: The annotation value to search by
    :param source_filter: Optional filter for source nodes (graph, node) -> bool
    :param target_filter: Optional filter for target nodes (graph, node) -> bool
    :return: An iterable of (source node, target node, key, data) for all edges that match the annotation/value and
             node filters
    :rtype: iter[tuple]
    """
    if source_filter is None:
        source_filter = keep_node_permissive

    if target_filter is None:
        target_filter = keep_node_permissive

    for u, v, k, data in graph.edges(keys=True, data=True):
        if not edge_has_annotation(data, annotation):
            continue
        if data[ANNOTATIONS][annotation] == value and source_filter(graph, u) and target_filter(graph, v):
            yield u, v, k, data