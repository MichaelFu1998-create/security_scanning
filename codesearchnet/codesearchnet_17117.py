def prune_mechanism_by_data(graph, key: Optional[str] = None) -> None:
    """Remove all leaves and source nodes that don't have weights.

    Is a thin wrapper around  :func:`remove_unweighted_leaves` and :func:`remove_unweighted_sources`

    :param graph: A BEL graph
    :param key: The key in the node data dictionary representing the experimental data. Defaults to
     :data:`pybel_tools.constants.WEIGHT`.

    Equivalent to:

    >>> remove_unweighted_leaves(graph)
    >>> remove_unweighted_sources(graph)
    """
    remove_unweighted_leaves(graph, key=key)
    remove_unweighted_sources(graph, key=key)