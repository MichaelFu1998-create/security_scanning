def remove_unweighted_sources(graph: BELGraph, key: Optional[str] = None) -> None:
    """Prune unannotated nodes on the periphery of the sub-graph.

    :param graph: A BEL graph
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.
    """
    nodes = list(get_unweighted_sources(graph, key=key))
    graph.remove_nodes_from(nodes)