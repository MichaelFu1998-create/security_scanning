def remove_unweighted_leaves(graph: BELGraph, key: Optional[str] = None) -> None:
    """Remove nodes that are leaves and that don't have a weight (or other key) attribute set.

    :param graph: A BEL graph
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.
    """
    unweighted_leaves = list(get_unweighted_upstream_leaves(graph, key=key))
    graph.remove_nodes_from(unweighted_leaves)