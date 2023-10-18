def get_causal_source_nodes(graph: BELGraph, func: str) -> Set[BaseEntity]:
    """Return a set of all nodes that have an in-degree of 0.

    This likely means that it is an external perturbagen and is not known to have any causal origin from within the
    biological system. These nodes are useful to identify because they generally don't provide any mechanistic insight.
    """
    return {
        node
        for node in graph
        if node.function == func and is_causal_source(graph, node)
    }