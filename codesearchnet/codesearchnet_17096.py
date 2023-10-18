def get_causal_sink_nodes(graph: BELGraph, func) -> Set[BaseEntity]:
    """Returns a set of all ABUNDANCE nodes that have an causal out-degree of 0.

    This likely means that the knowledge assembly is incomplete, or there is a curation error.
    """
    return {
        node
        for node in graph
        if node.function == func and is_causal_sink(graph, node)
    }