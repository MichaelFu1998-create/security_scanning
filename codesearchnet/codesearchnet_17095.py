def get_causal_central_nodes(graph: BELGraph, func: str) -> Set[BaseEntity]:
    """Return a set of all nodes that have both an in-degree > 0 and out-degree > 0.

    This means that they are an integral part of a pathway, since they are both produced and consumed.
    """
    return {
        node
        for node in graph
        if node.function == func and is_causal_central(graph, node)
    }