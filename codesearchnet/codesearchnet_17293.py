def summarize_node_filter(graph: BELGraph, node_filters: NodePredicates) -> None:
    """Print a summary of the number of nodes passing a given set of filters.

    :param graph: A BEL graph
    :param node_filters: A node filter or list/tuple of node filters
    """
    passed = count_passed_node_filter(graph, node_filters)
    print('{}/{} nodes passed'.format(passed, graph.number_of_nodes()))