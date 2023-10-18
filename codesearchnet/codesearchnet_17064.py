def list_abundance_expansion(graph: BELGraph) -> None:
    """Flatten list abundances."""
    mapping = {
        node: flatten_list_abundance(node)
        for node in graph
        if isinstance(node, ListAbundance)
    }
    relabel_nodes(graph, mapping, copy=False)