def get_subgraph_by_node_filter(graph: BELGraph, node_predicates: NodePredicates) -> BELGraph:
    """Induce a sub-graph on the nodes that pass the given predicate(s)."""
    return get_subgraph_by_induction(graph, filter_nodes(graph, node_predicates))