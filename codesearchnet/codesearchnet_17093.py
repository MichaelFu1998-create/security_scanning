def get_causal_out_edges(
        graph: BELGraph,
        nbunch: Union[BaseEntity, Iterable[BaseEntity]],
) -> Set[Tuple[BaseEntity, BaseEntity]]:
    """Get the out-edges to the given node that are causal.

    :return: A set of (source, target) pairs where the source is the given node
    """
    return {
        (u, v)
        for u, v, k, d in graph.out_edges(nbunch, keys=True, data=True)
        if is_causal_relation(graph, u, v, k, d)
    }