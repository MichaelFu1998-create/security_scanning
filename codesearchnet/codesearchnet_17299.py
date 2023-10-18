def variants_of(
        graph: BELGraph,
        node: Protein,
        modifications: Optional[Set[str]] = None,
) -> Set[Protein]:
    """Returns all variants of the given node."""
    if modifications:
        return _get_filtered_variants_of(graph, node, modifications)

    return {
        v
        for u, v, key, data in graph.edges(keys=True, data=True)
        if (
            u == node
            and data[RELATION] == HAS_VARIANT
            and pybel.struct.has_protein_modification(v)
        )
    }