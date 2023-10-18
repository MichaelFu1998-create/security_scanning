def summarize_edge_filter(graph: BELGraph, edge_predicates: EdgePredicates) -> None:
    """Print a summary of the number of edges passing a given set of filters."""
    passed = count_passed_edge_filter(graph, edge_predicates)
    print('{}/{} edges passed {}'.format(
        passed, graph.number_of_edges(),
        (
            ', '.join(edge_filter.__name__ for edge_filter in edge_predicates)
            if isinstance(edge_predicates, Iterable) else
            edge_predicates.__name__
        )
    ))