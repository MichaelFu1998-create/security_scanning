def get_unweighted_upstream_leaves(graph: BELGraph, key: Optional[str] = None) -> Iterable[BaseEntity]:
    """Get nodes with no incoming edges, one outgoing edge, and without the given key in its data dictionary.

    .. seealso :: :func:`data_does_not_contain_key_builder`

    :param graph: A BEL graph
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.
    :return: An iterable over leaves (nodes with an in-degree of 0) that don't have the given annotation
    """
    if key is None:
        key = WEIGHT

    return filter_nodes(graph, [node_is_upstream_leaf, data_missing_key_builder(key)])