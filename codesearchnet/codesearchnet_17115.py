def get_unweighted_sources(graph: BELGraph, key: Optional[str] = None) -> Iterable[BaseEntity]:
    """Get nodes on the periphery of the sub-graph that do not have a annotation for the given key.

    :param graph: A BEL graph
    :param key: The key in the node data dictionary representing the experimental data
    :return: An iterator over BEL nodes that are unannotated and on the periphery of this subgraph
    """
    if key is None:
        key = WEIGHT

    for node in graph:
        if is_unweighted_source(graph, node, key):
            yield node