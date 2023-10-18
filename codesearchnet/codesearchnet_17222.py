def get_subgraph_by_node_search(graph: BELGraph, query: Strings) -> BELGraph:
    """Get a sub-graph induced over all nodes matching the query string.

    :param graph: A BEL Graph
    :param query: A query string or iterable of query strings for node names

    Thinly wraps :func:`search_node_names` and :func:`get_subgraph_by_induction`.
    """
    nodes = search_node_names(graph, query)
    return get_subgraph_by_induction(graph, nodes)