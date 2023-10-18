def generate_mechanism(graph: BELGraph, node: BaseEntity, key: Optional[str] = None) -> BELGraph:
    """Generate a mechanistic sub-graph upstream of the given node.

    :param graph: A BEL graph
    :param node: A BEL node
    :param key: The key in the node data dictionary representing the experimental data.
    :return: A sub-graph grown around the target BEL node
    """
    subgraph = get_upstream_causal_subgraph(graph, node)
    expand_upstream_causal(graph, subgraph)
    remove_inconsistent_edges(subgraph)
    collapse_consistent_edges(subgraph)

    if key is not None:  # FIXME when is it not pruned?
        prune_mechanism_by_data(subgraph, key)

    return subgraph